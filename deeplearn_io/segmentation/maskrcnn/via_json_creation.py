


import os, json, logging
from collections import OrderedDict


def get_xy_values(dir_path, jsonfile):

    region_dict = {}
    try:
        jsonfile_list = os.path.join(dir_path, jsonfile)
        with open(jsonfile_list, encoding="utf8") as word_data:
            word_ocr_data = json.load(word_data)
            for idx, line_info in enumerate(word_ocr_data["shapes"]):
                region_dict[str(idx)] = []
                xval = []
                yval = []
                for kdx, kval in enumerate(line_info["points"]):
                    xval.append(kval[0])
                    yval.append(kval[1])

                shape_dict = {"shape_attributes": {"name": "polygon",
                              "all_points_x": xval,
                              "all_points_y": yval},
                              "region_attributes": {"name": "damage"}}

                region_dict[str(idx)] = shape_dict
    except Exception as ex:
        logging.exception("Error in |get_word_coordinates| function: " + str(ex))

    return region_dict


def main(json_dir):

    via_dict = OrderedDict({})

    try:
        for idx, file in enumerate(os.listdir(json_dir)):

            region_dict = get_xy_values(json_dir, file)

            via_dict[file[:-4]+"jpg"] = {"fileref": "", "size": "",
                                        "filename": file[:-4]+"jpg",
                                        "base64_img_data": "",
                                        "file_attributes": {},
                                        "regions": region_dict}

            with open("via_region.json", 'w', encoding='utf-8') as outfile:
                json.dump(via_dict, outfile, indent=4, sort_keys=False, ensure_ascii=False)
    except Exception as ex:
        logging.exception("Error in |get_word_coordinates| function: " + str(ex))


if __name__ == '__main__':

    json_dir = "./jsons/"

    main(json_dir)

    print("process completed......")