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
from process import Process


class Controller(object):
    def load_labels(self,path):
        with open(path, 'r') as f:
            return {i: line.strip() for i, line in enumerate(f.readlines())}
    
    def set_input_tensor(interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image
    
    def run(self):

        labels = self.load_labels('/tmp/labels_mobilenet_quant_v1_224.txt')
        #interpreter = Interpreter(args.model)
        interpreter = Interpreter('/tmp/mobilenet_v1_1.0_224_quant.tflite')
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
        process=Process()
        while True:
            #print('Hello from the Python Sorter Service')
            label=process.startPredict()
            print(label)
            time.sleep(1)
