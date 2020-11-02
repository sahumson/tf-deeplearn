# # coding: utf-8
# # Main DeepLearn IO

from project_io import project_main
from data_io import data_extraction, pre_processing_main
from training_io import parameters, training_main

# ======================================================================= #1 project
# username = 'PersonName'
# Email = 'XXXXX@gmail.com'
# in_path, out_path = project_folder(project_name)

project_name = "Road_quality"  # Project Name
task_name = "images"  # Task Name
library = "Tensorflow"  # "Choose library"
# library = "Custom - FRCNN(endernewton)"
in_path, libr, lib_ver = project_main(project_name, task_name, library)
# ======================================================================== #2 data preparation
data_directory = r"./frames"  # Data Path
cls_name_list, random_img_list, statusmessage= data_extraction(data_directory, in_path)
train = 70
test = 30
pre_processing_main(libr, in_path, train)
# ======================================================================== #3 training
run_mode = "train"
model = "ssd_mobilenet_v1_coco"
# model = "res101"
# ==================== #
iterations = 10000
step_size = 24
num_class = 2
anchor_size = "[8,16,32]"
ratio_size = "[0.5,1,2]"
eval_examples = 2000
max_evalation = 10
param = parameters(iterations, step_size, num_class, anchor_size, ratio_size, eval_examples, max_evalation)
# ==================== #
training_main(library, run_mode, model, param)
# ======================================================================== #
#

# Invoice_Training_images_sri_47_1-quantity




