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

#================================================================================
# change codes according to http://wenku.baidu.com/view/e993e17601f69e314332949e.html
#================================================================================

def get_all_pos_red_res():
    '''
    get top 15 items in red
    '''
    tmp = sorted(result_red.iteritems(), key = lambda d:d[1], reverse=True)
    reds = []
    res = []
    count = 15

    for (k, v) in tmp:
        if count <= 0:
            break

        reds.append(k)
    #end for

    print reds

    r_len = len(reds)

    for i0 in range(r_len):
        for i1 in range(i0, r_len):
            for i2 in range(i1, r_len):
                for i3 in range(i2, r_len):
                    for i4 in range(i3, r_len):
                        for i5 in range(i4, r_len):
                            t = []
                            t.append(reds[i0])
                            if reds[i1] not in t:
                                t.append(reds[i1])
                            if reds[i2] not in t:
                                t.append(reds[i2])
                            if reds[i3] not in t:
                                t.append(reds[i3])
                            if reds[i4] not in t:
                                t.append(reds[i4])
                            if reds[i5] not in t:
                                t.append(reds[i5])
                            #print tuple(t)
                            res.append(t)
        #end for i1
        #res.append(t)

    #end for i0

    #print res
    return res

#end get_all_pos_red_res

def get_all_pos_blue_res():
    '''
    get top 5 items in red
    '''
    tmp = sorted(result_blue.iteritems(), key = lambda d:d[1], reverse=True)
    blues = []
    count = 5

    for (k, v) in tmp:
        if count <= 0:
            break

        blues.append(k)
    #end for

    print blues

    return blues

#end get_all_pos_blue_res

def do_ji_ou_filter(reds = [], blue = 0):
    ou_cnt = 0
    ji_cnt = 0

    for i in reds:
        if i % 2 == 0:
            ou_cnt += 1
        else:
            ji_cnt += 1

    return (2 <= ou_cnt <= 4) and (3 <= ji_cnt <= 4)

#end do_ji_ou_filter

def do_and_filter(reds = [], blue = 0):
    sum = 0

    for i in reds:
        sum += i

    return 78 <= sum <= 126

#end do_and_filter

def do_qujian_filter(reds = [], blue = 0):
    q1 = 0
    q2 = 0
    q3 = 0

    for i in reds:
        if i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            q1 += 1
        if i in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
            q2 += 1
        if i in [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
            q3 += 1
    #end for

    if q1 in [1, 2, 3] and q2 in [1, 2, 3] and q3 in [1, 2, 3]:
        return True
    return False
#end do_qujian_filter

def do_lianhao_filter(reds = [], blue = 0):
    '''
    限制为无连号或者一组两连号
    '''
    cnt = 0
    for i in reds:
        if (i + 1) in reds:
            cnt += 1

    if cnt >= 2:
        return False

    for i in reds:
        if ((i + 1) in reds and (i + 2) in reds):
            return False

    return True
#end do_lianhao_filter

ZHISHU = [1, 2,3,5,7,11,13,17,19,23,29,31]

def do_zhishu_filter(reds, blue):
    cnt = 0
    for i in reds:
        if i in ZHISHU:
            cnt += 1
    return 1 <= cnt <= 3
#end do_zhishu_filter

def do_big_small_filter(reds, blue):
    b_cnt = 0
    s_cnt = 0

    for i in reds:
        if i in [1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:
            b_cnt += 1
        else:
            s_cnt += 1

    if (3 <= b_cnt <= 4) and (2 <= s_cnt <= 3):
        return True
    return False
#end do_big_small_filter

def do_filters(reds = [], blue = 0):
    if not do_ji_ou_filter(reds, blue):
        return False

    if not do_and_filter(reds, blue):
        return False

    if not do_qujian_filter(reds, blue):
        return False

    if not do_big_small_filter(reds, blue):
        return False

    if not do_lianhao_filter(reds, blue):
        return False

    if not do_zhishu_filter(reds, blue):
        return False

    return True
#end do_filters

def get_all_pos_res():
    '''
    get top 15 in red and top 5 in blue
    '''

    reds = get_all_pos_red_res()
    blues = get_all_pos_blue_res()

    for r in reds:
        for b in blues:
            if do_filters(r, b):
                print (r, b)
#end get_all_pos_res


if __name__ == '__main__':
    do_analysis()
    print_result()
    get_all_pos_res()
#end if

