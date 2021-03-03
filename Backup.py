import pyzed.sl as sl
import cv2
import numpy as np
import time
import math
import sys
import itertools
import importlib

"""
    To-Do:
        1) Work on checking the coordinates in coordinates_List and determining what the distances of each of the coordinates are. 
            If a coordinate is in the danger zone (STILL HAVE TO CREATE), send a signal to stop and re-adjust (HAVE TO WORK ON with jetson).

"""


def Initialize_Zed():
    # Creates a zed camera object
    zed_Camera = sl.Camera()

    init_Parameters = sl.InitParameters()   # Creates an initial Parameters object
    init_Parameters.camera_resolution = sl.RESOLUTION.HD1080    # Sets the camera resolution to 1080p
    init_Parameters.camera_fps = 30     # Sets the camera frames per second to 30
    init_Parameters.depth_mode = sl.DEPTH_MODE.ULTRA    # Sets depth mode to ultra for the best z-range accuracy
    init_Parameters.coordinate_units = sl.UNIT.FOOT     # Sets the unit of measure of the camera to feet
    init_Parameters.depth_minimum_distance = 6          # Sets the minimum distance detection to 6 feet

    err = zed_Camera.open(init_Parameters)     # Opens the zed camera with the initial parameters
    
    # Checks to make sure that the zed camera successfully opened up, if not a message will pop up with the error
    if err != sl.ERROR_CODE.SUCCESS:
        print(f'ERROR ON STARTUP: {err}')
        exit(-1)

    return zed_Camera   # Returns the zed camera object if the initialization was successful

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Distance_Print(depth_Map, x, y):
    error, distance = depth_Map.get_value(x, y)

    if error == sl.ERROR_CODE.SUCCESS:
        if np.isnan(distance) or np.isinf(distance):
            print("Please move the camera back")
        else:
            print(distance)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
# This function calculates a matrix of 30 coordinates that we will be checking to determine distance. It will return a list of the coordinates
def Get_Frame_Coords(zed_Camera):
    x_Increment = int(zed_Camera.get_camera_information().camera_resolution.width / 5)      # Calculates the x increment
    y_Increment = int(zed_Camera.get_camera_information().camera_resolution.height / 6)     # Calculates the y increment

    coords_List = []

    # Uses the itertools module to quickly iterate through a 2D matrix and creating a coordinate tuple which is appended to a coordinates list
    for x, y in itertools.product(range(x_Increment, zed_Camera.get_camera_information().camera_resolution.width, x_Increment), range(y_Increment, zed_Camera.get_camera_information().camera_resolution.height, y_Increment)):
        coord = (x, y)
        coords_List.append(coord)

    # Returns the coordinates list
    return coords_List




# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Check_Distance_Values(image):
    x_Increment = image.get_width() / 5       # Gets an x increment value that will be used to check distance values at different spots on the frame
    y_Increment = image.get_height() / 6      # Gets an y increment value that will be used to check distance values at different spots on the frame



    
    

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Run_Zed_Camera():
    zed_Camera = Initialize_Zed()   # Gets a zed camera object with inialization

    image_Map, depth_Map = sl.Mat(), sl.Mat()   # Creates an image and depth matrix that will be used to hold information taken in fromt he zed camera

    runtime_Parameters = sl.RuntimeParameters()     # Retrieves runtime parameters
    runtime_Parameters.confidence_threshold = 50    # Sets the confidence threshold to 5, on a scale from [1,100], the lower the value the higher the confidence of an object

    coordinates_List = Get_Frame_Coords(zed_Camera)     # Creates a coordinates list that contains coordinates that we are interested in which we will use to determine distance

    while True:
        if(zed_Camera.grab(runtime_Parameters) == sl.ERROR_CODE.SUCCESS):
            zed_Camera.retrieve_image(image_Map, sl.VIEW.LEFT)     # Retrives the image from the left lense of the zed camera

            zed_Camera.retrieve_measure(depth_Map, sl.MEASURE.DEPTH)    # Retrieves the depth image from the left lense
            depth_OpenCV = depth_Map.get_data()         # converts the zed matrix to a numpy array that can be used by opencv
            cv2.imshow("Depth Image", depth_OpenCV)     # Displays the depth image






            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

    print("SUCCESS")


Run_Zed_Camera()


