'''
@Author: your name
@Date: 2020-03-15 23:25:15
@LastEditTime: 2020-03-15 23:27:40
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/rm_somefile.py
'''
import os
path = '/mnt/Volume1/test/clic2020-devkit/tng_m/tng3'
for root, dirs, files in os.walk(path, topdown = False):
    for name in files:
        if '.png' in name:
            os.system("rm " + os.path.join(root,name))
            print(name)
