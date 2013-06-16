# -*- coding: cp1252 -*-
####
#
# rrdSetup
#
####
# Version 1.0
# Author: Dr. T. Schönfelder
# 1.0: 24MAY13
#
# Functionalities to create a RRD for tests
# support Holt-Winter algorithm
####
DATA_DIR = r"/home/asteinbr/Dropbox/University/0MSc/2. Term/Advanced Testing Methods/rrdtool/data"
RRD_DIR = r"/home/asteinbr/Dropbox/University/0MSc/2. Term/Advanced Testing Methods/rrdtool/"
RRDGaugeNameTemplate = 'test1'
DEBUG = False
####
SECONDS_PER_DAY = 86400
####
import os

def createTestRRD():

    assert os.path.exists('/usr/bin/rrdtool')
    daysWithBin = 1
    primaryDataBinsPerDay = SECONDS_PER_DAY/60
    primaryDataBinsTotal = primaryDataBinsPerDay*daysWithBin
    binDurationSeconds = SECONDS_PER_DAY/primaryDataBinsPerDay
    heartbeat = 2*binDurationSeconds
    rrd_gauge = RRDGaugeNameTemplate
    rraRows = primaryDataBinsTotal
    rrd_file = rrd_gauge+'.rrd'
    if DEBUG:
        print "Creating RRD", rrd_file
    try:
        os.makedirs(DATA_DIR) # just in case ...
    except:
        pass
    ds_string = ' DS:%s:GAUGE:%s:U:U' % (rrd_gauge, heartbeat)
    ## rrdtool params:
    ## step: lenght of a raw data bin [sec]
    ## heartbeat: max. distance of 2 data points (hb < step: several DP per bin required)
    HWPREDICT_length = rraRows/4
    HWPREDICT_alpha = 0.1
    HWPREDICT_beta = 0.0035
    SEASONAL_period = 60

    if DEBUG:
        print "Create RRD with"
        print "Data bins ttl.", primaryDataBinsTotal
        print "Data bin duration [sec]", binDurationSeconds
        print "Data time frame [hr]", primaryDataBinsTotal*binDurationSeconds/60/60
        print "Heart beat [sec]", heartbeat
        print "HWPREDICT_length [bins]", HWPREDICT_length
        print "HWPREDICT_alpha", HWPREDICT_alpha
        print "HWPREDICT_beta", HWPREDICT_beta
        print "SEASONAL_period [bins]", SEASONAL_period
    cmd_create = ''.join((
        'rrdtool create "', os.path.join(DATA_DIR,rrd_file), '" --start N-', str(binDurationSeconds*primaryDataBinsTotal), \
        ' --step ', str(binDurationSeconds), ds_string,
        ' RRA:AVERAGE:0.5:1:', str(rraRows),
        ' RRA:HWPREDICT:%i:%s:%s:%i' % (HWPREDICT_length, \
                                           ("%g" % HWPREDICT_alpha).replace('.','.'), \
                                           ("%g" % HWPREDICT_beta).replace('.','.'), \
                                           SEASONAL_period)
        ))

    if DEBUG:
        print cmd_create
    cmd = os.popen4(cmd_create)
    cmd_output = cmd[1].read()
    for fd in cmd:
        fd.close()
    if len(cmd_output) > 0:
        raise Exception, 'Unable to create RRD: ' + cmd_output

    # done with success
    assert os.path.exists(os.path.join(DATA_DIR,rrd_file))
    return primaryDataBinsTotal

        
if __name__=='__main__':
    pass
