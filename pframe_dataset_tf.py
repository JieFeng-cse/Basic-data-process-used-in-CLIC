'''
@Author: your name
@Date: 2020-03-03 05:21:35
@LastEditTime: 2020-03-04 08:44:03
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/pframe_dataset_tf.py
'''
import pframe_dataset_shared
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import cv2
import glob



def frame_sequence_dataset(data_root, merge_channels=False, num_frames_per_sequence=2):
    """
    Create a tf.data.Dataset that yields sequences of `num_frames` frames, e.g.:
        first element:  ( (f11_y, f11_u, f11_v), (f12_y, f12_u, f12_v) ),  # tuple for video 1, frame 1, 2
        second element: ( (f12_y, f12_u, f12_v), (f13_y, f13_u, f13_v) ),  # tuple for video 1, frame 2, 3

    If merge_channels=True, the channels are merged into one tensor, yielding
        first element:  ( f11, f12 ),  # for video 1, frame 1, 2
        second element: ( f12, f13 ),  # for video 1, frame 2, 3

    Dataformat is always HWC, and dtype is uint8, output is in {0, ..., 127} (non-normalized).
    """
    tuple_ps = pframe_dataset_shared.get_paths_for_frame_sequences(data_root, num_frames_per_sequence)
    tuple_ps = tf.constant(tuple_ps)
    d = tf.data.Dataset.from_tensor_slices(tuple_ps)
    d = d.map(load_frames)
    if merge_channels:
        d = d.map(merge_channels_per_frame)
    return d


def load_frames(ps):
    # Unpack ps = ((f11_y, f11_u, f11_v), (f12_y, f12_u, f12_v))
    return tuple(tuple(load_frame(p) for p in tf.unstack(frames))
                 for frames in tf.unstack(ps))


def load_frame(p):
    img = tf.image.decode_png(tf.io.read_file(p))
    img = tf.ensure_shape(img, (None, None, 1))
    # img.set_sh = (None, None, 1)
    return img


def merge_channels_per_frame(*frames):
    return tuple(yuv_420_to_444(y, u, v) for y, u, v in frames)


def yuv_420_to_444(y, u, v):
    """ Convert Y, U, V, given in 420, to RGB 444. """
    target_shape = tf.shape(y)[:2]  # Get H, W
    u = _upsample_nearest_neighbor(u, target_shape)
    v = _upsample_nearest_neighbor(v, target_shape)
    return tf.concat([y, u, v], -1)                 # merge


def _upsample_nearest_neighbor(t, target_shape):
    """ Upsample tensor `t`, given in H,W,C, to shape `target_shape`. """
    return tf.image.resize(
        t, target_shape, method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print("Path exists")
        return False

for root, dirs, files in os.walk("/mnt/Volume1/clic_P_frame/dataset", topdown = False):
    for name in sorted(dirs):
        str_path = os.path.join(root,name)
        save_root = '/mnt/Volume1/test/yuv444'
        tmp_dir = os.path.join(save_root,name)
        made = mkdir(tmp_dir)
        if made == False:
            continue
        print(name)
        i = 0
        for root1, dirs1, files1 in os.walk(str_path):
            str_files = os.path.join(str_path,files1[0])
            length = len(files1)
            length = length  / 3
            length = int(length)
            for i in range(1,length+1,1):
                
                str_filesy = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_y.png'
                str_filesu = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_u.png'
                str_filesv = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_v.png'
                
                imy = Image.open(str_filesy)
                imu = Image.open(str_filesu)
                imv = Image.open(str_filesv)
                imy_array = np.asarray(imy)
                imu_array = np.asarray(imu)
                imv_array = np.asarray(imv)

                height = imy_array.shape[0]
                width = imy_array.shape[1]
                
                # if imy_array.shape[0] != imu_array.shape[0]*2 or imy_array.shape[1] != imu_array.shape[1]*2:
                #     print("meet problem!")
                #     imy_array = np.pad(imy_array,((0,0),(1,0)), 'constant', constant_values=0)

                method = cv2.INTER_NEAREST
                imu_array = cv2.resize(imu_array, (imy_array.shape[1],imy_array.shape[0]), interpolation=method)
                imv_array = cv2.resize(imv_array, (imy_array.shape[1],imy_array.shape[0]), interpolation=method)

                #reshape
                imy_array = imy_array.reshape((imy_array.shape[0],imy_array.shape[1],1))
                imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
                imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))
                # print(imu_array.shape)
                # print(imv_array.shape)
                # print(imy_array.shape)

                yuv = np.concatenate([imy_array,imu_array,imv_array], axis = 2)

                #rgb = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
                img = Image.fromarray(yuv,'RGB')
                img.save(tmp_dir + '/' + name +"_{:0>5d}".format(i) + '_yuv.png')


# def main():
#     pathu = '/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_u.png'
#     pathv = '/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_v.png'
#     pathy = '/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_y.png'
#     y = load_frame(pathy)
#     u = load_frame(pathu)
#     v = load_frame(pathv)

#     img = yuv_420_to_444(y, u, v)
    
#     with tf.Graph().as_default():
#         y = load_frame(pathy)
#         u = load_frame(pathu)
#         v = load_frame(pathv)

#         img = yuv_420_to_444(y, u, v)
#         init = tf.initialize_all_variables()
#         sess = tf.Session()
#         sess.run(init)
#         tf.train.start_queue_runners(sess=sess)
        
#         img = sess.run(img)
#         img = Image.fromarray(img, "RGB")
#         img.save('/mnt/Volume1/test/woc1.png')






# if __name__ == '__main__':
#     main()