# based on https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

# assumes running from TF folder models/research/object_detection


import os
import glob
import argparse
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
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
    column_names = ['filename', 'width', 'height',
                    'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_names)
    return xml_df


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-o', '--outfile', help='Filename for output csv.', required=True)

    parser.add_argument('-f', '--folder',
                        help='Folder containing images and xml label files (default: current)')

    args = parser.parse_args()

    folder = args.folder
    if folder == None:
        folder = os.getcwd()

    xml_df = xml_to_csv(folder)
    if xml_df.shape[0] > 0:
        xml_df.to_csv(args.outfile, index=None)
        print('Successfully converted xml to csv.')
    else:
        print('Nothing to convert.')


main()
