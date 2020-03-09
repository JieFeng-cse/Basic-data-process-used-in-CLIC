'''
@Author: your name
@Date: 2020-02-25 09:15:15
@LastEditTime: 2020-02-25 09:18:04
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /Volume0/test/merge.py
'''
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib
from matplotlib import pyplot as plt
import os

# imy = Image.open('/mnt/Volume0/clic_P_frame/dataset/Animation_720P-3adc/Animation_720P-3adc_00001_y.png')
# imu = Image.open('/mnt/Volume0/clic_P_frame/dataset/Animation_720P-3adc/Animation_720P-3adc_00001_u.png')
# imv = Image.open('/mnt/Volume0/clic_P_frame/dataset/Animation_720P-3adc/Animation_720P-3adc_00001_v.png')

# toImage = Image.new('L',(imy.size[0]+ imu.size[0], imy.size[1]))
# print(imy.size[0])
# loc1 = (0,0)
# toImage.paste(imy,loc1)
# loc2 = (imy.size[0],0)
# toImage.paste(imu,loc2)
# loc3 = (imy.size[0],imu.size[1])
# toImage.paste(imv,loc3)

#toImage.save('/mnt/Volume0/test/merge.png')
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print("Path exists")
        return False


for root, dirs, files in os.walk("/mnt/Volume0/clic_P_frame/dataset", topdown = False):
    for name in sorted(dirs):
        str_path = os.path.join(root,name)
        save_root = '/mnt/Volume0/test/merge_yuv'
        tmp_dir = os.path.join(save_root,name)
        made = mkdir(tmp_dir)
        if made == False:
            continue
        #print(name)
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
                toImage = Image.new('L',(imy.size[0]+ imu.size[0], imy.size[1]))
                #print(imy.size[0])
                if imy.size[0]%2 and imy.size[1]%2:
                    print(name)
                    print(imy.size)
                loc1 = (0,0)
                toImage.paste(imy,loc1)
                loc2 = (imy.size[0],0)
                toImage.paste(imu,loc2)
                loc3 = (imy.size[0],imu.size[1])
                toImage.paste(imv,loc3)
                toImage.save(tmp_dir + '/'+ name + "_{:0>5d}".format(i) + '_merge.png')