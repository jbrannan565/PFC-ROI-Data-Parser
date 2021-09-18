#!/usr/bin/python3
# coding: utf-8
'''
Description:
    Single file mode:
        Take an input file name passed after --in-file and format into a csv file with 
        columns x,y and cnum (the last of which represents the coordinate number, 
        e.g. 'x123' or 'y451' in data). Saves the csv as name passed after --out-file.

    Multi-file mode:
        Take an input directory (folder) name passed after --in-dir and format each txt file
        into a csv file with columns x,y and cnum (the last of which represents the coordinate number, 
        e.g. 'x123' or 'y451 in data). Saves the results in the directory passed after --out-dir
        as a csv file with the name of the file processed with .csv instead of .txt 
        (e.g. if the file was named FILE.txt, the csv file will be named FILE.csv).

Usage:
    ./parser.py --in-file IN_FILE.txt --out-file OUT_FILE.csv
    ./parser.py --in-dir IN_DIR_PATH --out-dir OUT_DIR_PATH

Dependencies:
    -python>=3.8
    -pandas
'''

import pandas
import argparse
import os

def log_df_to_xy_df(df):
    """
    turns log dataframe `df` into x,y columned dataframe
    """
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

    return final_data


def read_roi_file_parse_and_save(in_file_name, out_file_name):
    """
    Processes contents of in_file_name as ROI coordinates and saves the results in out_file_name
    """
    # open file (ROI info have been removed)
    df = pandas.read_csv(in_file_name, sep=':', header=None) # change 'log.txt' to your file

    final_data = log_df_to_xy_df(df)

    # export to csv
    final_data.to_csv(out_file_name)

    # Remove extra row from pivot things
    with open(out_file_name, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(out_file_name, 'w') as fout:
        fout.writelines(data[1:])


def process_roi_dir(in_dir, out_dir):
    """
    Process all ROI coordinate files in in_dir and save the results to out_dir
    """
    files = os.listdir(in_dir)
    for f in files:
        # check for file type
        if ".txt" not in f:
            continue

        # contruct file paths
        in_file  = f"{in_dir}/{f}"
        out_file = f"{out_dir}/{f.replace('.txt','.csv')}"
        
        # process data
        read_roi_file_parse_and_save(in_file, out_file)


# Begining of program
if __name__ == "__main__":
    # handle arguments
    arg_parser = argparse.ArgumentParser(description="Parses the coordinates of ROI into x,y columns")
    arg_parser.add_argument('--in-file', action='store', type=str, required=False)
    arg_parser.add_argument('--out-file', action='store', type=str, required=False)
    arg_parser.add_argument('--in-dir', action='store', type=str, required=False)
    arg_parser.add_argument('--out-dir', action='store', type=str, required=False)

    args = arg_parser.parse_args()

    # process args
    if args.in_file and args.out_file:
        # handle single file
        read_roi_file_parse_and_save(args.in_file_name, args.out_file_name)

    elif args.in_dir and args.out_dir:
        # handle full directory
        process_roi_dir(args.in_dir, args.out_dir)

    else:
        print("Invalid input")
