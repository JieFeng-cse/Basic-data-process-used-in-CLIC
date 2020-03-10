'''
@Author: Jie
@Date: 2020-03-09 05:30:52
@LastEditTime: 2020-03-09 11:14:39
@LastEditors: Please set LastEditors
@Description: This python script is used to test bpg performance on several selected pics
@FilePath: /test/clic2020-devkit/bpg_as.py
'''
import os 
from PIL import Image
import numpy as np
import xlrd
import pandas as pd
import re
from ms_ssim_np import MultiScaleSSIM

_COMPONENTS_RE = re.compile(r'(.*?)_(\d{5})_([yuv]\.png)')
_COMPONENTS_RE_SUB = r'\1_{:05d}_\3'

def get_previous_frame_path(p):
    """Vlog_720P-7b30_00338_u.png"""
    return get_frame_path(p, offset=-1)
def get_next_frame_path(p):
    """Vlog_720P-7b30_00338_u.png"""
    return get_frame_path(p, offset=1)


def get_frame_path(p, offset):
    """
    INPUT a frame path `p` of the format NAME_INDEX_SUFFIX, where
        - NAME is the video name
        - INDEX is a five-digit number indexing the video
        - SUFFIX is one of (_y.png, _u.png, _v.png)
    :returns NAME_NEWINDEX_SUFFIX, where NEWINDEX = INDEX + `offset`.
    """
    dirname, basename = os.path.split(p)
    m = _COMPONENTS_RE.search(basename)
    if not m:
        raise ValueError('Invalid format: {}'.format(p))
    try:
        number = int(m.group(2))
    except ValueError:
        raise ValueError('Invalid format: {}'.format(p))
    new_number = number + offset
    new_basename = _COMPONENTS_RE.sub(_COMPONENTS_RE_SUB.format(new_number), basename)
    return os.path.join(dirname, new_basename)

def load_xlsx():
    df = pd.read_excel('/mnt/Volume1/test/clic2020-devkit/llog.xlsx',usecols=[4],names=None)
    df_li = df.values.tolist()
    namelist = []
    for path in df_li:
        name = os.path.basename(path[0])
        name = os.path.join("/mnt/Volume1/test/clic2020-devkit/residual",name)
        name = get_next_frame_path(name)
        namelist.append(name)
    return namelist
    
def find_residuals(namelist):
    for root, dirs, files in os.walk("/mnt/Volume1/test/clic2020-devkit/residual", topdown = False):
        for name in files:
            if '.bpg' in name:
                continue
            pref = get_previous_frame_path(name)
            pref = os.path.basename(pref)
            if pref in namelist:
                print("true")

def compress_encoder(namelist, save_path, qp):   
    os.chdir("/mnt/Volume1/test/bpg/libbpg-0.9.8")
    print("\nturn to bpg")
    for name in namelist:
        str_path = name
        p2 = os.path.basename(str_path).replace('.png', '.bpg')
        p2 = os.path.join(save_path,p2)
        os.system("./bpgenc -q {q} {path_en} -o {path_out}".format(q= qp, path_en = str_path, path_out = p2))

def decode_residual():
    path = '/mnt/Volume1/test/clic2020-devkit/part_bpg'
    path2 = '/mnt/Volume1/test/clic2020-devkit/bpg_resi_re'
    
    os.chdir("/mnt/Volume1/test/bpg/libbpg-0.9.8")
    for root, dirs, files in os.walk(path, topdown = False):
            for name in files:
                str_path = os.path.join(root,name)
                if os.path.splitext(name)[1] == '.bpg':
                    p2 = os.path.basename(str_path).replace('.bpg', '.png')
                    p2 = os.path.join(path2,p2)
                    #print(p2)
                    os.system("./bpgdec {path_en} -o {path_out}".format(path_en = str_path, path_out = p2))
    os.chdir("..")
    os.system("pwd")
    print("decode residual done!")
    #os.system("pwd")
def decoder(frame1, frame2_compressed):
    residual_normalized = np.array(frame2_compressed)
    return frame1 + (residual_normalized - 127) * 2


def decode(p):
    """Return decoded image from `p`.

    Assumes that the input frame corresponding to `p` is in the current working directory.
    The output will be saved in the current working directory.
    """
    #assert p.endswith('.' + EXTENSION)
    p1 = get_previous_frame_path(p)
    p1 = os.path.basename(p1)
    p1 = os.path.join('/mnt/Volume1/test/clic2020-devkit/inputs_yuv',p1)
    print(p)
    #assert os.path.isfile(p1), (p2, p1, p, len(glob.glob('*.png')))
    b = Image.open(p).convert('L')
    f2_reconstructed = decoder(np.array(Image.open(p1)), b)
    p2 = os.path.join('/mnt/Volume1/test/clic2020-devkit/bpg_reslut',os.path.basename(p))
    print(p)
    Image.fromarray(f2_reconstructed).save(p2)

def decode_part():
    decode_residual()
    path = '/mnt/Volume1/test/clic2020-devkit/bpg_resi_re'
    for root, dirs, files in os.walk(path, topdown = False):
        for name in sorted(files):
            p = os.path.join(root,name)
            decode(p)

def get_msssim():
    bppl =[]
    ssim = []
    namel = []
    path = '/mnt/Volume1/test/clic2020-devkit/bpg_reslut'
    path_ta = '/mnt/Volume1/test/clic2020-devkit/targets_yuv'
    path_bpg = '/mnt/Volume1/test/clic2020-devkit/part_bpg'
    for root, dirs, files in os.walk(path, topdown = False):
        for name in files:
            #get size
            p = os.path.join(path_bpg,name.replace('.png','.bpg'))
            size = os.path.getsize(p)
            fig1 = Image.open(os.path.join(root,name))
            fig1_array = np.asarray(fig1)
            fig2 = Image.open(os.path.join(path_ta,name))
            fig2_array = np.asarray(fig2)

            bpp = size*8 / fig1.size[0] / fig1.size[1]
            #fig2 = Image.open('/mnt/Volume0/test/1.png')
            fig1_array = fig1_array.reshape((1,fig1_array.shape[0],fig1_array.shape[1],1))
            fig2_array = fig2_array.reshape((1,fig2_array.shape[0],fig2_array.shape[1],1))

            # yuv = np.concatenate([fig1_array,fig1_array,fig1_array], axis = 3)
            # yuv1 = np.concatenate([fig2_array,fig2_array,fig2_array], axis = 3)
            score = MultiScaleSSIM(fig1_array,fig2_array, max_val=255, filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03, weights=None)
            print(score)
            bppl.append(bpp)
            ssim.append(score)
            namel.append(name)
    df1 = pd.DataFrame({'name':namel})
    df2 = pd.DataFrame({'bpp':bppl})
    df3 = pd.DataFrame({'ssim':ssim})
    writer = pd.ExcelWriter('/mnt/Volume1/test/clic2020-devkit/bpg_bpp_ssim.xlsx')

    df1.to_excel(writer,sheet_name='name',startcol=0)
    df2.to_excel(writer,sheet_name='bpp',startcol=1)
    df3.to_excel(writer,sheet_name='ssim',startcol=2)

    writer.save()



    


# namelist = load_xlsx()
# save_path = '/mnt/Volume1/test/clic2020-devkit/part_bpg'
# compress_encoder(namelist,save_path,29)
#decode_part()
get_msssim()

