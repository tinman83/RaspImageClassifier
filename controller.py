from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter


class Controller(object):
    predictFlag=True
    labels=[]
    def load_labels(self,path):
        with open(path, 'r') as f:
            return {i: line.strip() for i, line in enumerate(f.readlines())}
    
    def set_input_tensor(self,interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image
    
    def classify_image(self,interpreter, image, top_k=1):
        """Returns a sorted array of classification results."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))
        # If the model is quantized (uint8 data), then dequantize the results
        if output_details['dtype'] == np.uint8:
            scale, zero_point = output_details['quantization']
            output = scale * (output - zero_point)
            
            ordered = np.argpartition(-output, top_k)

            return [(i, output[i]) for i in ordered[:top_k]]
    
    def readCamera(self,interpreter,labels,height,width):

        with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
            camera.start_preview()
            if self.predictFlag==True:
                #print("started preview")
                try:
                    stream = io.BytesIO()
                    for _ in camera.capture_continuous(
                        stream, format='jpeg', use_video_port=True):
                        stream.seek(0)
                        #print("image stream")
                        image = Image.open(stream).convert('RGB').resize((width, height),Image.ANTIALIAS)
                        start_time = time.time()
                        results = self.classify_image(interpreter, image)
                        elapsed_ms = (time.time() - start_time) * 1000
                        label_id, prob = results[0]
                        stream.seek(0)
                        stream.truncate()
                        camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,elapsed_ms)
                        #print(label_id)
                        #time.sleep(5)
                        predictFlag=True
                finally:
                    #camera.stop_preview()
                    self.predictFlag=True
                
            else:
                camera.stop_preview()
                return
        
    def run(self):
        labels = self.load_labels('/home/pi/Desktop/MLProject/Model/labels_mobilenet_quant_v1_224.txt')
        #interpreter = Interpreter(args.model)
        interpreter = Interpreter('/home/pi/Desktop/MLProject/Model/mobilenet_v1_1.0_224_quant.tflite')
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']

        self.predictFlag=True
        if self.predictFlag==True:
            self.readCamera(interpreter,labels,height,width)
        else:
            print("sleeping")
            time.sleep(10)
        # while True:
        #     #print('Hello from the Python Sorter Service')
        #     #label=process.startPredict()
        #     print("while loop")
            

        #     time.sleep(1)
