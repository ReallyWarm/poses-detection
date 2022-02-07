import sys, os
from sys import platform
import argparse

class Pose(object):
    def __init__(self, dir_path, resolution):
        self.dir = dir_path
        self.importOP()

        self.args = ()
        self.params = dict()
        self.resolution = resolution
        self.setup()

    def importOP(self):
        # Import Openpose (Windows/Ubuntu/OSX)
        try:
            # Windows Import
            if platform == "win32":
                sys.path.append('E:/openpose/build/python/openpose/Release');
                os.add_dll_directory('E:/openpose/build/x64/Release')
                os.add_dll_directory('E:/openpose/build/bin')
                import pyopenpose as op
            else:
                sys.path.append('../../python');
                # sys.path.append('/usr/local/python')
                from pose import pyopenpose as op
            self.op = op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

    def setup(self):
        # Flags
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_path", default=self.dir + "/COCO_1.jpg", 
                            help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        self.args = parser.parse_known_args()

        # Custom Params (include/openpose/flags.hpp)
        self.params["model_folder"] = "E:\openpose\models"
        # default resolution is -1x368 ('656x368' equal to 720p and 1080p)
        self.params["net_resolution"] = self.resolution

        # Add others in path?
        for i in range(0, len(self.args[1])):
            curr_item = self.args[1][i]
            if i != len(self.args[1])-1: next_item = self.args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in self.params:  self.params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in self.params: self.params[key] = next_item

        # Construct it from system arguments
        # op.init_argv(self.args[1])
        # oppython = op.OpenposePython()

