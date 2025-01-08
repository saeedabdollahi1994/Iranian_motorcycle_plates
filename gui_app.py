import tkinter as tk
from tkinter import filedialog,Button,Text,Label,Canvas
from VideoDetection import VideoDetect
from ImageDetection import ImageDetect
from PIL import Image, ImageTk
import cv2
import numpy as np

class MyGUI():
    def __init__(self,root):
        self.root = root
        self.root.title("تشخیص پلاک موتورسیکلت")
        self.root.geometry("800x600")
        self.upload_button = Button(root, text="انتخاب فایل", command=self.upload_file, bg="yellow", fg="black")
        self.upload_button.place(x=50, y=50)
        self.plate_list = []
       
    def upload_file(self):
        plate_list = self.plate_list
        file_path = filedialog.askopenfilename(
            title="Select Image or Video File",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp"),
                       ("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
           
        if file_path:
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                imgobject = ImageDetect(file_path)
                image,plates,plate_list,plate_locations,top3_loc,last5_loc = imgobject.image_detection()
                '''
                 bgr_pixel = image[0, 0]
                rgb_pixel = bgr_pixel[::-1]  # Reverse to simulate RGB format

                if (image[0, 0] == rgb_pixel).all():
                    print(f"Image is already in RGB format.")

                else:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                '''
               
                
                cv2.imshow("پلاک", image)
                box_height, box_width = len(plate_list)*100, 500
                box = np.ones((box_height, box_width, 3), dtype=np.uint8) * 255 
                box[:, :] = (0, 255, 255)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (0, 0, 0)  # Black text
                thickness = 2
                for i in range(len(plate_list)):
                    cv2.putText(box, str(plate_list[i]), (20,(i+1)*50), font, font_scale, color, thickness)
                cv2.imshow("پلاک های تشخیص داده شده", box)

                '''
                pil_image = Image.fromarray(image)
                tk_image = ImageTk.PhotoImage(pil_image)
                self.image_frame.config(image=tk_image)
                self.image_frame.image = tk_image
                '''
                
            elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                n = 100  # Process every nth frame
                current_frame = 0
                k = 0
                cap = cv2.VideoCapture(file_path)
                if not cap.isOpened():
                    print("Error: Cannot open video file.")
                    exit()
                    
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    vid_object = VideoDetect(frame)
                    frame,plate_list = vid_object.frame_detection()
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.imshow("Video", frame)
                    
                    if len(plate_list) > 0:
                        k = k + 1
                        box_height, box_width = 300, 500
                        box = np.ones((box_height, box_width, 3), dtype=np.uint8) * 255 
                        box[:, :] = (0, 255, 255)
                        for i in range(len(plate_list)):
                             cv2.putText(box, str(plate_list[i]), (20,(i+1)*50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        cv2.imshow("Plates", box)
                        plate_list.clear

                    elif cv2.getWindowProperty("Plates", cv2.WND_PROP_VISIBLE) >= 1:
                        box[:, :] = (0, 255, 255)
                        #cv2.destroyWindow("Plates")

                    if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    
                    current_frame += n
                    
                cap.release()
                cv2.destroyAllWindows()   

        else:
            Text.showerror("Error", "Unsupported file format!")

