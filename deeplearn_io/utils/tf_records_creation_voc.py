
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import re
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple

import glob
import xml.etree.ElementTree as ET


def xml_to_csv(self):
    fh = open(self.txt_path, "r")
    xml_list = []
    for line in fh:
        file = os.path.join(line.strip()+".xml")
        print(file)
        # for xml_file in glob.glob(self.xmlpath + '\\' + file):
        xml_file = os.path.join(self.xmlpath, file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    self.xml_df = pd.DataFrame(xml_list, columns=column_name)
    fh.close()


def create_label_dict(self):

    number = []
    label = []

    with open(self.pbtxt_path, encoding='utf-8') as f:
        txt = f.read()
        lbyl = txt.splitlines()
        for i in range(len(lbyl)):
            data = lbyl[i].strip()
            if "id:" in data:
                num = re.findall('\d+', data)
                number.append(int(num[0]))
            elif "name:" in data:
                name = data[data.find("'") + 1:-1]
                label.append(name)
        self.dictionary = dict(zip(label, number))


# TO-DO replace this with label map
def class_text_to_int(row_label, dictionary):
    if row_label in dictionary:
        return dictionary[row_label]
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path, dictionary):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename))+'.jpg', 'rb') as fid:
    #with tf.compat.v1.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
    #with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class'], dictionary))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def generate_tf_record(self):

    for csv_files in os.listdir(self.output_directory):
        if csv_files.endswith(".csv"):
            print(csv_files)
            csv_input = os.path.join(self.output_directory, csv_files)
            file = re.split(r'_', csv_files)[0]
            rcd_file = file + ".record"
            output_path = os.path.join(self.output_directory, rcd_file)
            writer = tf.python_io.TFRecordWriter(output_path)
            #writer = tf.compat.v1.python_io.TFRecordWriter(output_path)
            examples = pd.read_csv(csv_input)
            grouped = split(examples, 'filename')
            for group in grouped:
                tf_example = create_tf_example(group, self.imgpath, self.dictionary)
                writer.write(tf_example.SerializeToString())
            writer.close()
            print('Successfully created the TFRecords: {}'.format(output_path))
    print("---------------------------------------------------------------------")




class tf_records_creation:

    def __init__(self):

        ###################  Parameter Changes  ##########################

        # self.input_directory = "/mnt/disk0/rainbow-cnn/data/pipeline/dataset/20181003_tf_object_det/split/"    ## in this directory "train.txt", "test.txt"
        # self.output_directory = "/mnt/disk0/rainbow-cnn/data/pipeline/dataset/20181003_tf_object_det/tfrecords/"
        # self.pbtxt_path = '/mnt/disk0/rainbow-cnn/data/pipeline/dataset/20181003_tf_object_det/rainbow_regions_pascal_label_map.pbtxt'
        # self.xmlpath = "/mnt/disk0/rainbow-cnn/data/All_Labelled_Xmlfiles/"
        # self.imgpath = "/mnt/disk0/rainbow-cnn/data/Fullset_Images/"
        #
        self.input_directory = "/home/buy/innovation/data/smart_recorder_item_coding/input/"    ## in this directory "train.txt", "test.txt"
        self.output_directory = "/home/buy/innovation/data/smart_recorder_item_coding/out/"
        self.pbtxt_path = "/home/buy/innovation/data/smart_recorder_item_coding/labelmap.pbtxt"
        self.xmlpath = "/home/buy/innovation/data/smart_recorder_item_coding/Annotations/"
        self.imgpath = "/home/buy/innovation/data/smart_recorder_item_coding/JPEGImages/"


    def pascal_xml_to_csv(self):

        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)
            for dir_txt in ['train.txt', 'test.txt']:
                self.txt_path = os.path.join(self.input_directory, dir_txt)
                xml_to_csv(self)
                csvname, extension = os.path.splitext(dir_txt)
                self.xml_df.to_csv(os.path.join(self.output_directory, ('{}_labels.csv'.format(csvname))), index=None, encoding='utf-8')
                # encoding='utf_8_sig' for chinese
                print('Successfully converted xml to csv.')
        except OSError:
            print('Error: creating directory. ' + self.output_directory)

        print("---------------------------------------------------------------------")


    def main_tf_records(self):

        create_label_dict(self)
        generate_tf_record(self)


if __name__ == "__main__":

    tf_records_objectdetection = tf_records_creation()
    tf_records_objectdetection.pascal_xml_to_csv()
    tf_records_objectdetection.main_tf_records()

    print("process done....")
