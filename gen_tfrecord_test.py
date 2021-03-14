import argparse
import csv

label_dict = {}


def class_text_to_int(row_label):
    if row_label in label_dict:
        return label_dict[row_label]
    else:
        return None
    # if row_label == 'harddisk':
    #     return 1
    # else:
    #     return None


def load_labels(filename):
    # load label list and return a dictionary
        # with label name as key and id as value
        # label file is csv with <id,label> row (no header)
    with open(filename, 'rt', newline='') as in_file:
        reader = csv.reader(in_file)
        rows = list(reader)

    # iterate all rows and create set of unique label names
    for row in rows:
        label_dict[row[1]] = row[0]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--labelfile', help='Filename of label list file.', required=True)

    args = parser.parse_args()

    load_labels(args.labelfile)

    print(label_dict)

    # test
    print(class_text_to_int('harddisk'))
    print(class_text_to_int('stlogo'))
    print(class_text_to_int('toslogo'))


main()
