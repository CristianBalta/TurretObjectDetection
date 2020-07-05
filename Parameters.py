import os

class Parameters:
    """Parameters"""
    labelmap_name = None
    modeldir = None
    graph_name = None
    min_conf_threshold = None
    imW = None
    imH = None
    PATH_TO_LABELS = None
    PATH_TO_CKPT = None
    labels = None

    def __init__(self):
        # Define input parameters
        self.labelmap_name = 'labelmap.txt'
        self.modeldir = 'modeldir'
        self.graph_name = 'detect.tflite'
        self.min_conf_threshold = float(0.5)
        self.imW, self.imH = int(1366), int(768)
        # Get path to current working directory
        self.CWD_PATH = os.getcwd()
        # Path to .tflite file, which contains the model that is used for object detection
        self.PATH_TO_CKPT = os.path.join(self.CWD_PATH, self.modeldir, self.graph_name)

        # Path to label map file
        self.PATH_TO_LABELS = os.path.join(self.CWD_PATH, self.modeldir, self.labelmap_name)

        # Load the label map
        with open(self.PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is 'background', which has to be removed.
        if self.labels[0] == 'background':
            del (self.labels[0])
