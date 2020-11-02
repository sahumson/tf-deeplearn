"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_invoice_labels.csv  --output_path=data/train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_invoice_labels.csv  --output_path=data/test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import re
import pandas as pd
import tensorflow as tf

from PIL import Image
from utils import dataset_util
from collections import namedtuple, OrderedDict


def create_label_dict(label_path):
    for files in os.listdir(label_path):
        if files.endswith(".pbtxt"):
            number = []
            label = []
            with open(label_path + '/' + files) as f:
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
                dictionary = dict(zip(label, number))
    return dictionary


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
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename))+'.jpg', 'rb') as fid:
    # with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:## THis is 2.0 tf version of gfile
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    # print(filename,path)
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
        # didt = {'quantity': 2, 'product': 1}
        # classes.append(didt[row['class']])
        # print(classes)

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


def generate_tf_record(output_dir, dictionary, csv_path):
    # print(output_dir)
    for csv_files in os.listdir(csv_path):
        if csv_files.endswith(".csv"):
            print(csv_files)
            csv_input = os.path.join(csv_path, csv_files)
            file = re.split(r'_', csv_files)[0]
            rcd_file = file + ".record"
            output_path = os.path.join(csv_path, rcd_file)
            writer = tf.compat.v1.python_io.TFRecordWriter(output_path) ## THis is the place where i modified tf 2.0 version
            # path = os.path.join(output_directory, directory)
            examples = pd.read_csv(csv_input)
            grouped = split(examples, 'filename')
            for group in grouped:
                tf_example = create_tf_example(group, output_dir, dictionary)
                writer.write(tf_example.SerializeToString())
            writer.close()
            # output_path = os.path.join(os.getcwd(), output_path)
            print('Successfully created the TFRecords: {}'.format(output_path))
    print("---------------------------------------------------------------------")


def main_tf_records(output_directory, pbtxt_path):
    dictionary = create_label_dict(pbtxt_path)
    generate_tf_record(output_directory, dictionary, pbtxt_path)


