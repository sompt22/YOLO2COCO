import os.path as osp
import os
import numpy as np

def mkdirs(d):
    if not osp.exists(d):
        os.makedirs(d)

label_root = '/data/yfzhang/MOT/JDE/MOT20/labels_with_ids/train'
seq_root = '/data/yfzhang/MOT/JDE/MOT20/images/train'
mkdirs(seq_root)

seqs = [s for s in os.listdir(label_root)]

for seq in seqs:
    seq_label_root = osp.join(label_root, seq, 'img1')
    gt_txt = osp.join(seq_label_root, 'gt.txt')

    with open(gt_txt, 'r') as f:
        lines = f.readlines()

    mot_gt = []

    for line in lines:
        line = line.strip().split(' ')
        tid = int(line[1])
        x = float(line[2])
        y = float(line[3])
        w = float(line[4])
        h = float(line[5])
        frame_id = int(line[0])
        label = int(line[6])
        mot_gt.append([frame_id, tid, x, y, w, h, label])

    mot_gt = np.asarray(mot_gt)

    seq_info_path = osp.join(seq_root, seq, 'seqinfo.ini')
    seq_info = open(seq_info_path).read()
    seq_width = int(seq_info[seq_info.find('imWidth=') + 8:seq_info.find('\nimHeight')])
    seq_height = int(seq_info[seq_info.find('imHeight=') + 9:seq_info.find('\nimExt')])

    mot_txt = osp.join(seq_root, seq, 'gt', 'gt.txt')
    with open(mot_txt, 'w') as f:
        for i in range(len(mot_gt)):
            frame_id = mot_gt[i][0]
            tid = mot_gt[i][1]
            x = mot_gt[i][2]
            y = mot_gt[i][3]
            w = mot_gt[i][4]
            h = mot_gt[i][5]
            label = mot_gt[i][6]
            if label == 0:
                continue
            x1 = int(x - w / 2.0)
            y1 = int(y - h / 2.0)
            x2 = int(x + w / 2.0)
            y2 = int(y + h / 2.0)
            f.write('{:d},{:d},{:.2f},{:.2f},{:.2f},{:.2f},1,-1,-1,-1\n'.format(
                frame_id, tid, x1, y1, x2-x1, y2-y1))
