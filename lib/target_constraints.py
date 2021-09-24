## A set of functions to match the target constraints between PUMS and sf1.

import numpy as np 

def convert_race(r):
    ''' Convert race from sf1 to PUMS RAC1P'''
    if r == 1 or r == 2:
        race = r
    elif r == 3:
        race = np.random.randint(3, 6, size=1)[0]
    elif r >= 4 and r <= 7:
        race = r + 2
    return race


def convert_sex(s):
    ''' Convert sex from sf1 to PUMS RAC1P'''
    return s


def convert_age(a):
    ''' Convert age from sf1 to PUMS RAC1P'''
    if a == 1:
        age = [0, 4]
    elif a == 2:
        age = [5, 9]
    elif a == 3:
        age = [10, 14]
    elif a == 4:
        age = [15, 17]
    elif a == 5:
        age = [18, 19]
    elif a == 6:
        age = [20, 20]
    elif a == 7:
        age = [21, 21]
    elif a == 8:
        age = [22, 24]
    elif a == 9:
        age = [25, 29]
    elif a == 10:
        age = [30, 34]
    elif a == 11:
        age = [35, 39]
    elif a == 12:
        age = [40, 44]
    elif a == 13:
        age = [45, 49]
    elif a == 14:
        age = [50, 54]
    elif a == 15:
        age = [55, 59]
    elif a == 16:
        age = [60, 61]
    elif a == 17:
        age = [62, 64]
    elif a == 18:
        age = [65, 66]
    elif a == 19:
        age = [67, 69]
    elif a == 20:
        age = [70, 74]
    elif a == 21:
        age = [75, 79]
    elif a == 22:
        age = [80, 84]
    else:
        age = [85, 100]  
    return age      


def convert_race1(r):
    ''' Convert race from PUMS RAC1P to sf1 (7 cells)'''
    if r == 1 or r == 2:
        race = r
    elif r >= 3 and r <= 5:
        race = 3
    elif r >= 6 and r <= 9:
        race = r - 2
    return race


def convert_race2(r):
    ''' Convert race from PUMS RAC3P to sf1 (63 cells)'''
    if r >= 1 and r <= 3:
        race = r
    elif r >= 4 and r <= 10 or r == 42 or r >= 44 and r <= 48 or r == 50 or r == 54 or r == 56 or r == 76 or r == 77:
        race = 4
    elif r >= 11 and r <= 14:
        race = 5
    elif r >= 15 and r <= 17:
        race = r - 9
    elif r >= 18 and r <= 24 or r == 65 or r == 66:
        race = 9
    elif r >= 25 and r <= 28:
        race = 10
    elif r >= 29 and r <= 30:
        race = r - 18
    elif r >= 31 and r <= 36 or r == 74:
        race = 13
    elif r == 75:
        race = 14
    elif r >= 37 and r <= 38:
        race = r - 23
    elif r >= 39 and r <= 40:
        race = 16
    elif r == 41:
        race = 18
    elif r == 49 or r == 51 or r == 52 or r == 55 or r == 57 or r == 71:
        race = 19
    elif r == 43 or r == 53 or r == 58:
        race = 20
    elif r == 99:
        race = 21
    elif r >= 59 and r <= 61:
        race = r - 38
    elif r == 78:
        race = 23
    elif r == 79:
        race = 26
    elif r >= 62 and r <= 63:
        race = r - 37
    elif r == 64 or r == 80:
        race = 28
    elif (r >= 67 and r <= 69) or (r >= 72 and r <= 73):
        race = 29
    elif r == 70:
        race = 30
    elif r == 95 or r == 98 or r == 96:
        race = 41
    elif r == 81 or r == 97:
        race = 42
    elif r == 84:
        race = 48
    elif r >= 85 and r <= 89 or r == 93:
        race = 51
    elif r == 92:
        race = 56
    elif r == 82:
        race = 59
    elif r == 83:
        race = 60
    elif r >= 90 and r <= 91:
        race = 62
    elif r == 100:
        race = 63
    else:
        race = 0
        print(r)
    return race


def convert_age1(a):
    ''' Convert age from PUMS AGEP to sf1 age band (23 cells)'''
    if a >= 0 and a <= 17:
        age = 1
    elif a >= 18 and a <= 64:
        age = 2
    else:
        age = 3
    return age   


def convert_age2(a):
    ''' Convert age from PUMS AGEP to sf1 age band (23 cells)'''
    if a >= 0 and a <= 4:
        age = 1
    elif a >= 5 and a <= 9:
        age = 2
    elif a >= 10 and a <= 14:
        age = 3
    elif a >= 15 and a <= 17:
        age = 4
    elif a >= 18 and a <= 19:
        age = 5
    elif a == 20:
        age = 6
    elif a == 21:
        age = 7
    elif a >= 22 and a <= 24:
        age = 8
    elif a >= 25 and a <= 29:
        age = 9
    elif a >= 30 and a <= 34:
        age = 10
    elif a >= 35 and a <= 39:
        age = 11
    elif a >= 40 and a <= 44:
        age = 12
    elif a >= 45 and a <= 49:
        age = 13
    elif a >= 50 and a <= 54:
        age = 14
    elif a >= 55 and a <= 59:
        age = 15
    elif a >= 60 and a <= 61:
        age = 16
    elif a >= 62 and a <= 64:
        age = 17
    elif a >= 65 and a <= 66:
        age = 18
    elif a >= 67 and a <= 69:
        age = 19
    elif a >= 70 and a <= 74:
        age = 20
    elif a >= 75 and a <= 79:
        age = 21
    elif a >= 80 and a <= 84:
        age = 22
    else:
        age = 23
    return age      


def convert_hisp1(h):
    ''' Convert hispanic from PUMS HISP to sf1 hispanmic (2 cells)'''
    if h == 1:
        hisp = 1
    else:
        hisp = 2
    return hisp 


def convert_hhgq1(u):
    ''' Convert unit type from PUMS RELSHIPP to sf1 type (3 cells)'''
    if u <= 36:
        hhgq = 1
    elif u == 37:
        hhgq = 2
    elif u == 38:
        hhgq = 3
    return hhgq
