import pandas as pd
import numpy as np
from lib.topdown_ols import *
import scipy.stats
import math


def query_detail_ori(hist):
	### workload matrix for original detailed histogram
	hist['BLK'] = hist['GEOID10'].astype(str)
	col_names = hist.columns.to_numpy()
	col_names = np.delete(col_names, [0, -1])
	hist = hist.groupby('BLK').sum()[col_names]
	return hist
	

def query_detail_dp(hist):
	### workload matrix for dp detailed histogram
	hist['BLK'] = hist['BLK'].astype(str)
	col_names = hist.columns.to_numpy()
	col_names = np.delete(col_names, [0])
	hist = hist.groupby('BLK').sum()[col_names]
	return hist


def query_race_va_ori(n2, n4, hist):
    ### workload matrix for race*va using original detailed histogram
    hist['BLK'] = hist['GEOID10'].astype(str)
    col_names = hist.columns.to_numpy()
    col_names = np.delete(col_names, [0, -1])
    hist = hist.groupby('BLK').sum()[col_names]
        
    for x in range(n2):
        x = '{number:0{width}d}'.format(width=2, number=x)
        col_names = [col for col in hist.columns if x in col[2:4] and len(col)==8]
        for y in range(n4):     
            y = '{number:0{width}d}'.format(width=2, number=y)
            col_names2 = [col for col in col_names if y in col[6:8]]
            hist[x + y] = hist[col_names2].sum(axis=1)
    hist.drop([col for col in hist.columns if len(col)==8], axis=1, inplace=True)
    return hist


def query_race_va_dp(n2, n4, hist):
    ### workload matrix for race*va using dp detailed histogram
    hist['BLK'] = hist['BLK'].astype(str)
    col_names = hist.columns.to_numpy()
    col_names = np.delete(col_names, [0, -1])
    hist = hist.groupby('BLK').sum()[col_names]
        
    for x in range(n2):
        x = '{number:0{width}d}'.format(width=2, number=x)
        col_names = [col for col in hist.columns if x in col[2:4] and len(col)==8]
        for y in range(n4):     
            y = '{number:0{width}d}'.format(width=2, number=y)
            col_names2 = [col for col in col_names if y in col[6:8]]
            hist[x + y] = hist[col_names2].sum(axis=1)
    hist.drop([col for col in hist.columns if len(col)==8], axis=1, inplace=True)
    return hist


def query_race_ori(n4, hist):
	### workload matrix for race using original detailed histogram
	hist['BLK'] = hist['GEOID10'].astype(str)
	col_names = hist.columns.to_numpy()
	col_names = np.delete(col_names, [0, -1])
	hist = hist.groupby('BLK').sum()[col_names]

	col_two_or_more_races = []
	for x in range(n4):     # race
	    if x >= 0 and x <= 5:
	        x = '{number:0{width}d}'.format(width=2, number=x)
	        col_names = [col for col in hist.columns if x in col[6:8]]
	        hist[str(x)] = hist[col_names].sum(axis=1)
	    else:
	        x = '{number:0{width}d}'.format(width=2, number=x)
	        col_names = [col for col in hist.columns if x in col[6:8]]
	        col_two_or_more_races.extend(col_names)
	hist['06'] = hist[col_two_or_more_races].sum(axis=1)
	hist.drop([col for col in hist.columns if len(col)==8], axis=1, inplace=True)
	return hist


def query_race_dp(n4, hist):
	### workload matrix for race using dp detailed histogram
	hist['BLK'] = hist['BLK'].astype(str)
	col_names = hist.columns.to_numpy()
	col_names = np.delete(col_names, [0])
	hist = hist.groupby('BLK').sum()[col_names]

	col_two_or_more_races = []
	for x in range(n4):     # race
	    if x >= 0 and x <= 5:
	        x = '{number:0{width}d}'.format(width=2, number=x)
	        col_names = [col for col in hist.columns if x in col[6:8]]
	        hist[str(x)] = hist[col_names].sum(axis=1)
	    else:
	        x = '{number:0{width}d}'.format(width=2, number=x)
	        col_names = [col for col in hist.columns if x in col[6:8]]
	        col_two_or_more_races.extend(col_names)
	hist['06'] = hist[col_two_or_more_races].sum(axis=1)
	hist.drop([col for col in hist.columns if len(col)==8], axis=1, inplace=True)
	return hist


def reid_risk(hist1, hist2):
	### calculate true positive rate [tp/(tp+fn)] with varying resolutions
	## block
	hist1_blk, hist2_blk = hist1, hist2
	tu = (hist1_blk == hist2_blk) & (hist1_blk == 1) & (hist2_blk == 1) # find a true unique
	if len(np.unique(tu.values, return_counts=True)[1]) == 2:  
	    n_tu = np.unique(tu.values, return_counts=True)[1][1]
	    u1 = hist1_blk == 1  # uniques after noise injection
	    n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    u2 = hist2_blk == 1  # uniques after noise injection
	    n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    ppv_blk = n_tu / n_u2   # precision
	    tpr_blk = n_tu / n_u1   # recall
	else:
	    n_tu = 0
	    u1 = hist1_blk == 1  # uniques after noise injection
	    if len(np.unique(u1.values, return_counts=True)[1]) == 2:
	    	n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    else:
	    	n_u1 = 0
	    u2 = hist2_blk == 1  # uniques after noise injection
	    if len(np.unique(u2.values, return_counts=True)[1]) == 2:
	    	n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    else:
	    	n_u2 = 0
	    ppv_blk = 0
	    tpr_blk = 0
	print(n_tu, n_u1, n_u2)

	## block group
	col_names = hist1.columns.to_numpy()
	hist1_bg = hist1.groupby(hist1.index.astype(str).str[:12]).sum()
	hist1_bg.index.name = 'BG'
	hist2_bg = hist2.groupby(hist2.index.astype(str).str[:12]).sum()
	hist2_bg.index.name = 'BG'

	tu = (hist1_bg == hist2_bg) & (hist1_bg == 1) & (hist2_bg == 1) # find a true unique
	if len(np.unique(tu.values, return_counts=True)[1]) == 2:  
	    n_tu = np.unique(tu.values, return_counts=True)[1][1]
	    u1 = hist1_bg == 1  # uniques after noise injection
	    n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    u2 = hist2_bg == 1  # uniques after noise injection
	    n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    ppv_bg = n_tu / n_u2   # precision
	    tpr_bg = n_tu / n_u1   # recall
	else:
	    n_tu = 0
	    u1 = hist1_bg == 1  # uniques after noise injection
	    if len(np.unique(u1.values, return_counts=True)[1]) == 2:
	    	n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    else:
	    	n_u1 = 0
	    u2 = hist2_bg == 1  # uniques after noise injection
	    if len(np.unique(u2.values, return_counts=True)[1]) == 2:
	    	n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    else:
	    	n_u2 = 0
	    ppv_bg = 0
	    tpr_bg = 0
	print(n_tu, n_u1, n_u2)
	
	## tract
	col_names = hist1.columns.to_numpy()
	hist1_tr = hist1.groupby(hist1.index.astype(str).str[:11]).sum()
	hist1_tr.index.name = 'TRACT'
	hist2_tr = hist2.groupby(hist2.index.astype(str).str[:11]).sum()
	hist2_tr.index.name = 'TRACT'

	tu = (hist1_tr == hist2_tr) & (hist1_tr == 1) & (hist2_tr == 1) # find a true unique
	if len(np.unique(tu.values, return_counts=True)[1]) == 2:  
	    n_tu = np.unique(tu.values, return_counts=True)[1][1]
	    u1 = hist1_tr == 1  # uniques after noise injection
	    n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    u2 = hist2_tr == 1  # uniques after noise injection
	    n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    ppv_tr = n_tu / n_u2   # precision
	    tpr_tr = n_tu / n_u1   # recall
	else:
	    n_tu = 0
	    u1 = hist1_tr == 1  # uniques after noise injection
	    if len(np.unique(u1.values, return_counts=True)[1]) == 2:
	    	n_u1 = np.unique(u1.values, return_counts=True)[1][1]
	    else:
	    	n_u1 = 0
	    u2 = hist2_tr == 1  # uniques after noise injection
	    if len(np.unique(u2.values, return_counts=True)[1]) == 2:
	    	n_u2 = np.unique(u2.values, return_counts=True)[1][1]
	    else:
	    	n_u2 = 0
	    ppv_tr = 0
	    tpr_tr = 0
	print(n_tu, n_u1, n_u2)
	
	return ppv_blk, ppv_bg, ppv_tr, tpr_blk, tpr_bg, tpr_tr


def reid_risk_ols(rho, hist1, W):
	### calculate true positive rate [tp/(tp+fn)] (for OLS estimators) with varying resolutions
	## block
	f1, f2, f3, f4, f6, f7, f8, f9, f10, f11 = 165/4099*5/4097, 165/4099*9/4097, 165/4099*5/4097, 165/4099*5/4097, 165/4099*5/4097, 165/4099*21/4097, 165/4099*21/4097, 165/4099*5/4097, 165/4099*71/4097, 165/4099*3945/4097
	A = strategy_mtx(rho, f1, f2, f3, f4, f6, f7, f8, f9, f10, f11)
	var = (W @ np.linalg.inv(A.T @ A) @ W.T)[0, 0]
	sigma = math.sqrt(var)
	column_values = hist1[hist1.columns].values.ravel()
	A = pd.unique(column_values)
	probs = []
	for i in A:
	    p1 = math.exp(-(i - 1)**2 / (2 * sigma**2))
	    u0 = hist1 == i
	    p2 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                           np.unique(u0.values, return_counts=True)[1][0])
	    probs.append(p1 * p2)
	p3 = 1
	u0 = hist1 == 1
	p4 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                       np.unique(u0.values, return_counts=True)[1][0])
	ppv_ols_blk = p3 * p4 / sum(probs)

	## block group
	col_names = hist1.columns.to_numpy()
	hist1_bg = hist1.groupby(hist1.index.astype(str).str[:12]).sum()

	f1, f2, f3, f4, f6, f7, f8, f9, f10, f11 = 1256/4099*1705/4099, 1256/4099*3/4099, 1256/4099*3/4099, 1256/4099*3/4099, 1256/4099*3/4099, 1256/4099*1055/4099, 1256/4099*9/4099, 1256/4099*3/4099, 1256/4099*24/4099, 1256/4099*1288/4099
	A = strategy_mtx(rho, f1, f2, f3, f4, f6, f7, f8, f9, f10, f11)
	W = workload_mtx_race()
	var = (W @ np.linalg.inv(A.T @ A) @ W.T)[0, 0]
	sigma = math.sqrt(var)

	column_values = hist1_bg[hist1_bg.columns].values.ravel()
	A = pd.unique(column_values)
	probs = []
	for i in A:
	    p1 = math.exp(-(i - 1)**2 / (2 * sigma**2))
	    u0 = hist1_bg == i
	    p2 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                           np.unique(u0.values, return_counts=True)[1][0])
	    probs.append(p1 * p2)
	p3 = 1
	u0 = hist1_bg == 1
	p4 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                       np.unique(u0.values, return_counts=True)[1][0])
	ppv_ols_bg = p3 * p4 / sum(probs)

	## tract
	col_names = hist1.columns.to_numpy()
	hist1_tr = hist1.groupby(hist1.index.astype(str).str[:11]).sum()

	f1, f2, f3, f4, f6, f7, f8, f9, f10, f11 = 687/4099*1567/4102, 687/4099*4/2051, 687/4099*5/4102, 687/4099*5/4102, 687/4099*5/4102, 687/4099*1933/4102, 687/4099*10/2051, 687/4099*5/4102, 687/4099*67/4102, 687/4099*241/2051
	A = strategy_mtx(rho, f1, f2, f3, f4, f6, f7, f8, f9, f10, f11)
	W = workload_mtx_race()
	var = (W @ np.linalg.inv(A.T @ A) @ W.T)[0, 0]
	sigma = math.sqrt(var)

	column_values = hist1_tr[hist1_tr.columns].values.ravel()
	A = pd.unique(column_values)
	probs = []
	for i in A:
	    p1 = math.exp(-(i - 1)**2 / (2 * sigma**2))
	    u0 = hist1_tr == i
	    p2 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                           np.unique(u0.values, return_counts=True)[1][0])
	    probs.append(p1 * p2)
	p3 = 1
	u0 = hist1_tr == 1
	p4 = np.unique(u0.values, return_counts=True)[1][1] / (np.unique(u0.values, return_counts=True)[1][1] + 
	                                                       np.unique(u0.values, return_counts=True)[1][0])
	ppv_ols_tr = p3 * p4 / sum(probs)
	
	tpr = scipy.stats.norm.cdf(0.5) - scipy.stats.norm.cdf(-0.5)
	return ppv_ols_blk, ppv_ols_bg, ppv_ols_tr, tpr


def acc_mae(hist1, hist2):
	### calculate true positive rate [tp/(tp+fn)] with varying resolutions
	## block
	hist1_blk, hist2_blk = hist1, hist2
	noise_blk = abs(hist2_blk - hist1_blk)
	mae_blk = noise_blk.values.mean()

	## block group
	col_names = hist1.columns.to_numpy()
	hist1_bg = hist1.groupby(hist1.index.astype(str).str[:12]).sum()
	hist1_bg.index.name = 'BG'
	hist2_bg = hist2.groupby(hist2.index.astype(str).str[:12]).sum()
	hist2_bg.index.name = 'BG'
	
	noise_bg = abs(hist2_bg - hist1_bg)
	mae_bg = noise_bg.values.mean()
	
	## tract
	col_names = hist1.columns.to_numpy()
	hist1_tr = hist1.groupby(hist1.index.astype(str).str[:11]).sum()
	hist1_tr.index.name = 'TRACT'
	hist2_tr = hist2.groupby(hist2.index.astype(str).str[:11]).sum()
	hist2_tr.index.name = 'TRACT'

	noise_tr = abs(hist2_tr - hist1_tr)
	mae_tr = noise_tr.values.mean()
	
	return mae_blk, mae_bg, mae_tr