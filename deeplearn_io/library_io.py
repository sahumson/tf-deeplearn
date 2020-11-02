# # coding: utf-8
# # DeepLearing Library + Version + Platform

import os
import sys
import json
import tensorflow as tf
import platform
# from deeplearn_standalone.data_io import data_split_object_detection, data_split_frcnn


def object_detection():
    # data_split_object_detection()
    print("TF-Object_Detection")
    tf_py_ver = "Tensorflow {} Python {}".format(tf.__version__, platform.python_version())
    sys_ver = platform.architecture()[1][:-2] + " " + platform.architecture()[0]
    print("Version:", tf_py_ver)
    print("Platform:", sys_ver)
    return tf_py_ver, sys_ver


def faster_rcnn():
    # data_split_frcnn()
    print("Faster-RCNN")
    tf_py_ver = "Tensorflow {} Python {}".format(tf.__version__, platform.python_version())
    sys_ver = platform.architecture()[1][:-2] + " " + platform.architecture()[0]
    print("Version:", tf_py_ver)
    print("Platform:", sys_ver)
    return tf_py_ver, sys_ver


def deeplearn_lib(Library):
    if Library == "Tensorflow":
        lib_ver = object_detection()
    elif Library == "Custom - FRCNN(endernewton)":
        lib_ver = faster_rcnn()
    elif Library == "CNTK":
        print("No Model")
    elif Library == "Caffe":
        print("No Model")
    elif Library == "Keras":
        print("No Model")
    else:
        print("Select DeepLearning Library")
    print("---------------------------------------------------------------------")
    return lib_ver
