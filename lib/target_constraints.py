## A set of functions to match the target constraints between PUMS and the enumeration data set.

import numpy as np 

def convert_race(r):
    if r == 1 or r == 2:
        race = r
    elif r == 3:
        race = np.random.randint(3, 6, size=1)[0]
    elif r >= 4 and r <= 7:
        race = r + 2
    return race


def convert_sex(s):
    return s


def convert_age(a):
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