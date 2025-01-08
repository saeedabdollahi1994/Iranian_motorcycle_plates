import os
import cv2
import numpy as np
import tkinter as tk
import time 
from gui_app import MyGUI
from gui_demo import DemoGUI
from ImageDetection import ImageDetect
import matplotlib


matplotlib.use('TkAgg',force=True)

def main():
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()

def demo_main():
    root = tk.Tk()
    app = DemoGUI(root)
    root.mainloop()    

if __name__ == "__main__":
    demo_main()
   
    '''
    main()
    folder_path = 'E:/Datasets/Iran_motorcycle_plate.v1i.yolov8/test/demo/'
    for file in os.listdir(folder_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            imgobject = ImageDetect(folder_path+file)
            image,plates,plate_list,plate_locations,top3_loc,last5_loc = imgobject.image_detection()
            print(file)
            for item in plate_list:
                print(item)
            bgr_pixel = image[0, 0]
            rgb_pixel = bgr_pixel[::-1]
            
            if (image[0, 0] == rgb_pixel).all():
                print(f"Image is already in RGB format.")

            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
           
            
            box_height, box_width = (len(plate_list)+1)*50, 300
            box = np.ones((box_height, box_width, 3), dtype=np.uint8) * 255 
            box[:, :] = (0, 255, 255)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (0, 0, 0)
            thickness = 2
            cv2.imshow("پلاک", image)
            cv2.waitKey(2000)
            
            for i in range(len(plate_list)):
                cv2.rectangle(image, (plate_locations[i][0],plate_locations[i][1]), (plate_locations[i][2],plate_locations[i][3]), (255,0,0), 2)
                cv2.putText(box, str(plate_list[i]), (20,(i+1)*50), font, font_scale, color, thickness)
                

            cv2.imshow("پلاک های تشخیص داده شده", box)
            cv2.waitKey(2000)

            for i in range(len(plates)):
                for j in range(3):
                    cv2.rectangle(plates[i], (top3_loc[j][1],top3_loc[j][0]), (top3_loc[j][3],top3_loc[j][2]), (0,255,255), 2)
                for k in range(5):
                    cv2.rectangle(plates[i], (last5_loc[k][1],last5_loc[k][0]), (last5_loc[k][3],last5_loc[k][2]), (0,255,255), 2)

                cv2.imshow("plate",plates[i])
                cv2.moveWindow("plate", 0, 0)
                cv2.waitKey(2000)
                cv2.destroyWindow("plate")

                 

                 
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
    
    '''
    