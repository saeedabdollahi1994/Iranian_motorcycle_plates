from ultralytics import YOLO
import cv2
class Plate():
    def __init__(self,main_image):
        self.main_image = main_image
        self.top3 = []
        self.last5 = []

    def plate_detection(self):
        model_plate = YOLO("Yolo/best.pt")
        image = self.main_image
        results = model_plate(image,conf=0.50)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        list_plates = []
        locations = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0]) 
                label = model_plate.names[class_id]
                if label == '1':  
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    location = [x1,y1,x2,y2]  
                    cropped_plate = image_rgb[y1:y2, x1:x2]
                    resized_image = cv2.resize(cropped_plate, (640,640))
                    list_plates.append(resized_image)
                    locations.append(location)
        return list_plates,locations

    def numbers_detection(self,results_num):
        list1 = []
        last5_items = []
        for result in results_num:
            for box in result.boxes:
                list2 = []
                class_id = int(box.cls)   
                x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
                list2 = [y_min, x_min, y_max, x_max, class_id + 1]
                list1.append(list2)
            list1.sort(reverse= False)
            top3_list =  list1[:3]    
            sorted_top3 = sorted(top3_list, key=lambda x: x[1])
            top3 = [sublist[-1] for sublist in sorted_top3]
            top3_locations = [sublist[0:4] for sublist in sorted_top3]
            last5_items = list1[3:]
            sorted_last5 = sorted(last5_items, key=lambda x: x[1])
            last5 = [sublist[-1] for sublist in sorted_last5]
            last5_locations = [sublist[0:4] for sublist in sorted_last5]
            final_plate = [top3,last5]
        return final_plate,top3_locations,last5_locations  