import cv2
import numpy as np
from ultralytics import YOLO
import os
from time import sleep
from .config import model, init_camera

accuracy_min = 0.4
# picam = init_camera()

class DiceDetector:
  def __init__(self,picam2,val_thr=4):
    """
    Class for detecting dice results based on the number of repetitions of the same result.

    :param threshold: Number of repetitions of the same result to validate the result.
    """
    self.validate_threshold = val_thr  
    self.history = []
    self.confirmed_result = None # Remains none untl number of repetitions is equal to threshold
    self.picam2 = picam2

  def resetHistory(self):
    """
    Resets the history of the results due to a change in the detected results.
    """
    self.history = []
    self.confirmed_result = None

  def validateResult(self,result) -> int:
    """
    Validates the result of the detection based on the number of repetitions of the same result.

    :param result: Dictionary containing the result of the detection
        Each key is a dice number and each value contains a class list [label]
    :return 
    """
    n = len(self.history)
    print(self.history,result,n)

    if len(result.keys())==0: # Case when nothing is detected
      self.resetHistory()
      return None

    if n==0:
       self.history.append(result)
    else:
      last_result = self.history[n-1]
      last_result_keys = last_result.keys()
      result_keys = result.keys()
      for key in result_keys:
        if key in last_result_keys:
          num_of_instances_result = len(result[key])
          num_of_instances_last_result = len(last_result[key])
          if num_of_instances_result != num_of_instances_last_result: # For every key in a dict, check the length of an array which is equal to number of detected scores
            self.resetHistory()
            return None
        else:
          self.resetHistory()
          return None

      self.history.append(result)
      if self.validate_threshold==(n-1): # n is assigned before appending
        self.confirmed_result = result
  
  def printResult(self,result: dict):
    labels=[]
    for key,value in result.items():
      [labels.append(key) for _ in range(len(value))]
    print(f'Final result: {labels}')
    

  def detectAndDisplay(self,detection_threshold) -> dict:
      """
      Detects and displays the dice result based on the captured image from the camera

      :param detection_threshold: Minimum threshold for the detection to be considered valid

      :return dict: Dictionary containing the result of the detection
          Each key is a dice number and each value contains a class list [label,accuracy,bounding box]
      """
      result = {}

      frame = self.picam2.capture_array()[:,:,:3]
      detections = model(frame)[0]

      for box in detections.boxes:

        #extract accuracy along with bounding boxes and labels
        data=box.data.tolist()[0]
        accuracy = data[4]

        label=model.names.get(box.cls.item()) #extract the class label name

      # filter out bad detections
        if float(accuracy) < detection_threshold :
            continue
            
      
        # draw the bounding box on the picture
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        print(f'Label: {label}, Accuracy: {accuracy}, Bounding Box: ({xmin}, {ymin}, {xmax}, {ymax})')

        if result.get(label) is None:
          result[label] = []
          result[label].append([label,accuracy,(xmin, ymin, xmax, ymax)])
        else:
          result[label].append([label,accuracy,(xmin, ymin, xmax, ymax)])

        frame = np.ascontiguousarray(frame) # Converts to C-contigous array
        cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax),(0,255,0),2)
        y = ymin - 15 if ymin - 15 > 15 else ymin + 15
        cv2.putText(frame, "{} {:.1f}%".format(label,float(accuracy*100)), (xmin, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)


      cv2.imshow('frame', frame)
      cv2.waitKey(1)
      result = { k:v for k,v in sorted(result.items(),key=lambda item:item[0]) }
      return result,frame


# detector = DiceDetector(picam)
# while True:
    
#   accuracy_min = 0.5
#   res,frame = detector.detectAndDisplay(accuracy_min)
#   detector.validateResult(res)

#   if detector.confirmed_result is not None:
#     print(f'Confirmded result is {res} ')
#     detector.printResult(res)

#     sleep(5)
#     detector.resetHistory()

# self.picam2.stop()
