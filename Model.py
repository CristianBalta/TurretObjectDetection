import importlib.util
import numpy as np

# Import TensorFlow libraries
# If tensorflow is not installed, import interpreter from tflite_runtime, else import from regular tensorflow
pkg = importlib.util.find_spec('tensorflow')

if pkg is None:
    from tflite_runtime.interpreter import Interpreter

else:
    from tensorflow.lite.python.interpreter import Interpreter

class Model:
    interpreter = None
    input_details = None
    output_details = None
    height = None
    width = None
    floating_model = None
    input_mean = None
    input_std = None

    def __init__(self, PATH_TO_CKPT):


        # Load the Tensorflow Lite model.
        self.interpreter = Interpreter(model_path=PATH_TO_CKPT)
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

        self.input_mean = 127.5
        self.input_std = 127.5
