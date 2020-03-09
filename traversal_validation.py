'''
@Author: Feng Jie
@Date: 2020-02-10 05:23:41
@LastEditTime: 2020-02-26 00:12:29
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/traversal_validation.py
'''
#!/usr/bin/env python3
import numpy as np
import os
from PIL import Image
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import cv2
import glob

# size_count = {}
for root1, dirs1, files1 in os.walk("/mnt/Volume0/test/ttttest", topdown = False):
    for name1 in sorted(dirs1):
        str_dir = os.path.join(root1,name1)
        for root, dirs, files in os.walk(str_dir, topdown = False):
            for name in sorted(files):
                newname = name1 + '_' + name
                str_path = os.path.join(str_dir,name)
                newstr_path = os.path.join(str_dir,newname)
                #print(str_path)
                #print(newstr_path)
                os.rename(str_path,newstr_path)

# for root1, dirs1, files1 in os.walk("/mnt/Volume0/test/merge_yuv", topdown = False):
#     for name1 in sorted(dirs1):
#         for name2 in sorted(files1):
#             str_path = os.path.join(root1, name1)
#             st_path = os.path.join(root1,name2)
#             newstr_path = os.path.join(str_path, name2)
#             os.rename(st_path,newstr_path)
        



# print(size_count)
# print('filenum:',len([lists for lists in os.listdir(path) ]))
# for root, dirs, files in os.walk("/mnt/Volume0/test/rgb_pics", topdown = False):
#     for name in dirs:
#         str_path = os.path.join("/mnt/Volume0/test/rgb_pics",name)
#         listt = os.listdir(str_path)
#         num = len(listt)
#         if num < 20:
#             print(name)
# str_path = '/mnt/Volume0/clic_P_frame/dataset/Vlog_2160P-7295'
# tmp_dir = '/mnt/Volume0/test/rgb_pics/Vlog_2160P-7295'
# for root, dirs, files in os.walk(str_path):
#     str_files = os.path.join(str_path,files[0])
#     length = len(files)
#     length = length  / 3
#     length = int(length)
#     for i in range(1,length+1,1):

#         str_filesy = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_y.png'
#         str_filesu = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_u.png'
#         str_filesv = str_files[0:len(str_files)-11] + "{:0>5d}".format(i) + '_v.png'
#         imy = Image.open(str_filesy)
#         imu = Image.open(str_filesu)
#         imv = Image.open(str_filesv)
#         imy_array = np.asarray(imy)
#         imu_array = np.asarray(imu)
#         imv_array = np.asarray(imv)
#         imy_array = np.pad(imy_array,((0,0),(1,0)), 'constant', constant_values=0)

#         print(imy_array.shape)
#         height = imy_array.shape[0]
#         width = imy_array.shape[1]

#         imv_array = ndimage.zoom(imv_array,2,order = 0)
#         imu_array = ndimage.zoom(imu_array,2,order = 0)
#         #reshape
#         imy_array = imy_array.reshape((imy_array.shape[0],imy_array.shape[1],1))
#         imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
#         imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))

#         yuv = np.concatenate([imy_array,imu_array,imv_array], axis = 2)

#         rgb = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
#         img = Image.fromarray(rgb,'RGB')
#         img.save(tmp_dir + '/'+"{:0>5d}".format(i) + '_rgb.png')

           
        