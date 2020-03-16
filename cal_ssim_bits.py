'''
@Author: Jie Feng
@Date: 2020-03-15 22:24:51
@LastEditTime: 2020-03-15 23:24:52
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/cal_ssim_bits.py
'''
import os
import glob
from PIL import Image
import numpy as np
import pframe_dataset_shared
import tensorflow as tf


input_img1 = tf.placeholder(shape=[1, None, None, 1],dtype=tf.float32, name = 'input_img1')
input_img2 = tf.placeholder(shape=[1, None, None, 1],dtype=tf.float32, name = 'input_img2')
ssim_mul = tf.image.ssim_multiscale(input_img1, input_img2, max_val=255)

mode = []
for j in range(5):
    print(j)
    arr = []
    decode_path = '/mnt/Volume1/test/clic2020-devkit/tng_m/tng_'+ str(j) +'_result'
    src_path = '/mnt/Volume1/test/clic2020-devkit/targets'
    bin_path = '/mnt/Volume1/test/clic2020-devkit/tng_m/tng' + str(j)

    frameNames = sorted(os.listdir(decode_path))
    totalSSIM  = 0.
    print ("start")
    sess = tf.Session()
    num = 0
    for framName in frameNames:
        if '_y.png' in framName:
            tngName = framName.replace('_y.png','_y.tng')
            tngPath = os.path.join(bin_path,tngName)
            size = os.path.getsize(tngPath) #bytes

            Pngu_path = os.path.join(src_path, framName.repalce('_y.png','_u.png'))
            Pngv_path = os.path.join(src_path, framName.repalce('_y.png','_v.png'))
            Pngy_path = os.path.join(src_path, framName)
            print(Pngu_path)
            print(Pngv_path)

            de_pngu_path = os.path.join(decode_path, framName.repalce('_y.png','_u.png'))
            de_pngv_path = os.path.join(decode_path, framName.repalce('_y.png','_v.png'))
            de_pngy_path = os.path.join(decode_path, framName)
            print(de_pngv_path)
            
            #U***********************************************************************************************************************************************
            inputPng  = np.array(Pngu_path), dtype = np.float32)
            reconPng  = np.array(de_pngu_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valu = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})
            
            #V**************************************************************************************************************************************************
            inputPng  = np.array(Pngv_path), dtype = np.float32)
            reconPng  = np.array(de_pngv_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valv = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})
            
            #Y**************************************************************************************************************************************************

            inputPng  = np.array(Pngy_path), dtype = np.float32)
            reconPng  = np.array(de_pngy_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valy = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})

            ssim = ssim_valu + ssim_valv + ssim_valy*4
            ssim = ssim/6
            print(ssim)

            prameter = []
            prameter.append(size)
            prameter.append(ssim)
            arr.append(prameter)
    mode.append(arr)
np.save("/mnt/Volume1/test/clic2020-devkit/data_tng.npy", np.array(mode))




