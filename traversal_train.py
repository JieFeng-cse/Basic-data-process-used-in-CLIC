'''
@Author: your name
@Date: 2020-02-21 20:59:51
@LastEditTime: 2020-03-05 05:01:25
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /Volume0/test/clic2020-devkit/traversal_train.py
'''
import numpy as np
import os
from PIL import Image
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import cv2
import glob
import pframe_dataset_shared

from ms_ssim_np import MultiScaleSSIM


# summ = 0
# for root, dirs, files in os.walk("/mnt/Volume0/clic_P_clic_new", topdown = False):
#     for name in dirs:
#         str_path = os.path.join(root,name)
#         for root2,dirs1,files1 in os.walk(str_path,topdown=False):
#             for name1 in files1:
#                 summ = summ + 1
#         #print(str_path)
#         #summ = summ + len(str(files1))
# print(summ)

# with open('/mnt/Volume0/clic_P_clic_new/pframe_video_urls.txt.1','r') as r:
#     lines=r.readlines()
# flag = 0
# with open('/mnt/Volume0/clic_P_clic_new/pframe_video_urls.txt','w') as w:
#     for l in lines:
#         flag = 0
#         for root, dirs, files in os.walk("/mnt/Volume0/clic_P_clic_new", topdown = False):
#             for name in dirs:
#                 #print(name)
#                 if name in l:
#                     flag = 1
                    
#                     break
#         if flag == 0:
#             print("hh,gotcha")
#             w.write(l)
# str_filesy = '/mnt/Volume1/test/clic2020-devkit/result/Animation_720P-0acc_00006_u.png'
# str_filesyy = '/mnt/Volume1/test/clic2020-devkit/targets/Animation_720P-0acc_00006_u.png'
# str_filesu = '/mnt/Volume1/test/clic2020-devkit/result/Animation_720P-0acc_00006_u.png'
# str_filesv = '/mnt/Volume1/test/clic2020-devkit/result/Animation_720P-0acc_00006_v.png'
# imy = Image.open(str_filesy)
# imyy = Image.open(str_filesyy)

# imu = Image.open(str_filesu)
# imv = Image.open(str_filesv)
# imy_array = np.asarray(imy)
# imyy_array = np.asarray(imyy)

# imu_array = np.asarray(imu)
# imv_array = np.asarray(imv)
# imy_array = imy_array.reshape((1,imy_array.shape[0],imy_array.shape[1],1))
# imyy_array = imyy_array.reshape((1,imyy_array.shape[0],imyy_array.shape[1],1))
# imu_array = imu_array.reshape((imu_array.shape[0],imu_array.shape[1],1))
# imv_array = imv_array.reshape((imv_array.shape[0],imv_array.shape[1],1))
# yuv = np.concatenate([imy_array,imy_array,imy_array], axis = 2)
# yuv1 = np.concatenate([imyy_array,imyy_array,imyy_array], axis = 2)

# score = MultiScaleSSIM(yuv,yuv1)
# print("score",score)

#old mssim calculater.
# mssim = 0
# number = 0
# f = open('/mnt/Volume1/test/clic2020-devkit/nonmovement.txt','r')
# data = f.readlines()
# for root, dirs, files in os.walk("/mnt/Volume1/test/clic2020-devkit/targets_yuv", topdown = False):
#     for i,name in enumerate(sorted(files)):
#         assert name in data[i]
#         score_nochange = float(data[i].split(':',4)[3]) 
#         str_file_result = os.path.join(root,name)
#         p2 = pframe_dataset_shared.get_previous_frame_path(name)
         
#         print(name)
#         print(p2)
#         str_file_target = os.path.join("/mnt/Volume1/test/clic2020-devkit/inputs_yuv",p2)

#         im_re = Image.open(str_file_result)
#         im_ta = Image.open(str_file_target)

#         im_re_arr = np.asarray(im_re)
#         im_ta_arr = np.asarray(im_ta)

#         im_re_arr = im_re_arr.reshape((1,im_re_arr.shape[0],im_re_arr.shape[1],1))
#         im_ta_arr = im_ta_arr.reshape((1,im_ta_arr.shape[0],im_ta_arr.shape[1],1))
        
#         yuv = np.concatenate([im_re_arr,im_re_arr,im_re_arr], axis = 3)
#         yuv1 = np.concatenate([im_ta_arr,im_ta_arr,im_ta_arr], axis = 3)
#         score = MultiScaleSSIM(yuv,yuv1)
#         if np.isnan(score):
#             print(str_file_result)
#             score = 0
#         print(score)
#         str_w = 'input:' + p2+'; '+ 'target: ' + name + '; ' + 'ssim: ' + str(score)+ '\n'
#         if '_y.png' in name:
#             score = score * 4
#         mssim = score + mssim
#         number = number + 1
#         print(number)
#         #print(mssim)
# print(number)
# mssim = (mssim/number)/2
# print(mssim)
# f.close()

mssim = 0
mssim1 = 0
number = 0
f = open('/mnt/Volume1/test/clic2020-devkit/nonmovement.txt','r')
data = f.readlines()
ssim_yuv = 0
ssim_tng = 0
bpp1 = 0#without using nonchange
bpp2 = 0 #use nonchange
tmp = 0
ssims = np.zeros((3,1))
for root, dirs, files in os.walk("/mnt/Volume1/test/clic2020-devkit/targets_yuv", topdown = False):
    for i,name in enumerate(sorted(files)):
        assert name in data[i]
        
        str_file_result = os.path.join(root,name)
        #p2 = pframe_dataset_shared.get_previous_frame_path(name)
         
        str_file_target = os.path.join("/mnt/Volume1/test/clic2020-devkit/yuv_result",name)
        str_mid =os.path.join('/mnt/Volume1/test/clic2020-devkit/tng_save',name[:-5]+'rgb.tng')

        im_re = Image.open(str_file_result)
        im_ta = Image.open(str_file_target)

        im_re_arr = np.asarray(im_re)
        im_ta_arr = np.asarray(im_ta)

        im_re_arr = im_re_arr.reshape((1,im_re_arr.shape[0],im_re_arr.shape[1],1))
        im_ta_arr = im_ta_arr.reshape((1,im_ta_arr.shape[0],im_ta_arr.shape[1],1))
        
        yuv = np.concatenate([im_re_arr,im_re_arr,im_re_arr], axis = 3)
        yuv1 = np.concatenate([im_ta_arr,im_ta_arr,im_ta_arr], axis = 3)
        score = MultiScaleSSIM(yuv,yuv1)
        if np.isnan(score):
            print(str_file_result)
            score = 0
        #print(score)
        #str_w = 'input:' + p2+'; '+ 'target: ' + name + '; ' + 'ssim: ' + str(score)+ '\n'
        
        score_nochange = float(data[i].split(':',4)[3]) 
        ssims[i%3]=score_nochange
        size = os.path.getsize(str_mid)
        #print("size",size)
        if not (i+1)%3:
            tmp = tmp + size
            ssim_tng = ssim_tng + score * 4
            ssim_yuv = ssim_yuv + score_nochange*4
            # print("tng",ssim_tng)
            # print("yuv",ssim_yuv)
            # print(i,"bpp3",tmp)
            bpp1 = bpp1 + tmp
            if ssim_tng < ssim_yuv:
                mssim1 = ssim_yuv + mssim1
                mssim = ssim_tng + mssim
            else:
                mssim1 = ssim_tng + mssim1
                mssim = ssim_tng + mssim
                bpp2 = bpp2 + tmp
            ssim_tng = 0
            ssim_yuv = 0
            tmp = 0
            print("bpp1: ",bpp1," bpp2: ",bpp2)
            print("ssim1: ", mssim, "ssim2: ", mssim1)
        else:
            #print(i,"bpp",tmp)
            ssim_yuv = ssim_yuv + score_nochange
            ssim_tng = ssim_tng + score
        
        number = number + 1
        print(number)
        #print(mssim)
print(number)
mssim = (mssim/number)/2
mssim1 = (mssim1/number)/2
print("all tng: ","1.ssim: ",mssim,"2.bpp: ",bpp1)
print("all tng: ","1.ssim: ",mssim1,"2.bpp: ",bpp2)
f.close()



