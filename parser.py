#!/usr/bin/env python
# coding: utf-8
'''
Description:
    Take an input file 'log.txt' and format into a csv file with columns x,y and cnum (the last of which represents the coordinate number e.g. 'x123' or 'y451 in data.
    Saves the csv as 'data_out.csv'

Dependencies:
    -python>=3.8
    -pandas
'''

import pandas

# open file (ROI info have been removed)
df = pandas.read_csv('log.txt', sep=':', header=None) # change 'log.txt' to your file

# split out the coordinate labels
df[['xynum','coordinate']] = df[0].str.split(expand=True)

df = df[[1, 'xynum']]


# get coordinate indecies
df[['yres','xnum']] = df['xynum'].str.split('x', expand=True)
df[['xres','ynum']] = df['xynum'].str.split('y', expand=True)


## coordinate index columns
df = df.fillna(0)
df['element_num'] = df['ynum'].astype(int) + df['xnum'].astype(int)
df = df[['element_num','xres','yres', 1]]
df['cnum'] = df['xres'] + df['yres']


# remove extra columns
df = df[['element_num','cnum', 1]]

# remove numbers from x,y columns
df['cnum'] = df['cnum'].str.replace('\d+', '')

# pivot on x,y pairs
final_data = df.pivot(index='element_num', columns='cnum').rename_axis(None)

# export to csv
final_data.to_csv('data_out.csv')

# Remove extra row from pivot things
with open('data_out.csv', 'r') as fin:
    data = fin.read().splitlines(True)
with open('data_out.csv', 'w') as fout:
    fout.writelines(data[1:])

