'''
@Author: your name
@Date: 2020-03-17 12:13:59
@LastEditTime: 2020-03-18 04:54:40
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/test_p/thread.py
'''
import os

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print("Path exists")
        return False

#os.system("sed -ie 's/LM = 0/LM = 1/g' /mnt/Volume1/test/clic2020-devkit/test_p/model_two/configs/config.py")
lasti = lastj = 0
path = '/test/clic2020-devkit/test_p/rc_data_flip/'
for i in range(1):
    for j in range(6):
        print("***********************************************************************************************************************************************************")
        print('LM = ' + str(i) + ', ' + 'angle = '+str(j+2))
        print("***********************************************************************************************************************************************************")
        mkdir(path+'angel_'+str(j+2)+'_LM_'+str(i)+'_re')
        mkdir(path+'angel_'+str(j+2)+'_LM_'+str(i))
        #os.system("sed -ie 's/LM = "+str(lastj)+"/LM = "+str(j)+ "/g' /test/clic2020-devkit/test_p/model_two/configs/config.py")
        os.system("./encode_rot /test/clic2020-devkit " + path+'angel_'+str(j+2)+'_LM_'+str(i))
        os.system("./decode_rot /test/clic2020-devkit/inputs " + path+'angel_'+str(j+2)+'_LM_'+str(i)+ ' ' + path+'angel_'+str(j+2)+'_LM_'+str(i)+'_re')
        lastj = j
    os.system("sed -ie 's/ANGLE = "+str(lastj+2)+"/ANGLE = "+str(j+2)+ "/g' /test/clic2020-devkit/test_p/model_two/configs/config.py")
    lasti = i

