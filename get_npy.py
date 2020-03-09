'''
@Author: your name
@Date: 2020-02-12 21:52:26
@LastEditTime : 2020-02-13 21:03:38
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /test/clic2020-devkit/get_npy.py
'''
#!/usr/bin/env python3
import os
import glob
from PIL import Image
import numpy as np
import pframe_dataset_shared
from io import BytesIO
from skimage.measure import compare_ssim


from baseline_np import EXTENSION
from baseline_np import compress_encoder

def decode_residual():
    path = '/mnt/Volume0/test/clic2020-devkit/residual'
    path2 = '/mnt/Volume0/test/clic2020-devkit/reconstruct'
    
    os.chdir("/mnt/Volume0/test/bpg/libbpg-0.9.8")
    for root, dirs, files in os.walk(path, topdown = False):
            for name in files:
                str_path = os.path.join(root,name)
                if os.path.splitext(name)[1] == '.bpg':
                    p2 = os.path.basename(str_path).replace('.bpg', '.png')
                    p2 = os.path.join(path2,p2)
                    os.system("./bpgdec {path_en} -o {path_out}".format(path_en = str_path, path_out = p2))


def decoder(frame1, frame2_compressed):
    residual_normalized = np.array(frame2_compressed)
    return frame1 + (residual_normalized - 127) * 2


def decode(p):
    """Return decoded image from `p`.

    Assumes that the input frame corresponding to `p` is in the current working directory.
    The output will be saved in the current working directory.
    """
    #assert p.endswith('.' + EXTENSION)
    p2 = os.path.basename(p).replace('baseline.png', '.png')
    p2p = os.path.join('/mnt/Volume0/test/clic2020-devkit/result/', p2) #add by me
    pp = os.path.join('/mnt/Volume0/test/clic2020-devkit/targets',p2)
    p2 = os.path.join('/mnt/Volume0/test/clic2020-devkit/inputs/', p2) #add by me
    p1 = pframe_dataset_shared.get_previous_frame_path(p2)
    #p1 = os.path.join('/mnt/Volume0/test/clic2020-devkit/test_data/inputs/', p1)
    #assert os.path.isfile(p1), (p2, p1, p, len(glob.glob('*.png')))
    b = Image.open(p).convert('L')
    f2_reconstructed = decoder(np.array(Image.open(p1)), b)
    Image.fromarray(f2_reconstructed).save(p2p)
    return f2_reconstructed, np.array(Image.open(pp))


def main():
    path_residual = '/mnt/Volume0/test/clic2020-devkit/reconstruct' #decode 第一步
    mode = []
    for j in range(28,29):
        print(j)
        #compress_encoder('/mnt/Volume0/test/clic2020-devkit/residual',j)
        decode_residual()
        arr = []
        for root, dirs, files in os.walk(path_residual, topdown = False):
            for i,name in enumerate(sorted(files)):
                str_path = os.path.join(root,name)
                img1,img2 = decode(str_path)
                ssim = compare_ssim(img1,img2)
                if 'ybaseline.png' in name:
                    ssim = 4 * ssim
                    print("4:1:1")
                filename_enc = os.path.basename(str_path).replace('.png','.bpg')
                path_enc_dir = '/mnt/Volume0/test/clic2020-devkit/residual'
                path_enc = os.path.join(path_enc_dir,filename_enc)
                fsize = os.path.getsize(path_enc)
                bits = fsize*8

                prameter = []
                prameter.append(bits)
                prameter.append(ssim)
                arr.append(prameter)
                print(str_path)
                #print("Pic %d: The ssim is %f and the size is %d"%(i,ssim, bits))
            mode.append(arr)


    print(np.sum(np.array(mode))/12785/2)
    # np.save("/mnt/Volume0/test/clic2020-devkit/data.npy", np.array(mode))
    #print("The ssim is %f and the size is %d"%(ssim, bits))



if __name__ == '__main__':
    #main()
    # path_result = '/mnt/Volume0/test/clic2020-devkit/result'
    # sum = 0
    # for root, dirs, files in os.walk(path_result, topdown = False):
    #     for i,name in enumerate(sorted(files)):
    #         p_re = os.path.join(root,name)
    #         img_re = Image.open(p_re)
    #         img_re = np.array(img_re)
    #         p_tar = os.path.join('/mnt/Volume0/test/clic2020-devkit/targets',name)
    #         img_tar = Image.open(p_tar)
    #         img_tar = np.array(img_tar)
    #         ssim = compare_ssim(img_re,img_tar)
    #         if 'y.png' in name:
    #             ssim = ssim * 4
    #         sum = sum + ssim
    # print(sum/2)
    path_resi = '/mnt/Volume0/test/clic2020-devkit/residual'
    print(path_resi)
    for root, dirs, files in os.walk(path_resi, topdown = False):
        for name in sorted(files):
            if '.png' in name:
                re_img = os.path.join(root,name)
                print(re_img)
                os.system("rm {}".format(re_img))
    print("done")