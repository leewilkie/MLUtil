import csv
import argparse


def from_txt():
    with open("labels.txt", "rt") as text_file:
        pbtxt = []

        # fill pbtxt array from file lines
        lines = text_file.readlines()
        for line in lines:
            # remove newline
            line = line.replace('\n', '')
            # split on colon
            vals = line.split(':')
            pbtxt.append("item {\n")
            pbtxt.append("  id: {}\n".format(vals[0]))
            pbtxt.append("  name: {}\n".format(vals[1]))
            pbtxt.append("}\n")

        print(pbtxt)

        return pbtxt


def from_csv(csv_file, labels):
    with open(csv_file, 'rt', newline='') as in_file:

        # load the csv into a list and remove the first (header) row
        reader = csv.reader(in_file)
        rows = list(reader)
        rows.pop(0)

        # iterate all rows and create set of unique label names
        for row in rows:
            labels.add(row[3])


def write_pbtxt(out_file, labels):
    lines = []
    label_id = 1
    for label_name in labels:
        lines.append("item {\n")
        lines.append("  id: {}\n".format(label_id))
        lines.append("  name: '{}'\n".format(label_name))
        lines.append("}\n")
        label_id += 1

    with open(out_file, "wt") as out_file:
        out_file.writelines(lines)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--infiles', nargs='+',
                        help='<Required> List of CSV files to extract labels from.', required=True)

    parser.add_argument('-op', '--outpbfile', default='labelmap.pbtxt',
                        help='Output pbtxt filename (default: labelmap.pbtxt).')

    args = parser.parse_args()

    # print(args.infiles)

    # read labels from each csv
    labels = set()
    for file in args.infiles:
        from_csv(file, labels)

    write_pbtxt(args.outpbfile, labels)


main()
