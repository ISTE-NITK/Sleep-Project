# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 17:50:30 2017

@author: Lenovo
"""

import xlwt

wbk = xlwt.Workbook()
sheet = wbk.add_sheet('python')
row = 0 # row counter

f = open('output.txt')
for line in f:
    L = line.split('\t')
    for i,c in enumerate(L):
        sheet.write(row,i,c)
    row += 1
wbk.save('AirQuality.xls')