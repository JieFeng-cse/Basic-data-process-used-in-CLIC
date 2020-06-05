'''
@Author: Jie Feng
@Date: 2020-03-15 22:24:51
@LastEditTime: 2020-03-24 21:25:07
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/cal_ssim_bits.py
'''
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from glob import glob
from PIL import Image
import numpy as np
import tensorflow as tf


input_img1 = tf.placeholder(shape=[1, None, None, 1],dtype=tf.float32, name = 'input_img1')
input_img2 = tf.placeholder(shape=[1, None, None, 1],dtype=tf.float32, name = 'input_img2')
ssim_mul = tf.image.ssim_multiscale(input_img1, input_img2, max_val=255)

mode = []
for name in glob("tng_save_*"):
    rate_angle = name.split("save_")[1]
    decode_path = "./recon_image_"+rate_angle
    bin_path = './' + name
    arr = []
    # decode_path = '/home/xiangji/Desktop/model_TL_icn_dc_rev/CLIC_valid/decode_post_'+str(j)
    src_path = '/mnt/Volume1/test/clic_testphase/clic_test/targets'
    # bin_path = '/home/xiangji/Desktop/model_TL_icn_dc_rev/CLIC_valid/tng_post_'+str(j)
    # decode_path = '/mnt/Volume1/test/clic2020-devkit/inputs'
    # src_path = '/mnt/Volume1/test/clic2020-devkit/targets'

    frameNames = sorted(os.listdir(decode_path))
    #frameNames = sorted(os.listdir(src_path))
    totalSSIM  = 0.
    print ("start")
    sess = tf.Session()
    num = 0
    for framName in frameNames:
        if '_y.png' in framName:
            tngName = framName.replace('_y.png','_y.tng')
            tngPath = os.path.join(bin_path,tngName)
            size = os.path.getsize(tngPath) #bytes
            #size = 0

            Pngu_path = os.path.join(src_path, framName.replace('_y.png','_u.png'))
            Pngv_path = os.path.join(src_path, framName.replace('_y.png','_v.png'))
            Pngy_path = os.path.join(src_path, framName)
            print(Pngu_path)
            print(Pngv_path)

            de_pngu_path = os.path.join(decode_path, framName.replace('_y.png','_u.png'))
            de_pngv_path = os.path.join(decode_path, framName.replace('_y.png','_v.png'))
            de_pngy_path = os.path.join(decode_path, framName)
            # de_pngu_path = os.path.join(decode_path, inputname.replace('_y.png','_u.png'))
            # de_pngv_path = os.path.join(decode_path, inputname.replace('_y.png','_v.png'))
            # de_pngy_path = os.path.join(decode_path, inputname)

            print(de_pngv_path)
            
            #U***********************************************************************************************************************************************
            inputPng  = np.array(Image.open(Pngu_path), dtype = np.float32)
            reconPng  = np.array(Image.open(de_pngu_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valu = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})
            
            #V**************************************************************************************************************************************************
            inputPng  = np.array(Image.open(Pngv_path), dtype = np.float32)
            reconPng  = np.array(Image.open(de_pngv_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valv = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})
            
            #Y**************************************************************************************************************************************************

            inputPng  = np.array(Image.open(Pngy_path), dtype = np.float32)
            reconPng  = np.array(Image.open(de_pngy_path), dtype = np.float32)
            ###MS-SSIM###
            inputPng  = np.expand_dims(np.expand_dims(inputPng, axis = 0), axis = -1)
            reconPng  = np.expand_dims(np.expand_dims(reconPng, axis = 0), axis = -1)
            #SSIM      = MultiScaleSSIM(inputPng, reconPng)

            ssim_valy = sess.run(ssim_mul, feed_dict={input_img1:inputPng, input_img2:reconPng})

            ssim = ssim_valu + ssim_valv + ssim_valy*4
            ssim = ssim/6
            print(float(ssim))

            prameter = []
            prameter.append(size)
            prameter.append(float(ssim))
            arr.append(prameter)
    np.save(rate_angle, np.array(arr))
    print(np.array(arr).shape)


