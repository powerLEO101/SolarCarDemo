from collections.abc import Callable
from tkinter import *
from typing import Tuple
import numpy as np
import cv2
from PIL import Image, ImageTk
import sys

class SolarCar(object):
    def __init__(self, get_speed: Callable, get_pos: Callable, gps_dim: Tuple):
        if (gps_dim[0] > gps_dim[2]) or (gps_dim[1] > gps_dim[3]):
            print('Wrong GPS boundary')
            sys.exit(1)
        root = Tk()
        root.geometry('400x400')
        root.title('Kent Solar Car')

        self.gps_dim = gps_dim
        self.get_speed = get_speed
        self.get_pos = get_pos
        self.root = root
        self.speed_str = StringVar()
        self.speed_label = Label(self.root,
                                 textvariable=self.speed_str,
                                 font=('Arial', 16, 'bold'))
        self.speed_entry = Entry(self.root,
                                 textvariable=self.speed_str)
        self.map = Canvas(root,
                          bg='blue',
                          height=100,
                          width=100)
        self.map_image = Image.open('/home/leo101/Pictures/Selection_006.png')

        self.speed_label.pack(pady=20)
        self.map.pack()

        self.update_speed()
        self.update_pos()
        #self.speed_entry.pack()

    def update_speed(self):
        x = self.get_speed()
        self.speed_str.set(f'Speed: {x} km/h')
        self.root.after(100, self.update_speed)
    
    def get_window_dim(self):
        return self.root.winfo_width(), self.root.winfo_height()

    def get_map_dim(self):
        return self.map.winfo_width(), self.map.winfo_height()

    def draw_google_map(self):
        m_x, m_y = self.get_map_dim()
        map_image_resized = self.map_image.resize((m_x, m_y))
        self.map_image_tk = ImageTk.PhotoImage(image=map_image_resized)
        self.map.create_image(0, 0, image=self.map_image_tk, anchor=NW)

    def redraw_map(self):
        w_x, w_y = self.get_window_dim()
        self.map.config(width=w_x - 30, height=w_y - 30)
        m_x, m_y = self.get_map_dim()
        self.map.delete('all')
        self.draw_google_map()
        self.map.create_rectangle(30, 30, m_x - 30, m_y - 30, width=10)

    def gps_to_map(self, x):
        if (x[0] < self.gps_dim[0]) or \
           (x[0] > self.gps_dim[2]) or \
           (x[1] < self.gps_dim[1]) or \
           (x[1] > self.gps_dim[3]):
               print('Out of boundary')
               return 0, 0
        m_x, m_y = self.get_map_dim()
        current_x = (x[0] - self.gps_dim[0]) / (self.gps_dim[2] - self.gps_dim[0])
        current_y = (x[1] - self.gps_dim[1]) / (self.gps_dim[3] - self.gps_dim[1])
        current_x *= m_x
        current_y *= m_y
        return current_x, current_y

    def update_pos(self):
        x, y = self.get_pos()
        x, y = self.gps_to_map([x, y])
        self.redraw_map()
        self.map.create_oval(x, y, x + 10, y + 10, fill='red')
        self.root.after(100, self.update_pos)

    def start_loop(self):
        self.root.mainloop()

def get_speed():
    return float(np.random.rand())

def get_pos():
    x_len = gps_dim[2] - gps_dim[0]
    y_len = gps_dim[3] - gps_dim[1]
    x_base = gps_dim[0]
    y_base = gps_dim[1]
    return float(np.random.rand() * x_len + x_base), float(np.random.rand() * y_len + y_base)

gps_dim = (41.72454112609995, -73.4811918422402, 41.72635922342008, -73.47515215049468)
solar = SolarCar(get_speed, get_pos, gps_dim)
solar.start_loop()
