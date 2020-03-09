'''
@Author: Jie Feng
@Date: 2020-03-08 00:06:54
@LastEditTime: 2020-03-08 04:15:21
@LastEditors: Please set LastEditors
@Description: Use this script to get mse for nearby pics
@FilePath: /test/clic2020-devkit/get_mse_record.py
'''
import numpy as np
from PIL import Image
import os

def mse(image0, image1):
	return np.mean(np.square(image1 - image0))

# img1 = Image.open('/mnt/Volume1/test/rgb_pics/Animation_720P-0acc/Animation_720P-0acc_00001_rgb.png')
# img2 = Image.open('/mnt/Volume1/test/rgb_pics/Animation_720P-0acc/Animation_720P-0acc_00002_rgb.png')

# img1_ar = np.asarray(img1)
# img2_ar = np.asarray(img2)
# print(mse(img1_ar,img2_ar))
flag = False
f = open('/mnt/Volume1/test/clic2020-devkit/mse.txt','a')
for root, dirs, files in os.walk("/mnt/Volume1/test/rgb_pics", topdown = False):
    for name in sorted(dirs):
        if name == 'Gaming_720P-493e':
            flag = True
        if flag == False:
            print("done!")
            continue
        str_path = os.path.join(root,name)
        files1 = os.listdir(str_path)
        str_files = os.path.join(str_path,files1[0])
        length = len(files1)
        print(name)
        f.write(name+'\n')
        for i in range(1,length,1):
            
            str_files_f = str_files[0:len(str_files)-13] + "{:0>5d}".format(i) + '_rgb.png'
            str_files_n = str_files[0:len(str_files)-13] + "{:0>5d}".format(i+1) + '_rgb.png'
            imf = Image.open(str_files_f)
            imn = Image.open(str_files_n)

            imf_array = np.asarray(imf)
            imn_array = np.asarray(imn)

            mse_v = mse(imf_array,imn_array)
            f.write(name + ':'+'%d and %d, with mse: %f'%(i,i+1,mse_v)+'\n')
f.close()
                

