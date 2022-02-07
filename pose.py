import sys, os
import cv2
from openpose import Pose

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    resolution = '320x176'
    
    # Import Openpose
    pose = Pose(dir_path, resolution)

    # Starting OpenPose
    # opWrapper = pose.op.WrapperPython(pose.op.ThreadManagerMode.Synchronous)
    opWrapper = pose.op.WrapperPython()
    opWrapper.configure(pose.params)
    # opWrapper.execute()
    opWrapper.start()

    # Process Image
    datum = pose.op.Datum()
    imageToProcess = cv2.imread(pose.args[0].image_path)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(pose.op.VectorDatum([datum]))

    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
    cv2.waitKey(0)

except Exception as e:
    print(e)
    sys.exit(-1)