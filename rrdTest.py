# -*- coding: cp1252 -*-
####
#
# cpuFillerSetup
#
####
# Version 1.0
# Author: Dr. T. Sch�nfelder
# 1.0: 24MAY13
#
# Functionalities to use a RRD for tests
# support Holt-Winter algorithm
####
import traceback

RRDFIRSTTEMPLATE = 'rrdtool first \"%s/%s.rrd\"'
RRDLASTTEMPLATE = 'rrdtool last \"%s/%s.rrd\"'
RRDUPDATETEMPLATE = 'rrdtool update \"%s/%s.rrd\" %i:%i'
RRDXPORTTEMPLATE = 'rrdtool xport '+ \
                   '-s N-%i -e N-%i '+ \
                   'DEF:%s=\"%s\":%s:FAILURES XPORT:%s:%s'
RRDGRAPHTEMPLATE = 'rrdtool graph \"%s/%s.png\" '+ \
                   '-e N+100 '+ \
                   'DEF:obs=\"%s\":%s:AVERAGE '+ \
                   'DEF:pred=\"%s\":%s:HWPREDICT '+ \
                   'DEF:dev=\"%s\":%s:DEVPREDICT '+ \
                   'DEF:sea=\"%s\":%s:SEASONAL '+ \
                   'DEF:fail=\"%s\":%s:FAILURES '+ \
                   'TICK:fail#ffffa0:1.0:Fail '+\
                   'CDEF:scaledobs=obs,1,* '+\
                   'CDEF:upper=obs,pred,dev,1,*,+,+ '+\
                   'CDEF:lower=obs,pred,dev,1,*,-,+ '+\
                   'CDEF:scaledupper=upper,2,* '+\
                   'CDEF:scaledlower=lower,1,* '+\
                   'LINE1:pred#00ffff:Pred '+\
                   'LINE1:dev#a0ff00:dev '+\
                   'LINE1:scaledobs#00ff00:Obs '+\
                   'LINE2:scaledupper#ff0000:UpperBound '+\
                   'LINE1:sea#ffff00:LowerBound'
####
from rrdTestSetup import DATA_DIR, RRD_DIR, RRDGaugeNameTemplate, \
     SECONDS_PER_DAY, DEBUG

import os, time, sys

def print_execption_data():
    """Get the exception data for further analysis
"""
    print sys.exc_info()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print traceback.print_tb(exc_traceback)


def getRRDFirst(DATA_DIR, RRDGaugeNameTemplate):
    """Read timestamp of first data point in RRD file
Returns int as system time
"""
    # get first timestamp in rrd
    cmd_line = RRDFIRSTTEMPLATE % (DATA_DIR, RRDGaugeNameTemplate)
    try:
        cmd = os.popen4(cmd_line)
        cmd_output = cmd[1].read()
    except:
        for fd in cmd:
            fd.close()
    try:
        time = int(cmd_output) # should be plain integer
        return time
    except:
        print "Unable to execute first on rrd: " + cmd_output
        print cmd_output
    
def getRRDLast(DATA_DIR, RRDGaugeNameTemplate):
    """Read timestamp of last data point in RRD file
Returns int as system time
"""
    # get first timestamp in rrd
    cmd_line = RRDLASTTEMPLATE % (DATA_DIR, RRDGaugeNameTemplate)
    try:
        cmd = os.popen4(cmd_line)
        cmd_output = cmd[1].read()
    except:
        for fd in cmd:
            fd.close()
    try:
        time = int(cmd_output) # should be plain integer
        return time
    except:
        print "Unable to execute first on rrd: " + cmd_output
        print cmd_output
    
def fillTestRRD(primaryDataBinsTotal, fill_function, samples=None):
    """Fill rrd with test data generated by fill_function8integer)
"""
    # get first timestamp in rrd
    first_time = getRRDFirst(DATA_DIR, RRDGaugeNameTemplate)
    assert first_time != None
    assert isinstance(first_time, int)

    # get last timestamp in rrd
    last_time = getRRDLast(DATA_DIR, RRDGaugeNameTemplate)
    assert last_time != None
    assert isinstance(last_time, int)

    print "Fill RRD from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

    timeFrame = last_time-first_time
    steps = timeFrame / primaryDataBinsTotal # don't set every data point
    print "Set by", timeFrame, steps
    print "From %i to %i" % (first_time, last_time)
    this_sample = 0
    for timevalue in range(last_time+1, last_time+timeFrame, steps):
        if samples!=None:
            this_sample += 1
            if this_sample >= samples:
                break
        value = fill_function(timevalue)
        

    # update rrd
        if DEBUG:
            print timevalue, value
        cmd_update = RRDUPDATETEMPLATE % (DATA_DIR, RRDGaugeNameTemplate, \
                                          timevalue, int(value))
        if DEBUG:
            print "Update:", cmd_update

        cmd = os.popen4(cmd_update)
        cmd_output = cmd[1].read()
        for fd in cmd:
            fd.close()
        if len(cmd_output) > 0:
            print "Unable to update rrd: " + cmd_output
            print cmd_output

def xportTestRRD(primaryDataBinsTotal, dataBinsTotal, dsname, t_start, t_end):
    """Export rrd data for ds-name
"""
    # get first timestamp in rrd
    first_time = getRRDFirst(DATA_DIR, RRDGaugeNameTemplate)
    assert first_time != None
    assert isinstance(first_time, int)

    # get last timestamp in rrd
    last_time = getRRDLast(DATA_DIR, RRDGaugeNameTemplate)
    assert last_time != None
    assert isinstance(last_time, int)


    print "RRD from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

    timeFrame = last_time-first_time
    steps = timeFrame / primaryDataBinsTotal
    print "Set by", timeFrame, steps

    print dsname, RRDGaugeNameTemplate, t_start, t_end
    # update rrd
    #if DEBUG:
        #print timevalue, value
    rrd_filename = os.path.join(DATA_DIR, RRDGaugeNameTemplate+'.rrd').replace(':','\:')

    t_start = primaryDataBinsTotal
    t_end = 0
    cmd_xport = RRDXPORTTEMPLATE % (t_start*steps, t_end*steps, dsname, rrd_filename, RRDGaugeNameTemplate, \
                                    dsname, dsname)
    if not DEBUG:
        print "Xport:", cmd_xport

    cmd = os.popen4(cmd_xport)
    cmd_output = cmd[1].read()
    for fd in cmd:
        fd.close()
    if len(cmd_output) > 0:
        print "Unable to update rrd: " + cmd_output
        return cmd_output

def createRRDGraph(filename_extension=""):

    # get first timestamp in rrd
    first_time = getRRDFirst(DATA_DIR, RRDGaugeNameTemplate)
    assert first_time != None
    assert isinstance(first_time, int)

    # get last timestamp in rrd
    last_time = getRRDLast(DATA_DIR, RRDGaugeNameTemplate)
    assert last_time != None
    assert isinstance(last_time, int)

    print "Create Graph RRD RRD from %s to %s" % (time.ctime(first_time), time.ctime(last_time))


    # direct call to rrdtool
    rrd_filename = os.path.join(DATA_DIR, RRDGaugeNameTemplate+'.rrd').replace(':','\:')
##    print rrd_filename
    cmd_graph = RRDGRAPHTEMPLATE % (DATA_DIR, RRDGaugeNameTemplate+filename_extension,\
                                    rrd_filename, RRDGaugeNameTemplate, \
                                    rrd_filename, RRDGaugeNameTemplate, \
                                    rrd_filename, RRDGaugeNameTemplate, \
                                    rrd_filename, RRDGaugeNameTemplate, \
                                    rrd_filename, RRDGaugeNameTemplate)
    if not DEBUG:
        print cmd_graph
    try:
        cmd = os.popen4(cmd_graph)
        cmd_output = cmd[1].read()
    except:
        for fd in cmd:
            fd.close()
    if len(cmd_output) > 0:
        pixels = cmd_output.split('x')
        try:
            if len(pixels)!=2:
                raise Exception
            xPix = int(pixels[0])
            yPix = int(pixels[1])
        except:
            raise Exception, 'Unable to graph RRD: ' + cmd_output
        
if __name__=='__main__':
    print "Start"
    originDir = os.getcwd()
    try:
        os.chdir(RRD_DIR)
        createRRDGraph()
    except:
        import sys
        print sys.exc_info()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_tb(exc_traceback)
        # restore path
        os.chdir(originDir)

    pass