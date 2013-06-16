# -*- coding: cp1252 -*-
####
#
# cpuFillerSetup
#
####
# Version 1.0
# Author: Dr. T. Schönfelder
# 1.0: 22MAY13
#
# Functionalities to create a RRD for the cpu
# support Holt-Winter algorithm
####
WORKING_DIR = r"/home/asteinbr/Dropbox/University/0MSc/2. Term/Advanced Testing Methods/rrdtool/"
RRDGaugeNameTemplate = 'cpu%s'
####
SECONDS_PER_DAY = 86400
####

def createCpuRRD(cpu_id):
    assert isinstance(cpu_id, int)
    import os
    daysWithBin = 1
    primaryDataBinsPerDay = SECONDS_PER_DAY/60
    primaryDataBinsTotal = primaryDataBinsPerDay*daysWithBin
    binDurationSeconds = SECONDS_PER_DAY/primaryDataBinsPerDay
    heartbeat = 2*binDurationSeconds
    rrd_gauge = RRDGaugeNameTemplate % cpu_id
    rraRows = primaryDataBinsTotal
    rrd_file = rrd_gauge+'.rrd'
    print "Creating RRD", rrd_file
    ds_string = ' DS:%s:GAUGE:%s:U:U' % (rrd_gauge, heartbeat)
    ## rrdtool params:
    ## step: lenght of a raw data bin [sec]
    ## heartbeat: max. distance of 2 data points (hb < step: several DP per bin required)
    HWPREDICT_length = rraRows/4
    HWPREDICT_alpha = 0.1
    HWPREDICT_beta = 0.0035
    SEASONAL_period = 60

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
        'rrdtool create "', os.path.join(WORKING_DIR,rrd_file), '" --start N-', str(binDurationSeconds*primaryDataBinsTotal), \
        ' --step ', str(binDurationSeconds), ds_string,
        ' RRA:AVERAGE:0.5:1:', str(rraRows),
        ' RRA:HWPREDICT:%i:%s:%s:%i' % (HWPREDICT_length, \
                                           ("%g" % HWPREDICT_alpha).replace('.','.'), \
                                           ("%g" % HWPREDICT_beta).replace('.','.'), \
                                           SEASONAL_period)
        ))

    print cmd_create
    cmd = os.popen4(cmd_create)
    cmd_output = cmd[1].read()
    for fd in cmd:
        fd.close()
    if len(cmd_output) > 0:
        raise Exception, 'Unable to create RRD: ' + cmd_output

        
if __name__=='__main__':
    # get number of cores
    import psutil
    no_cores = len(psutil.cpu_percent(interval=1, percpu=True))
    assert no_cores > 0
    import time
    print "Creating\n at %i (%s) for %i cores" % (time.time(), time.ctime(), no_cores)
    print " RRD data at", WORKING_DIR
    import os
    originDir = os.getcwd()
    os.chdir(WORKING_DIR)
    for cpu_id in range(1,no_cores+1):
        createCpuRRD(cpu_id)
    os.chdir(originDir)
