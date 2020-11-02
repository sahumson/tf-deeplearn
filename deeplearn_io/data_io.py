# # coding: utf-8
# # DeepLearing Data Preparation or Preprocessing

import os
import sys
import shutil
import json
import random
from xml.dom.minidom import parse
from project_io import jsonreader
from utils.xmltocsv_io import pascal_xml_to_csv
from utils.tfrecord_io import main_tf_records


class get_data():
    def __init__(self, data_dir=None, in_path=None):
        self.input_folder = data_dir
        self.output_folder = in_path

    def data_from_directory(self):
        try:
            txt_file = os.path.join(self.output_folder, "basename.txt")  # (os.path.basename(output_path) + '.' + 'txt')
            f = open(txt_file, "w+")
            for files in os.listdir(self.input_folder):
                if files.endswith(".xml"):
                    name, extension = os.path.splitext(files)
                    xml_img = name + ".jpg"
                    if xml_img in os.listdir(self.input_folder):
                        src = os.path.join(self.input_folder, xml_img)
                        dst = os.path.join(self.output_folder, xml_img)
                        shutil.copy(src, dst)
                else:
                    name, extension = os.path.splitext(files)
                    img_xml = name + ".xml"
                    if img_xml in os.listdir(self.input_folder):
                        f.write(name + '\n')
                        src = os.path.join(self.input_folder, img_xml)
                        dst = os.path.join(self.output_folder, img_xml)
                        shutil.copy(src, dst)
            f.close()
            print("Unused files in input directory: {} ".format(len(os.listdir(self.input_folder))))
            print("Number of files in output directory: {} ".format(len(os.listdir(self.output_folder))-1))

        except Exception as err:
            print("Error Found in data from directory: {}".format(err))

        print("Successfully data moved to output directory: {}".format('\n' + self.output_folder))
        print("---------------------------------------------------------------------")

    def data_from_urllink(self):
        print("data_from_urllink")

    def data_from_server(self):
        print("data_from_server")


def random_images(in_path):
    img_list = []
    for files in os.listdir(in_path):
        if files.endswith(".jpg"):
            img = os.path.join(in_path, files)
            img_list.append(img)
    img_name_list = random.sample(img_list, 2)
    print("Random_Images:", img_name_list)
    return img_name_list


def class_labels(in_path):
    classlist = []
    for files in os.listdir(in_path):
        try:
            if files.endswith(".xml"):
                # print(files)
                xmlfile = os.path.join(in_path, files)
                dom = parse(xmlfile)
                namelist = dom.getElementsByTagName('name')
                for i, data in enumerate(namelist):
                    tag = namelist[i].firstChild._data
                    # print(tag)
                    classlist.append(tag)
        except Exception as err:
            print("Error Found in Class_names: {}".format(err))
    unique_class = list(set(classlist))
    # for i in range(len(unique_class)):
    #     print(i, unique_class[i])
    print("Class_Names:", unique_class)
    return unique_class


def pbtxt_file(path):
    in_path = os.path.join((os.path.dirname(os.getcwd()) + "/dataset/"), os.path.basename(os.path.dirname(os.path.dirname(path))))
    cls_lst = class_labels(in_path)
    try:
        f = open(os.path.join(path, 'class_labels.pbtxt'), 'w+')
        for i, txt in enumerate(cls_lst):
            id = i+1
            name = txt
            pt1 = "item { " + "\n" + "  " + "id:" + " " + str(id) + "\n" + "  " + "name:" + " " + "'" + str(
                name) + "'" + "\n" + "}"
            f.write(pt1 + "\n\n")
        f.close()
        print("Successfully pbtxt_file created")
    except Exception as err:
        print("Error found in creating pbtxt_file".format(err))


def frcnn_folders(in_path):
    frcn_path = os.path.join(in_path, "VOCdevkit2007/VOC2007")
    sublst = ["Annotations", "ImageSets/Main", "JPEGImages"]
    for subfldrs in sublst:
        frcn_in = os.path.join(frcn_path, subfldrs)
        try:
            if not os.path.exists(frcn_in):
                os.makedirs(frcn_in)
        except OSError:
            print('Error: creating frcnn_folders indirectory. ' + frcn_in)
    data = jsonreader()
    for files in os.listdir(in_path):
        if files.endswith(".xml"):
            src = os.path.join(in_path, files)
            dst = os.path.join(frcn_path+"/Annotations", files)
            shutil.move(src, dst)
        elif files.endswith(".jpg"):
            src = os.path.join(in_path, files)
            dst = os.path.join(frcn_path+"/JPEGImages", files)
            shutil.move(src, dst)
        elif files.endswith(".txt"):
            src = os.path.join(in_path, files)
            dst = os.path.join(frcn_path+"/ImageSets/Main", files)
            shutil.move(src, dst)
    try:
        data['xml_path'] = str(os.path.join(frcn_path, "Annotations"))
        data['image_path'] = str(os.path.join(frcn_path, "JPEGImages"))
        data['imgset_path'] = str(os.path.join(frcn_path, "ImageSets/Main"))
        sub_jsonfile = os.path.join(data["sub_folder_path"], (data["sub_folder_name"]+".json"))
        jsonfile = os.path.join(os.getcwd(),'..', "deeplearnio_settings.json")
        with open(jsonfile, 'w+', encoding='utf8') as f:
            pt = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            f.write(pt)
        shutil.copy(jsonfile, sub_jsonfile)
    except OSError:
        print('Error: creating deeplearnio_settings JSON File')


def data_split_object_detection(in_path, train):
    try:
        xml_list = []
        for files in os.listdir(in_path):
            if files.endswith(".xml"):
                xml_list.append(files)
        random.shuffle(xml_list)
        train_need = round((train / 100) * len(xml_list))
        train_imgNumber = xml_list[0:train_need]
        f = open(in_path + "/train.txt", "w+")
        for idx in train_imgNumber:
            name, extension = os.path.splitext(idx)
            f.write(name + '\n')
        f.close()
        print("Data splitting into Train:~{}% and Test:~{}%".format(train, (100 - train)))
        test_imgNumber = [x for x in xml_list if x not in train_imgNumber]
        f = open(in_path + "/test.txt", "w+")
        for idx1 in test_imgNumber:
            name, extension = os.path.splitext(idx1)
            f.write(name + '\n')
        f.close()
    except Exception as err:
        print("Error Found in data split: {}".format(err))
    print("Successfully data splitted")
    print("---------------------------------------------------------------------")


def data_split_frcnn(in_path, train):
    try:
        xml_list = []
        for files in os.listdir(in_path):
            if files.endswith(".xml"):
                xml_list.append(files)
        random.shuffle(xml_list)
        train_need = round((train / 100) * len(xml_list))
        train_imgNumber = xml_list[0:train_need]
        f = open(in_path + "/valid.txt", "w+")
        f1 = open(in_path + "/trainval.txt", "w+")
        for idx in train_imgNumber:
            name, extension = os.path.splitext(idx)
            f.write(name + '\n')
            f1.write(name + '\n')
        f.close()
        f1.close()
        print("Data splitting into Train:~{}% and Test:~{}%".format(train, (100 - train)))
        test_imgNumber = [x for x in xml_list if x not in train_imgNumber]
        f = open(in_path + "/test.txt", "w+")
        for idx1 in test_imgNumber:
            name, extension = os.path.splitext(idx1)
            f.write(name + '\n')
        f.close()
    except Exception as err:
        print("Error Found in data split: {}".format(err))
    print("Successfully data splitted")
    print("---------------------------------------------------------------------")


def data_extraction(data_dir, in_path):
    datacreate = get_data(data_dir, in_path)
    datacreate.data_from_directory()
    # get_data().data_from_directory(data_dir, in_path)
    cls_name_list = class_labels(in_path)
    random_img_list = random_images(in_path)
    return cls_name_list, random_img_list, "data extracted successfully"


def pre_processing_main(library, in_path, train, test=None, Eval=None):
    if library == "Tensorflow":
        data_split_object_detection(in_path, train)
        pbtxt_path = pascal_xml_to_csv(in_path)
        pbtxt_file(pbtxt_path)
        main_tf_records(in_path, pbtxt_path)
    elif library == "Custom - FRCNN(endernewton)":
        data_split_frcnn(in_path, train)
        frcnn_folders(in_path)  # FRCNN_folders
    elif library == "CNTK":
        print("No Model")
    elif library == "Caffe":
        print("No Model")
    elif library == "Keras":
        print("No Model")
    else:
        print("Select preprocessing model")
