# xml to csv conversion
# deep learning IO

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from project_io import jsonreader


def xml_to_csv(path):
    fh = open(path, "r")
    xml_list = []
    for line in fh:
        file = os.path.join(line.strip()+".xml")
        xmlpath = os.path.dirname(path)
        for xml_file in glob.glob(xmlpath + '\\' + file):
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
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    fh.close()
    return xml_df


def pascal_xml_to_csv(output_directory):
    jsn = jsonreader()
    csv_path = os.path.join(jsn["sub_folder_path"], "data")
    print(csv_path)
    try:
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
            for directory in ['train.txt', 'test.txt']:
                # image_path = os.path.join(os.getcwd(), 'images\{}'.format(directory))
                image_path = os.path.join(output_directory, directory)
                xml_df = xml_to_csv(image_path)
                csvname, extension = os.path.splitext(directory)
                xml_df.to_csv(os.path.join(csv_path, ('{}_labels.csv'.format(csvname))), index=None)
                print('Successfully converted xml to csv.')
        else:
            print("Folders are already exits")
    except OSError:
        print('Error: creating directory. ' + csv_path)
    # pbtxt_file(csv_path)
    print("---------------------------------------------------------------------")
    return csv_path


# if __name__ == "__main__":
#     print("CSV")
#
#     data_path = r"C:\Users\allara02\Desktop\Deeplearn IO\dataset\POPULAR"   # in_folder
#     pascal_xml_to_csv(data_path)
    # pdtxt = pascal_xml_to_csv(data_path) file location(return csv)