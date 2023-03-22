# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# MIT License
#
# Copyright (c) 2018 qqwweee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import cv2
import numpy as np
from tqdm import tqdm
import tensorflow.compat.v1 as tf
import time
from yolo3_predictor import yolo_predictor
from config import Yolov3VOCConfig as Config
tf.disable_v2_behavior()

tf.app.flags.DEFINE_string('input_graph', '../float_model/yolov3_voc.pb',
                           'TensorFlow \'GraphDef\' file to load.')
tf.app.flags.DEFINE_string('eval_image_path', '',
                           'The directory where put the eval images')
tf.app.flags.DEFINE_string('eval_image_list', '',
                           'file has validation images list')
tf.app.flags.DEFINE_string('input_node', 'input_1', 'input node of pb model')
tf.app.flags.DEFINE_string(
    'output_node', 'conv2d_59/BiasAdd,conv2d_67/BiasAdd,conv2d_75/BiasAdd',
    'ouput node of pb model')
tf.app.flags.DEFINE_integer('input_height', 416, 'input height of pb model')
tf.app.flags.DEFINE_integer('input_width', 416, 'input width of pb model')
tf.app.flags.DEFINE_string('result_file', 'voc2007_pred_results.txt',
                           'The directory of output results')
tf.app.flags.DEFINE_boolean('use_quantize', False, 'quantize or not')
tf.app.flags.DEFINE_string('gpus', '0',
                           'The gpus used for running evaluation.')

FLAGS = tf.app.flags.FLAGS
os.environ['CUDA_VISIBLE_DEVICES'] = FLAGS.gpus
time_consume = 0
latency = 0

if FLAGS.use_quantize:
    from tensorflow.contrib import decent_q

def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    ih, iw, _ = image.shape
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = cv2.resize(image, (nw,nh), interpolation=cv2.INTER_LINEAR)
    new_image = np.ones((h,w,3), np.uint8) * 128
    h_start = (h-nh)//2
    w_start = (w-nw)//2
    new_image[h_start:h_start+nh, w_start:w_start+nw, :] = image
    return new_image


def write_items_to_file(image_id, items, fw):
    for item in items:
        fw.write(image_id + " " + " ".join([str(comp) for comp in item]) + "\n")


def get_detection(image, model_image_size, class_names):
    image_h, image_w, _ = image.shape
    #print('Mdel Image size :',model_image_size)
    #print('IMage height :',image_h)
    #print('IMage width :',image_w)
    # image preprocessing
    if model_image_size != (None, None):
        assert model_image_size[0]%32 == 0, 'Multiples of 32 required'
        assert model_image_size[1]%32 == 0, 'Multiples of 32 required'
        #res_tuple = tuple(32)+tuple(reversed(model_image_size))
        #print('tuple reverse size :',res_tuple)
        boxed_image = letterbox_image(image, tuple(reversed(model_image_size)))
    else:
        new_image_size = (image_w - (image_w % 32), image_h - (image_h % 32))
        boxed_image = letterbox_image(image, new_image_size)
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    #print('Input shape: ',image_data.shape)
    #print('IMage.shape: ',image.shape)
    start_time = time.time()
    out_boxes, out_scores, out_classes, out_y = sess.run(
        [pred_boxes, pred_scores, pred_classes, output_y],
        feed_dict={input_x: image_data, input_image_shape: (image_h, image_w)})
    global time_consume
    global latency
    latency = time.time() - start_time 
    time_consume += time.time() - start_time

    # convert the result to label format
    items = []
    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]
        box = out_boxes[i]
        score = out_scores[i]

        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image_h, np.floor(bottom + 0.5).astype('int32'))
        right = min(image_w, np.floor(right + 0.5).astype('int32'))
        item  = [predicted_class, score, left, top, right, bottom]
        items.append(item)

    return items


if __name__ == "__main__":

    config = Config()
    class_names = config.classes
    predictor = yolo_predictor(config)
    sess = tf.compat.v1.Session()
    with tf.io.gfile.GFile(FLAGS.input_graph, 'rb') as f: # file I/O
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read()) # get graph_def from file
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')  # import graph
    sess.run(tf.compat.v1.global_variables_initializer())

    input_x = sess.graph.get_tensor_by_name(FLAGS.input_node + ':0')
    output_y = []
    for node in FLAGS.output_node.split(","):
        output_y.append(sess.graph.get_tensor_by_name(node + ":0"))

    input_image_shape = tf.compat.v1.placeholder(tf.int32, shape=(2))
    pred_boxes, pred_scores, pred_classes = predictor.predict(output_y, input_image_shape)
    iterations = 0

    with open(FLAGS.eval_image_list) as fr:
        lines = fr.readlines()
    fw = open(FLAGS.result_file, "w")
    for line in tqdm(lines):
        img_id = line.strip()
        img_path = os.path.join(FLAGS.eval_image_path, img_id + '.jpg')
        image = cv2.imread(img_path)
        image = image[...,::-1] # BGR -> RGB
        # items = get_detection(image, (config.height, config.width), class_names)
        #print('Main IMg shape :',image.shape)
        items = get_detection(image, (FLAGS.input_height, FLAGS.input_width), class_names)
        iterations+=1
        write_items_to_file(img_id, items, fw)
    print('============PERFORMANCE RESULTS======================')
    print("Latency :",latency,"s")
    print("Throughput :",iterations/time_consume)
    print('=====================================================')
    fw.close()
