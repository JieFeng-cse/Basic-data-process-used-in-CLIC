'''
@Author: your name
@Date: 2020-03-05 03:13:46
@LastEditTime: 2020-03-05 03:52:08
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/read_txt.py
'''
import numpy as np
import os
ssims = []
num = 0
ssim_yuv=0
with open('/mnt/Volume1/test/clic2020-devkit/nonmovement.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        num = num + 1
        ssim = float(line.split(':',4)[3])
        if  not num % 3:
            ssim_yuv =ssim_yuv + ssim*4/6
            ssims.append(ssim_yuv)
            # print(ssim_yuv,line.split(':',4)[1])
            ssim_yuv = 0
        else:
            ssim_yuv = ssim_yuv + ssim/6
            # print(line.split(':',4)[1])

ssims = np.asarray(ssims)
print(ssims.shape)
medi = np.median(ssims)
mean = np.mean(ssims)
hist = np.histogram(ssims,np.array([0. , 0.2, 0.4, 0.6, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 0.994, 0.996, 0.998, 0.9999999,1. ]),range=(0,1))
print("median: ",medi)
print("mean: ",mean)
print("hist: ",hist)

