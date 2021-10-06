import torch
import numpy as np
import math
import lib.cdp2adp as cdp2adp

def strategy_mtx(rho, f1, f2, f3, f4, f6, f7, f8, f9, f10, f11):
	n1, n2, n3, n4 = 8, 2, 2, 63        # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)
	N = n1 * n2 * n3 * n4         # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)
	q1, q2, q3, q4, q6, q7, q8, q9, q10, q11 = [], [], [], [], [], [], [], [], [], []

	AA = torch.tensor(range(N))
	AA = AA.reshape([n1, n2, n3, n4])

	## Q1: TOTAL (1 cell)
	q1 = np.full((1, N), rho * f1)

	## Q2: CENRACE (63 cells)
	q2 = np.zeros((n4, N))
	for x in range(n4):     # race
	    hist_idx = torch.flatten(AA[:, :, :, x]).tolist()
	    for i in hist_idx:
	        q2[x, i] = math.sqrt(rho * f2)

	## Q3: HISPANIC (2 cells)
	q3 = np.zeros((n3, N))
	for x in range(n3):
	    hist_idx = torch.flatten(AA[:, :, x, :]).tolist()
	    for i in hist_idx:
	        q3[x, i] = math.sqrt(rho * f3)   

	## Q4: VOTINGAGE (2 cells)
	q4 = np.zeros((n2, N))
	for x in range(n2):
	    hist_idx = torch.flatten(AA[:, x, :, :]).tolist()
	    for i in hist_idx:
	        q4[x, i] = math.sqrt(rho * f4) 

	## Q6: HHGQ (8 cells)
	q6 = np.zeros((n1, N))
	for x in range(n1):
	    hist_idx = torch.flatten(AA[x, :, :, :]).tolist()
	    for i in hist_idx:
	        q6[x, i] = math.sqrt(rho * f6) 

	## Q7: HISPANIC*CENRACE (126 cells)
	q7 = np.zeros((n3*n4, N))
	row_idx = 0 
	for x in range(n3): 
	    for y in range(n4):
	        hist_idx = torch.flatten(AA[:, :, x, y]).tolist()
	        for i in hist_idx:
	            q7[row_idx, i] = math.sqrt(rho * f7)
	        row_idx += 1

	## Q8: VOTINGAGE*CENRACE (126 cells)
	q8 = np.zeros((n2*n4, N))
	row_idx = 0 
	for x in range(n2): 
	    for y in range(n4):
	        hist_idx = torch.flatten(AA[:, x, :, y]).tolist()
	        for i in hist_idx:
	            q8[row_idx, i] = math.sqrt(rho * f8)
	        row_idx += 1

	## Q9: VOTINGAGE*HISPANIC (4 cells)
	q9 = np.zeros((n2*n3, N))
	row_idx = 0 
	for x in range(n2): 
	    for y in range(n3):
	        hist_idx = torch.flatten(AA[:, x, y, :]).tolist()
	        for i in hist_idx:
	            q9[row_idx, i] = math.sqrt(rho * f9)
	        row_idx += 1

	## Q10: VOTINGAGE*HISPANIC*CENRACE (252 cells)
	q10 = np.zeros((n2*n3*n4, N))
	row_idx = 0 
	for x in range(n2):
	    for y in range(n3):
	        for z in range(n4):
	            hist_idx = torch.flatten(AA[:, x, y, z]).tolist()
	            for i in hist_idx:
	                q10[row_idx, i] = math.sqrt(rho * f10)
	            row_idx += 1

	## Q11: HHGQ*VOTINGAGE*HISPANIC*CENRACE (2,016 cells)
	q11 = np.zeros((N, N))
	np.fill_diagonal(q11, math.sqrt(rho * f11))

	## stack all queries -> strategy matrix
	A = np.vstack((q1, q2, q3, q4, q6, q7, q8, q9, q10, q11))

	print(q1.shape, q2.shape, q3.shape, q4.shape, q6.shape, q7.shape, q8.shape, q9.shape, q10.shape, q11.shape, A.shape)
	return A
	
	
def workload_mtx_race():
	# setup parameters
	n1, n2, n3, n4 = 8, 2, 2, 63        # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)
	N = n1 * n2 * n3 * n4         # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)

	AA = torch.tensor(range(N))
	AA = AA.reshape([n1, n2, n3, n4])

	t = 7
	W = np.zeros((t, N))
	col_two_or_more_races = []
	for x in range(n4):
	    if x >= 0 and x <= 5:     
	        hist_idx = torch.flatten(AA[:, :, :, x]).tolist()
	        for i in hist_idx:
	            W[x, i] = 1
	    else:
	        hist_idx = torch.flatten(AA[:, :, :, x]).tolist()
	        col_two_or_more_races.extend(hist_idx)
	for i in hist_idx:
	    W[6, i] = 1
	return W


def workload_mtx_detail():
	# setup parameters
	n1, n2, n3, n4 = 8, 2, 2, 63        # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)
	N = n1 * n2 * n3 * n4         # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)

	W = np.zeros((N, N))
	np.fill_diagonal(W, 1)
	return W


def workload_mtx_va_race():
	# setup parameters
	n1, n2, n3, n4 = 8, 2, 2, 63        # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)
	N = n1 * n2 * n3 * n4         # number of attribute combinations: HHGQ (8) ∗ VOTINGAGE (2) ∗ HISPANIC (2) ∗ RACE (63)

	AA = torch.tensor(range(N))
	AA = AA.reshape([n1, n2, n3, n4])

	W = np.zeros((n2 * n4, N))
	row_idx = 0
	for x in range (n2):
	    for y in range(n4):
	        hist_idx = torch.flatten(AA[:, x, :, y]).tolist()
	        for i in hist_idx:
	            W[row_idx, i] = 1
	        row_idx += 1
	return W