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


GPUS=0
BATCH_SIZE=1
WEIGHTS=float/yolov3_voc.pb
SUB_DATA=data/voc2007_test
IMG_DIR=${SUB_DATA}/images
TEST_LIST=${SUB_DATA}/test.txt
GT_FILE=${SUB_DATA}/gt_detection.txt
RESULT_FILE=data/dt_detection.txt

python code/test/tf_prediction_upgraded.py \
    --batch_size ${BATCH_SIZE} \
    --input_graph ${WEIGHTS} \
    --eval_image_path ${IMG_DIR} \
    --eval_image_list ${TEST_LIST} \
    --result_file ${RESULT_FILE} \
    --gpus ${GPUS} \
