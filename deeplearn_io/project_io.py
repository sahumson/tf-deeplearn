# # coding: utf-8
# # DeepLearing Project Creation

import os
import shutil
import random
import json
import sys
import time
from library_io import deeplearn_lib


def project_folder(project_name, task_name):
    in_path = os.path.join((os.path.dirname(os.getcwd()) + "/dataset/"), project_name)
    out_path = os.path.join((os.path.dirname(os.getcwd()) + "/projects/"), project_name)
    sub_name = (project_name.lower()) + "_" + task_name
    sub_out_path = os.path.join(out_path, sub_name)
    try:
        if not os.path.exists(in_path):
            os.makedirs(in_path)
        # else:
        #     print("Folder already Exist: {}".format(in_path))
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        # else:
        #     print("Folder already Exist: {}".format(out_path))
        if not os.path.exists(sub_out_path):
            os.makedirs(sub_out_path)
        # else:
        #     print("Folder already Exist: {}".format(sub_out_path))
        print("{} : Project created successfully".format(project_name))
    except Exception as err:
        print("Error Found in creating folders: {}".format(err))

    # if not os.path.exists(in_path) or not os.path.exists(out_path):
    #     try:
    #         os.makedirs(out_path)
    #         os.makedirs(sub_out_path)
    #         os.makedirs(in_path)
    #         print("{} : Project created successfully".format(project_name))
    #     except Exception as err:
    #         print("Error Found in creating folders: {}".format(err))
    # else:
    #     print("Folders are already exits")

    try:
        data = {}
        # data1 = {}
        # data.setdefault(project_name, {})[task_name] = data1
        # data1['project_name'] = project_name
        # # data1.setdefault(task_name, {})['input_path'] = in_path
        data['project_name'] = project_name
        data['sub_folder_name'] = sub_name
        data['input_path'] = in_path
        data['output_path'] = out_path
        data['sub_folder_path'] = sub_out_path
        data['pre_trained_wts'] = os.path.abspath(os.path.join(os.getcwd(), '..', "pre_trained_weights"))
        jsonfile = os.path.join(os.getcwd(),'..', "deeplearnio_settings.json")
        sub_jsonfile = os.path.join(data["sub_folder_path"], (data["sub_folder_name"] + ".json"))
        with open(jsonfile, 'w+', encoding='utf8') as f:
            pt = json.dumps(data,indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            f.write(pt)
        shutil.copy(jsonfile, sub_jsonfile)
        print('JSON File created')
    except OSError:
        print('Error: creating deeplearnio_settings JSON File')
    print("---------------------------------------------------------------------")
    return in_path, out_path


def jsonreader():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(path)
    file = os.path.join(path, "deeplearnio_settings.json")
    with open(file, "r") as f:
        dict = json.load(f)
    return dict


def project_main(project_name, task_name, library):
    # dbpath = os.path.abspath(os.path.join(os.getcwd(),'..','docs'))
    # f = open(dbpath + "\\Database_file.txt", "a+")
    # infor = username + "  -@-  " + email + "  -@-  " + time.strftime("%d-%m-%Y  %H:%M:%S  (%Z)")
    # f.write(infor + '\n')
    # f.close()
    in_path, out_path = project_folder(project_name, task_name)
    lib_ver = deeplearn_lib(library)
    print("Successfully project created")

    return in_path, library, lib_ver

