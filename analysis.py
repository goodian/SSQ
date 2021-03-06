# -*- coding: utf-8 -*-
import random
from utils import *

PRINT_TAOBAO_FMT = "%02d %02d %02d %02d %02d %02d:%02d"
RESULT_CNT = 10
AC_R = 6
LAST_NUM = []
ZHISHU = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
last_sd = 0

#个数
red_cnt_num = [0] * (NUM_RED + 1)

blue_cnt_num = [0] * (NUM_BLUE + 1)

# 概率
red_gailv = [0] * (NUM_RED + 1)

blue_gailv = [0] * (NUM_BLUE + 1)

result_red = {}
result_blue = {}

parsed_line = 0

def get_last_data(line):
    global LAST_NUM
    if not line or len(line) == 0:
        print "get last line data error.\n"
        os.exit()
    data_list = line.split()

    for i in range(1, 8):
        LAST_NUM.append(int(data_list[i]))
    print LAST_NUM
#end get_last_data

def do_analysis():
    fp = open_for_read(DATA_FILE)
    if not fp:
        print "can't open file: %s"  % DATA_FILE
        return
    for line in fp:
        count_data_line(line)
    get_last_data(line)
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

    cnt = 10 * RESULT_CNT
    while cnt > 0:
        tmp = random.sample(reds, 6)
        if tmp not in res:
            res.append(tmp)
            cnt = cnt - 1

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
    return 78 <= sum(reds) <= 126
#end do_and_filter

def do_qujian_filter(reds = [], blue = 0):
    q1 = 0
    q2 = 0
    q3 = 0

    for i in reds:
        if i in range(1, 12):
            q1 += 1
        elif i in range(12, 23):
            q2 += 1
        elif i in [23, 34]:
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
        if (i + 1) in reds: cnt += 1

    if cnt > 2: return False

    return True
#end do_lianhao_filter

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
        if i in range(1, 17):
            b_cnt += 1
        else:
            s_cnt += 1

    if (3 <= b_cnt <= 4) and (2 <= s_cnt <= 3):
        return True
    return False
#end do_big_small_filter

def do_AC_filter(reds, blue):
    tmp = []

    for i in reds:
        for j in reds:
            d = i - j
            if d != 0 and abs(d) not in tmp: tmp.append(abs(d))
        #end for
    #end for

    return 6 <= len(tmp) - AC_R + 1 <= 9

#end do_AC_filter

def get_sandu(reds):
    tmp = []

    for i in reds:
        t = 99
        for j in reds:
            d = i - j
            if d != 0 and t > abs(d):
                t = abs(d)
        if t != 99: tmp.append(t)

    return max(tmp)
#end get_sandu

def do_sandu_filter(reds, blue):
    return get_sandu(reds) in range(5, 10)
#end do_sandu_filter

def do_chonghao_filter(reds, blue):
    cnt = 0

    for i in reds:
        if i in LAST_NUM:
            cnt += 1
    return cnt in [1, 2]
#end do_chonghao_filter

def do_piandu_filter(reds, blue):
    global last_sd
    tmp = []

    for i in LAST_NUM:
        t = 99
        for j in reds:
            d = i - j
            if d != 0 and t > abs(d):
                t = abs(d)
        if t != 99: tmp.append(t)

    piandu = max(tmp)
    if last_sd == 0: last_sd = get_sandu(LAST_NUM)
    return piandu in range(4, 8) and piandu >= last_sd
#end do_piandu_filter

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

    if not do_AC_filter(reds, blue):
        return False

    if not do_sandu_filter(reds, blue):
        return False

    if not do_chonghao_filter(reds, blue):
        return False

    if not do_piandu_filter(reds, blue):
        return True
        #return False

    return True
#end do_filters

def print_taobao_format(reds = [], blue = 0):
    print PRINT_TAOBAO_FMT % (reds[0], reds[1], reds[2], reds[3], reds[4], reds[5], blue)
#end print_taobao_format

def has_similar_in_results(reds, results):
    for r in results:
        cnt = 0
        for i in reds:
            if i in r[0]:
                cnt += 1
            #end if
        #end for
        if cnt >= 4:
            return True
    #end for
    return False
#end has_similar_in_results

def get_all_pos_res():
    '''
    get top 15 in red and top 5 in blue
    '''
    false_cnt = 0
    reds = get_all_pos_red_res()
    blues = get_all_pos_blue_res()
    results = []

    remains = RESULT_CNT
    while remains > 0:
        (r, b) = (random.sample(reds, 1)[0], random.sample(blues, 1)[0])
        if do_filters(r, b):
            r.sort()
            if (r, b) in results:
                false_cnt += 1
                continue
            if has_similar_in_results(r, results):
                false_cnt += 1
                continue
            results.append((r, b))
            print_taobao_format(r, b)
            remains -= 1
        else:
            false_cnt += 1
            if false_cnt >= RESULT_CNT * 100:
                reds = get_all_pos_red_res()
                blues = get_all_pos_blue_res()
                false_cnt = 0
                #print "Can not get enough results, retry..."
            #end if
        #end if
    #end while
#end get_all_pos_res

if __name__ == '__main__':
    do_analysis()
    print_result()
    get_all_pos_res()
#end if

