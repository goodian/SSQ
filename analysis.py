# -*- coding: utf-8 -*-
from utils import *

#个数
red_cnt_num = [0] * (NUM_RED + 1)

blue_cnt_num = [0] * (NUM_BLUE + 1)

# 概率
red_gailv = [0] * (NUM_RED + 1)

blue_gailv = [0] * (NUM_BLUE + 1)

result_red = {}
result_blue = {}

parsed_line = 0

def do_analysis():
    fp = open_for_read(DATA_FILE)
    if not fp:
        print "can't open file: %s"  % DATA_FILE
        return
    for line in fp:
        count_data_line(line)

    compute_gailv()
#end do_analysis

def compute_gailv():
    total_data_analysis()
    compute_result()
#end compute_gailv

def compute_result():
    compute_red()
    compute_blue()
#end compute_result

def compute_red():
    global parsed_line
    for i in range(1, NUM_RED + 1):
        result_red[i] = (G_RED * (parsed_line + 100) - red_gailv[i] * parsed_line)/100
#end compute_red

def compute_blue():
    global parsed_line
    for i in range(1, NUM_BLUE + 1):
        result_blue[i]= (G_BLUE * (parsed_line + 100) - blue_gailv[i] * parsed_line)/100
#end compute_blue

def total_data_analysis():
    global parsed_line
    for i in range(1, NUM_RED + 1):
        red_gailv[i] = red_cnt_num[i] * 1.0 / parsed_line

    for i in range(1, NUM_BLUE + 1):
        blue_gailv[i] = blue_cnt_num[i] * 1.0 / parsed_line
#end total_data_analysis


def count_data_line(line):
    global parsed_line

    line_list = line.split()
    if len(line_list) != 8:
        return

    for i in range(1, 7):
        red_cnt_num[int(line_list[i])] += 1

    blue_cnt_num[int(line_list[7])] += 1

    parsed_line += 1
#end count_data_line

def print_result():
    print "Red:"
    print_red()
    print "Blue:"
    print_blue()
#end print_result

def print_red():
    tmp = sorted(result_red.iteritems(), key = lambda d:d[1], reverse=True)
    for (k, v) in tmp:
        print "%d: %f" % (k, v)
#end print_red

def print_blue():
    tmp = sorted(result_blue.iteritems(), key = lambda d:d[1], reverse=True)
    for (k, v) in tmp:
        print "%d: %f" % (k, v)
#end print_blue

if __name__ == '__main__':
    do_analysis()
    print_result()
#end if
