import sys, os

#file which store SSQ datas
DATA_FILE = "./result.txt"

#max data to analysis
MAX_TERM = 10000

NUM_RED = 33
NUM_BLUE = 16

G_RED = 1 - 1.0 / (32 * 31 * 30 * 29 * 28 * 27)
G_BLUE = 1.0/16

def open_for_read(name = ""):
    fp = None

    if not name or len(name) == 0:
        print "can not open file."
        return None

    if not os.path.exists(name):
        print "can not find file: %s, please check." % name
        return None

    try:
        fp = open(name, 'r')
    except Exception, e:
        print "Open file %s got except: %s." % (name, e)

    return fp

#end open_file

def open_for_write(name = ""):
    fp = None

    if not name or len(name) == 0:
        print "can not open file."
        return None

    if not os.path.exists(name):
        print "can not find file: %s, create a new one." % name

    try:
        fp = open(name, 'w')
    except Exception, e:
        print "Open file %s got except: %s." % (name, e)

    return fp

#end open_file

def close_file(fp = None):
    if not fp:
        print "fp error."
        return
    fp.close()
#end close_file
