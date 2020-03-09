#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
from tqdm import tqdm_notebook
import sys
import re
import pulp

def get_rc_arr(npy_list):
    rc_arr = None
    for npy_file in npy_list:
        if type(rc_arr) == type(None):
            rc_arr = np.load(npy_file)
        else:
            rc_arr = np.concatenate((rc_arr, np.load(npy_file)), axis=1)
    return rc_arr

def interpreter_RC_results(variables, N_img):
    index = np.zeros(N_img, dtype=np.int)
    for v in variables:
        i_img, m_model = re.findall(r'\d+', str(v.name))
        if int(v.varValue) == 1:
            index[int(i_img)] = int(m_model)
    return index

def create_names(N_img, M_model):
    names = []
    for i_img in range(N_img):
        for j_model in range(M_model):
            names.append('Img_%d_Model_%d' % (i_img, j_model))
    return names

def summary_rc(array, idex):
    #total_RGB_size = 720*1280*2/3*12786
    bpp = np.sum([array[j][i][0] for i, j in enumerate(idex)])
    ms_ssim = np.mean([array[j][i][1] for i, j in enumerate(idex)])
    print("bpp : %lf, ms_ssim : %lf" % (bpp, ms_ssim))
    print("Model Index For Each Image : \n", idex)

def pulp_solver(rc_arr, Min_ms_ssim, Min_psnr):
    N_img, M_model, _ = rc_arr.shape
    names = create_names(N_img, M_model)
    total_RGB_size = np.sum(rc_arr[:, 0, 2])
    
    x = pulp.LpVariable.dicts("Idex", names, 0, 1, cat='Integer')
    prob = pulp.LpProblem("The RC Problem", pulp.LpMinimize)
    for i_img in range(N_img):
        prob += pulp.lpSum([x['Img_%d_Model_%d' % (i_img, j_model)] for j_model in range(M_model)]) == 1., 'Idex_Img_%d'%i_img

    ms_list = []
    se_list = []
    bpp_list = []
    for i_img in range(N_img):
        for j_model in range(M_model):
            ms_list.append(x['Img_%d_Model_%d' % (i_img, j_model)]*rc_arr[i_img, j_model, 3])
            bpp_list.append(x['Img_%d_Model_%d' % (i_img, j_model)]*rc_arr[i_img, j_model, 0])

    prob += pulp.lpSum(bpp_list), 'Minimum bits'        
    prob += pulp.lpSum(ms_list) >= Min_ms_ssim * N_img, 'ms_ssim requirement'
    prob += pulp.lpSum(se_list) <= 255.**2/10.**(Min_psnr/10) * total_RGB_size, 'se_sum(psnr) requirement'
    prob.solve()
    index = interpreter_RC_results(prob.variables(), N_img)
    summary_rc(rc_arr, index)
    return index

def pulp_solver_low_BR(rc_arr, Max_bpp, psnr_flag=False):
    M_model, N_img, _ = rc_arr.shape
    names = create_names(N_img, M_model)
    
    x = pulp.LpVariable.dicts("Idex", names, 0, 1, cat='Integer')
    
    if psnr_flag:
        prob = pulp.LpProblem("The RC Problem", pulp.LpMinimize)
    else:        
        prob = pulp.LpProblem("The RC Problem", pulp.LpMaximize)
        
    for i_img in range(N_img):
        prob += pulp.lpSum([x['Img_%d_Model_%d' % (i_img, j_model)] for j_model in range(M_model)]) == 1., 'Idex_Img_%d'%i_img

    ms_list = []
    bpp_list = []
    for i_img in range(N_img):
        for j_model in range(M_model):
            ms_list.append(x['Img_%d_Model_%d' % (i_img, j_model)]*rc_arr[j_model, i_img, 1])
            bpp_list.append(x['Img_%d_Model_%d' % (i_img, j_model)]*rc_arr[j_model, i_img, 0])
    
    if psnr_flag == False:    
        prob += pulp.lpSum(ms_list), 'ms_ssim objective'
        
    prob += pulp.lpSum(bpp_list) <= int(38999000*6), 'Maximum bits requirement' 
    prob.solve()
    index = interpreter_RC_results(prob.variables(), N_img)
    summary_rc(rc_arr, index)
    return index


if __name__=="__main__":
    ######################## EXAMPLE #################
    
    # data_file1 = "calculate_post_processing0124.npy"
    # data_file2 = "calculate_post_processing56.npy"
    # data_file3 = "calculate_post_processing78.npy"
    # data_file4 = "calculate_post_processing3.npy"
    # data_file5 = "calculate_post_processing012.npy"
    # data_file6 = "calculate_post_processing345.npy"
    data_file7 = "data.npy"

    rc_arr = get_rc_arr([data_file7])  # data_file1, data_file2, data_file3, data_file4, 

    #rc_arr.shape, np.sum(rc_arr[:, 0, 2]) # rc_arr : [N_image, M_model, K_metric], K_metric : bits, ms_ssim

    # Min_ms_ssim = 0.993
    # Min_psnr = 40 # in dB
    Max_bpp = 0.075

    ## For 40 dB
    # index = pulp_solver(rc_arr, Min_ms_ssim, Min_psnr)

    ## Maximize PSNR
    #index = pulp_solver_low_BR(rc_arr, Max_bpp, psnr_flag=True)

    ## Maximize MS-SSIM
    index = pulp_solver_low_BR(rc_arr, Max_bpp, psnr_flag=False)
    np.save('/mnt/Volume0/test/clic2020-devkit/index.npy',index)