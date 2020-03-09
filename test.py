'''
@Author: your name
@Date: 2020-03-04 09:56:51
@LastEditTime: 2020-03-07 01:03:37
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/test.py
'''
#this code used for transpose rgb back to yuv
import numpy as np
import os
from PIL import Image
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import cv2
import glob

# str_filesy = '/mnt/Volume1/test/clic2020-devkit/inputs_yuv/Animation_720P-0acc_00005_y.png'
# str_filesu = '/mnt/Volume1/test/clic2020-devkit/inputs_yuv/Animation_720P-0acc_00005_u.png'
# str_filesv = '/mnt/Volume1/test/clic2020-devkit/inputs_yuv/Animation_720P-0acc_00005_v.png'
                
# imy = Image.open(str_filesy)
# imu = Image.open(str_filesu)
# imv = Image.open(str_filesv)
# imy_array = np.asarray(imy)
# imu_array = np.asarray(imu)
# imv_array = np.asarray(imv)

# height = imy_array.shape[0]
# width = imy_array.shape[1]
                
# if imy_array.shape[0] != imu_array.shape[0]*2 or imy_array.shape[1] != imu_array.shape[1]*2:
#     print("meet problem!")
#     imy_array = np.pad(imy_array,((0,0),(1,0)), 'constant', constant_values=0)

# method = cv2.INTER_NEAREST
# imu_array = cv2.resize(imu_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)
# imv_array = cv2.resize(imv_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)

                
# #reshape
# imy_array = imy_array.reshape((imy_array.shape[0],imy_array.shape[1],1))
# imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
# imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))

# yuv = np.concatenate([imy_array,imu_array,imv_array], axis = 2)

# rgb = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
# img = Image.fromarray(rgb,'RGB')
# img.save('/mnt/Volume1/test/clic2020-devkit/rgb1.png')
for root, dirs, files in os.walk("/mnt/Volume1/test/clic2020-devkit/tng_result", topdown = False):
    for name in files:
        path = os.path.join(root,name)
        # save_path = '/mnt/Volume1/test/clic2020-devkit/yuv_result'
        save_path = '/mnt/Volume1/test'
        print(name)
        img = Image.open(path)
        img_yuv = img.convert('YCbCr')
        y,u,v = Image.Image.split(img_yuv)
        method = Image.BICUBIC
        print(y.size)
        u = u.resize((y.size[0]//2,y.size[1]//2), method)
        v = v.resize((y.size[0]//2,y.size[1]//2), method)
        print(u.size)
        if 'Gaming_2160P-2b92' in name \
            or 'Lecture_1080P-4991' in name \
                or 'Vlog_2160P-266c' in name \
                    or 'Vlog_2160P-26ef' in name \
                        or 'Vlog_2160P-2b61' in name \
                            or 'Vlog_2160P-6bf1' in name \
                                or 'Vlog_2160P-7295' in name:
                                y = np.asarray(y)
                                y = np.delete(y, -1, axis=1)
                                y = Image.fromarray(y)

        namey = os.path.basename(path).replace('_rgb.png','_y.png')
        nameu = os.path.basename(path).replace('_rgb.png','_u.png')
        namev = os.path.basename(path).replace('_rgb.png','_v.png')

        save_y = os.path.join(save_path,namey)
        save_u = os.path.join(save_path,nameu)
        save_v = os.path.join(save_path,namev)

        y.save(save_y)
        u.save(save_u)
        v.save(save_v)
        exit(0)
    




