def compute_detection_ap(results, gts, thresh, overlap_thresh, use_07_metric=False):
    """
    Evaluate detection results
    :param results: image_name class_label score xmin ymin xmax ymax
    :param gts: image_name class_label xmin ymin xmax ymax
    :param thresh: only bboxes whose confidence score under thresh are used
    :param overlap_thresh: threshold of IOU ratio to determine a match bbox
    :param use_07_metric: uses the VOC 07 11 point method to compute VOC AP given precision and recall
    :return: recall, precision, ap
    """
    # load gt
    class_gts = {}
    class_num_positive = {}
    image_names = set()
    for gt in gts:
        gt_info = gt.split(' ')
        if len(gt_info) != 6 and len(gt_info) != 7:
            print('wrong ground truth info: ' + gt_info[0])
            return 0
        image_name = gt_info[0]
        class_name = gt_info[1]
        bbox = [float(item) for item in gt_info[2:6]]
        if len(gt_info) == 6:
            difficult = False
        else:
            difficult = bool(int(gt_info[-1]))

        if class_name not in class_gts.keys():
            class_gts[class_name] = {}
            class_num_positive[class_name] = 0
        if image_name not in class_gts[class_name].keys():
            class_gts[class_name][image_name] = {'bbox': np.array([bbox]),
                                                 'hit': [False],
                                                 'difficult': [difficult]}
        else:
            class_gts[class_name][image_name]['bbox'] = np.vstack((class_gts[class_name][image_name]['bbox'],
                                                                   np.array(bbox)))
            class_gts[class_name][image_name]['hit'].append(False)
            class_gts[class_name][image_name]['difficult'].append(difficult)
        class_num_positive[class_name] += int(True ^ difficult)
        image_names.add(image_name)
    class_names = class_gts.keys()

    # read dets
    class_dets = {}
    for result in results:
        result_info = result.split(' ')
        if len(result_info) != 7:
            print('wrong detections info: ' + result_info[0])
            return 0
        image_name = result_info[0]
        class_name = result_info[1]
        bbox = [float(item) for item in result_info[2:]]
        if bbox[0] <= thresh:
            continue
        if class_name not in class_names:
            continue
        if class_name not in class_dets.keys():
            class_dets[class_name] = {'images': [],
                                      'scores': [],
                                      'bboxes': []}
        class_dets[class_name]['images'].append(image_name)
        class_dets[class_name]['scores'].append(bbox[0])
        class_dets[class_name]['bboxes'].append(bbox[1:])

    ap = {}
    precision = {}
    recall = {}
    count = 0
    start=time.time()
    for class_name in class_names:
        if class_name not in class_dets.keys():
            ap[class_name] = 0
            recall[class_name] = 0
            precision[class_name] = 0
            continue

        gt_images = class_gts[class_name]
        num_positive = class_num_positive[class_name]

        det_images = class_dets[class_name]['images']
        det_scores = np.array(class_dets[class_name]['scores'])
        det_bboxes = np.array(class_dets[class_name]['bboxes'])

        # sort by confidence
        sorted_index = np.argsort(-det_scores)
        det_bboxes = det_bboxes[sorted_index, :]
        det_images = [det_images[x] for x in sorted_index]

        # go down dets and mark TPs and FPs
        num_dets = len(det_images)
        true_positive = np.zeros(num_dets)
        false_positive = np.zeros(num_dets)
        for idx in range(num_dets):
            if det_images[idx] not in gt_images.keys():
                false_positive[idx] = 1
                continue

            gt_bboxes = gt_images[det_images[idx]]['bbox'].astype(float)
            gt_hit = gt_images[det_images[idx]]['hit']
            git_difficult = gt_images[det_images[idx]]['difficult']
            det_bbox = det_bboxes[idx, :].astype(float)
            overlaps_max = -np.inf

            if gt_bboxes.size > 0:
                # compute overlaps
                # intersection
                inter_xmin = np.maximum(gt_bboxes[:, 0], det_bbox[0])
                inter_ymin = np.maximum(gt_bboxes[:, 1], det_bbox[1])
                inter_xmax = np.minimum(gt_bboxes[:, 2], det_bbox[2])
                inter_ymax = np.minimum(gt_bboxes[:, 3], det_bbox[3])
                inter_width = np.maximum(inter_xmax - inter_xmin + 1., 0.)
                inter_height = np.maximum(inter_ymax - inter_ymin + 1., 0.)
                inters = inter_width * inter_height

                # union
                unions = ((det_bbox[2] - det_bbox[0] + 1.) * (det_bbox[3] - det_bbox[1] + 1.) +
                          (gt_bboxes[:, 2] - gt_bboxes[:, 0] + 1.) * (gt_bboxes[:, 3] - gt_bboxes[:, 1] + 1.) - inters)

                overlaps = inters / unions
                overlaps_max = np.max(overlaps)
                jmax = np.argmax(overlaps)

            if overlaps_max > overlap_thresh:
                if not git_difficult[jmax]:
                    if not gt_hit[jmax]:
                        true_positive[idx] = 1.
                        gt_hit[jmax] = 1
                    else:
                        false_positive[idx] = 1.
            else:
                false_positive[idx] = 1.
            count+=1

        # compute precision recall
        false_positive = np.cumsum(false_positive)
        true_positive = np.cumsum(true_positive)
        recall[class_name] = true_positive / float(num_positive)
        precision[class_name] = true_positive / np.maximum(true_positive + false_positive, np.finfo(np.float64).eps)
        ap[class_name] = voc_ap(recall[class_name], precision[class_name], use_07_metric)
    end=time.time()
    throughput = count*len(class_names)/(end-start)
    print('evaluate ' + str(len(image_names)) + ' images')
    print('============PERFORMANCE RESULTS======================')
    print('Latency is {:.4f}s'.format(end-start))
    print('Throughput is {:.4f}'.format(throughput))
    print('=====================================================')
    return recall, precision, ap

