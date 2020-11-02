# # coding: utf-8
# # DeepLearing Training

import os
import shutil

from models.tf_object_detection.modified.TF_objectdetection_train_io import tf_objectdetection_train
from models.tf_faster_rcnn.tools.FRCNN_endernewton_train_io import frcnn_endernewton_train



def parameters(iters, stepsize, classes, anchors, ratios, eval_eg, max_eval):
    # iter = iterations/no.of steps, stepsize = batchsize
    return iters, stepsize, classes, anchors, ratios, eval_eg, max_eval


def training_main(library, run_mode, model, param):
    if library == "Tensorflow":
        tf_objectdetection_train(run_mode, model, param)
        print("No Model")
    elif library == "Custom - FRCNN(endernewton)":
        frcnn_endernewton_train(run_mode, model, param)
        print("No Model")
    elif library == "CNTK":
        print("No Model")
    elif library == "Caffe":
        print("No Model")
    elif library == "Keras":
        print("No Model")
    else:
        print("Select training model")
