'''
@Author: your name
@Date: 2020-02-03 09:46:26
@LastEditTime: 2020-03-08 00:17:41
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /Volume0/test/test1.py
'''
#!/usr/bin/env python3
#This file is used to translate pics
import numpy as np
import os
from PIL import Image
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import cv2
import glob

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
        save_root = '/mnt/Volume1/test/rgb_pics'
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
                
                if imy_array.shape[0] != imu_array.shape[0]*2 or imy_array.shape[1] != imu_array.shape[1]*2:
                    print("meet problem!")
                    imy_array = np.pad(imy_array,((0,0),(1,0)), 'constant', constant_values=0)

                method = cv2.INTER_CUBIC
                imu_array = cv2.resize(imu_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)
                imv_array = cv2.resize(imv_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)

                
                #reshape
                imy_array = imy_array.reshape((imy_array.shape[0],imy_array.shape[1],1))
                imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
                imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))

                yuv = np.concatenate([imy_array,imu_array,imv_array], axis = 2)

                rgb = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
                img = Image.fromarray(rgb,'RGB')
                img.save(tmp_dir + '/' + name +"_{:0>5d}".format(i) + '_rgb.png')

# def yuv2rgb(im):
#     """convert array-like yuv image to rgb colourspace

#     a pure numpy implementation since the YCbCr mode in PIL is b0rked. 
#     TODO: port this stuff to a C extension, using lookup tables for speed
#     """
#     ## conflicting definitions exist depending on whether you use the full range
#     ## of YCbCr or clamp out to the valid range. see here
#     ## http://www.equasys.de/colorconversion.html
#     ## http://www.fourcc.org/fccyvrgb.php
#     from numpy import dot, ndarray, array
#     if not im.dtype == 'uint8':
#         raise ImageUtilsError('yuv2rgb only implemented for uint8 arrays')

#     ## better clip input to the valid range just to be on the safe side
#     yuv = ndarray(im.shape) ## float64
#     yuv[:,:, 0] = im[:,:, 0].clip(16, 235).astype(yuv.dtype) - 16
#     yuv[:,:,1:] = im[:,:,1:].clip(16, 240).astype(yuv.dtype) - 128

#     ## ITU-R BT.601 version (SDTV)
#     A = array([[1., 0., 0.701 ],
#     [1., -0.886*0.114/0.587, -0.701*0.299/0.587],
#     [1., 0.886, 0.]])
#     A[:,0] *= 255./219.
#     A[:,1:] *= 255./112.

#     ## ITU-R BT.709 version (HDTV)
#     # A = array([[1.164, 0., 1.793],
#     # [1.164, -0.213, -0.533],
#     # [1.164, 2.112, 0.]])

#     rgb = dot(yuv, A.T)
#     return rgb.clip(0, 255).astype('uint8')

# imy = Image.open('/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_y.png')
# imu = Image.open('/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_u.png')
# imv = Image.open('/mnt/Volume1/test/clic2020-devkit/targets_yuv/Animation_720P-0acc_00006_v.png')
# imy_array = np.asarray(imy)
# # imu_array = np.asarray(imu)
# # imv_array = np.asarray(imv)

# height = imy_array.shape[0]
# width = imy_array.shape[1]
# # method = cv2.INTER_CUBIC
# # imu_array = cv2.resize(imu_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)
# # imv_array = cv2.resize(imv_array, (0, 0), fx=2.0, fy=2.0, interpolation=method)
# method = Image.BICUBIC
# imu = imu.resize((imy.size[0],imy.size[1]), method)
# imv = imv.resize((imy.size[0],imy.size[1]), method) 
# imu_array = np.asarray(imu)
# imv_array = np.asarray(imv)
       
# #reshape
# imy_array = imy_array.reshape((imy_array.shape[0],imy_array.shape[1],1))
# imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
# imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))

# yuv = np.concatenate([imy_array,imu_array,imv_array], axis = 2)
# yuv = Image.fromarray(yuv,'YCbCr')
# rgb = yuv.convert('RGB')
# #rgb = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
# #img = Image.fromarray(rgb,'RGB')
# img = rgb
# img.save('/mnt/Volume1/test/hh_rgb.png')



