import os
from PlateNumbers import Plate
import cv2
from ultralytics import YOLO


class ImageDetect():
    def __init__(self,image):
       self.image = image
       self.plate_list= []
        
    def image_detection(self): 
        final_top3_loc = []
        final_last5_loc = []
        image = self.image
        plate_list = self.plate_list
        image = cv2.imread(image)
        myplate = Plate(image)
        plates,plate_locations = myplate.plate_detection()
        image = cv2.resize(image, (640,640))
        confidence = 0.80
        for i in range(len(plates)):
            model_nums = YOLO("YOLO/best_nums_weights.pt")
            results_num = model_nums(plates[i],conf=confidence)
            if(len(results_num[0].boxes) == 8): 
                result,top3_loc,last5_loc = myplate.numbers_detection(results_num)
                final_top3_loc.append(top3_loc)
                final_last5_loc.append(last5_loc)
                print(result[0]+result[1])
                up3 = " "
                bottom5 = " "
                for num in result[0]:
                    up3 = up3 + str(num)

                for num in result[1]:
                    bottom5 = bottom5 + str(num) 
                
                output = up3+"__"+bottom5     
                plate_list.append(output)
                bgr_pixel = image[0, 0]
                rgb_pixel = bgr_pixel[::-1]  # Reverse to simulate RGB format

                if (image[0, 0] == rgb_pixel).all():
                    print(f"Image is already in RGB format.")

                else:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result.clear
            elif(len(results_num[0].boxes) > 8):
                i = i - 1
                confidence = confidence + 0.03
                
            else:
                i = i - 1
                confidence = confidence - 0.03

        return image,plates,plate_list,plate_locations,final_top3_loc,final_last5_loc