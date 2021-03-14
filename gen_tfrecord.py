# based on https://github.com/datitran/raccoon_dataset/blob/master/generate_tfrecord.py

# adapted to take label map from command line option 'label_map' so
# code doesn't have to be edited for different label sets.
# label file must be csv with two columns ID,LABEL_NAME and no header row.

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from collections import namedtuple, OrderedDict
from object_detection.utils import dataset_util
from PIL import Image
import os
import io
import pandas as pd
import csv

from tensorflow.python.framework.versions import VERSION
if VERSION >= "2.0.0a0":
    import tensorflow.compat.v1 as tf
else:
    import tensorflow as tf

# update to load image label map from file rather than being hard-coded
label_dict = {}

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
flags.DEFINE_string('label_map', '', 'Label map file')
FLAGS = flags.FLAGS


# method updated to use global 'label_dict' populated from file
def class_text_to_int(row_label, label_list):
    if row_label in label_dict:
        return label_dict[row_label]
    else:
        return None
    # if row_label == 'person':
    #     return 1
    # else:
    #     return None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
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
        classes.append(class_text_to_int(row['class']))

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


# loads label map from file
def load_labels(filename):
    # load label list and return a dictionary
    # with label name as key and id as value
    # label file is csv with <id,label> row (no header)
    # (id's must be unique)
    with open(filename, 'rt', newline='') as in_file:
        reader = csv.reader(in_file)
        rows = list(reader)

    # iterate rows and add to dictionary
    for row in rows:
        label_dict[row[1]] = row[0]


def main(_):
    # load label map from file
    load_labels(FLAGS.label_map)

    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
