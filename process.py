from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import time
import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

class Process(object):

    def classify_image(interpreter, image, top_k=1):
        """Returns a sorted array of classification results."""
        set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))
        # If the model is quantized (uint8 data), then dequantize the results
        if output_details['dtype'] == np.uint8:
            scale, zero_point = output_details['quantization']
            output = scale * (output - zero_point)
            
            ordered = np.argpartition(-output, top_k)
            return [(i, output[i]) for i in ordered[:top_k]]

    def startPredict(self):

        with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
            camera.start_preview()
            try:
                stream = io.BytesIO()
                for _ in camera.capture_continuous(
                    stream, format='jpeg', use_video_port=True):
                    stream.seek(0)
                    image = Image.open(stream).convert('RGB').resize((width, height),Image.ANTIALIAS)
                    start_time = time.time()
                    results = classify_image(interpreter, image)
                    elapsed_ms = (time.time() - start_time) * 1000
                    label_id, prob = results[0]
                    stream.seek(0)
                    stream.truncate()
                    camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,elapsed_ms)
            finally:
                camera.stop_preview()
        return label_id



