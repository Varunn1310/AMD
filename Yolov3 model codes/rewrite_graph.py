import tensorflow.compat.v1 as tf
sess = tf.Session()

def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
    return graph

graph = load_graph("yolov3_voc.pb")
graph_def = graph.as_graph_def()
# if ReLu op is at node 161
#input_x = sess.graph.get_tensor_by_name('leaky_re_lu_1/LeakyRelu' + ':0').op="relu"
for n in graph_def.node:
  if 'LeakyRelu' in n.name:
    n.op='Relu'
    n.attr.pop('alpha')
tf.train.write_graph(graph_def, "/home/mcw/Desktop/TF_v2.10_ZenDNN_v4.0_Python_v3.9/tf_yolov3_voc_416_416_65.63G_3.0/code/test/", "altered_yolov3.pb", False)
