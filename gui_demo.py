import tkinter as tk
from tkinter import filedialog,Button,Text,Label,Canvas
from VideoDetection import VideoDetect
from ImageDetection import ImageDetect
from PIL import Image, ImageTk
import time 
import cv2
import os
import numpy as np


class DemoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("تشخیص پلاک موتورسیکلت")
        self.root.geometry("+0+0")
        self.root.geometry("1100x650")
        self.root_width = 1100
        self.root_height = 650
        self.image1_width = self.root_width // 2
        self.image1_height = 500
        self.image2_width = int(self.root_width * 0.4)
        self.image2_height = int(self.root_height * 0.4)
        self.nextera_image = Image.open("nextera.jpg")  # Replace with your image path
        #self.nextera_image = self.nextera_image.resize((1100, 650))  # Resize the image to fit the canvas
        self.nextera_image_tk = ImageTk.PhotoImage(self.nextera_image)
        self.canvas_nextera = Canvas(root,width=573,height=395,bg="lightyellow")
        self.canvas_nextera.place(x=(self.root_width/2)-286,y=(self.root_height/2)-197)
        self.canvas_nextera.create_image(0, 0, anchor=tk.NW, image=self.nextera_image_tk)
        
        self.folder_path = 'E:/Datasets/Iran_motorcycle_plate.v1i.yolov8/test/demo/'
        self.files = [file for file in os.listdir(self.folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_index = 0
        self.tk_image = None
        self.root.after(15000, self.start_bg)
       
        

    def start_bg(self):
        self.bg_image = Image.open("motor.png")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1100, 650))  # Resize the image to fit the canvas
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        self.canvas_bg = Canvas(self.root,width=1100,height=650,bg="lightyellow")
        self.canvas_bg.place(x=0,y=0)
        self.canvas_bg.create_image(0, 0, anchor=tk.NW, image=self.bg_image_tk)
        self.root.after(5000, self.start_demo)

    def start_demo(self):
        self.canvas1 = Canvas(self.root, width=self.image1_width, height=self.image1_height, bg="lightgray")
        self.canvas1.place(x=0, y=0)
        self.canvas2 = Canvas(self.root, width=500,height=350, bg="lightyellow")
        self.canvas2.place(x=self.image1_width+10,y=0)
        self.text_font = ("Helvetica", 16)
        self.text_box = tk.Text(self.root, height=7, width=50,font=self.text_font)
        self.text_box.place(x=self.image1_width+10,y=360)
        if self.current_index < len(self.files):
            file = self.files[self.current_index]
            imgobject = ImageDetect(self.folder_path + file)
            image, plates, plate_list, plate_locations, top3_loc, last5_loc = imgobject.image_detection()
            

            # Ensure the image is in RGB format
            bgr_pixel = image[0, 0]
            rgb_pixel = bgr_pixel[::-1]
            if not (image[0, 0] == rgb_pixel).all():
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Draw rectangles around plates
            for i in range(len(plate_list)):
                cv2.rectangle(image, (plate_locations[i][0], plate_locations[i][1]), 
                              (plate_locations[i][2], plate_locations[i][3]), (255, 0, 0), 2)

            image = cv2.resize(image, (550,500))
            pil_image = Image.fromarray(image)
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.canvas1.create_image(0, 0, anchor="nw", image=self.tk_image)
            self.text_box.delete("1.0", tk.END)
            if len(plate_list) > 0:
                for i in range(len(plate_list)):
                    for j in range(3):
                        cv2.rectangle(plates[i], (top3_loc[i][j][1],top3_loc[i][j][0]), (top3_loc[i][j][3],top3_loc[i][j][2]), (0,255,255), 2)
                    for k in range(5):
                        cv2.rectangle(plates[i], (last5_loc[i][k][1],last5_loc[i][k][0]), (last5_loc[i][k][3],last5_loc[i][k][2]), (0,255,255), 2)
                    plt = cv2.resize(plates[i], (500,350))
                    pil_plt = Image.fromarray(plt)
                    self.plt_tk_image = ImageTk.PhotoImage(pil_plt)
                    self.canvas2.create_image(0, 0, anchor="nw", image=self.plt_tk_image)
                    self.text_box.insert(tk.END, plate_list[i] + "\n")
                    self.root.update()
                    time.sleep(5)   
               
            
            self.current_index += 1
            self.root.after(3000, self.start_demo)  # 3 seconds delay

            
                
                    
                

                

                 