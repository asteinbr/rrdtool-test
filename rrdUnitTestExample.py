#! /usr/bin/env python
# -*- coding: cp1252 -*-
# -*- mode: python; make-backup-files: nil -*-
####
# Example unittest for rrd tool
####
VERSION = "1.0"
# Author: Dr. T. Schönfelder
# 1.0: 24MAY13
####

import os
import time
import unittest
import rrdTestSetup
import rrdTest


class ExampleRrdTestCase(unittest.TestCase):
    def testSimple1(self):  ## test method names begin 'test*'
        """
Create rrd, fill with constant value 10, after HW working, jump to
value 20. Expect failure after 10 sampes.
Remove rrd file
"""

        # create an empty RRD (timeframe yesterday to now)
        primaryDataBinsTotal = rrdTestSetup.createTestRRD()
        # we are not able to fill the past history of data (it's only
        # a forward moving RRD!

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD created from %s to %s" % (time.ctime(first_time), time.ctime(last_time))



        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:7, samples=400)

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled first from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        rrdTest.createRRDGraph("1_T1")

##
        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:40, samples=100)

        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled second from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        rrdTest.createRRDGraph("1_T2")

        print rrdTest.xportTestRRD(primaryDataBinsTotal, 20, 'obs', primaryDataBinsTotal, primaryDataBinsTotal-600)

##        os.remove(os.path.join(rrdTestSetup.DATA_DIR, rrdTestSetup.RRDGaugeNameTemplate+'.rrd'))

##
        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:90, samples=50)

        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled second from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        rrdTest.createRRDGraph("1_T3")


    def testSimple2(self):  ## test method names begin 'test*'
        """
Create rrd, fill with constant value 10, after HW working, jump to
value 20. Expect failure after 10 sampes.
Remove rrd file
"""

        # create an empty RRD (timeframe yesterday to now)
        primaryDataBinsTotal = rrdTestSetup.createTestRRD()
        # we are not able to fill the past history of data (it's only
        # a forward moving RRD!

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD created from %s to %s" % (time.ctime(first_time), time.ctime(last_time))



        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:10, samples=200)

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled first from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        #rrdTest.createRRDGraph("2_T1")

##
        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:10, samples=200)

        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled second from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        #rrdTest.createRRDGraph("2_T2")

        print rrdTest.xportTestRRD(primaryDataBinsTotal, 20, 'obs', primaryDataBinsTotal, primaryDataBinsTotal-600)

##        os.remove(os.path.join(rrdTestSetup.DATA_DIR, rrdTestSetup.RRDGaugeNameTemplate+'.rrd'))


    def testSimple3(self):  ## test method names begin 'test*'
        """
Create rrd, fill with constant value 10, after HW working, jump to
value 20. Expect failure after 10 sampes.
Remove rrd file
"""

        # create an empty RRD (timeframe yesterday to now)
        primaryDataBinsTotal = rrdTestSetup.createTestRRD()
        # we are not able to fill the past history of data (it's only
        # a forward moving RRD!

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD created from %s to %s" % (time.ctime(first_time), time.ctime(last_time))



        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:1000, samples=200)

        # get first timestamp in rrd
        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled first from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        #rrdTest.createRRDGraph("2_T1")

##
        rrdTest.fillTestRRD(primaryDataBinsTotal, lambda x:800, samples=200)

        first_time = rrdTest.getRRDFirst(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert first_time != None
        assert isinstance(first_time, int)

        # get last timestamp in rrd
        last_time = rrdTest.getRRDLast(rrdTest.DATA_DIR, rrdTest.RRDGaugeNameTemplate)
        assert last_time != None
        assert isinstance(last_time, int)

        print "RRD filled second from %s to %s" % (time.ctime(first_time), time.ctime(last_time))

        #rrdTest.createRRDGraph("2_T2")

        print rrdTest.xportTestRRD(primaryDataBinsTotal, 20, 'fail', primaryDataBinsTotal, primaryDataBinsTotal-600)

##        os.remove(os.path.join(rrdTestSetup.DATA_DIR, rrdTestSetup.RRDGaugeNameTemplate+'.rrd'))


if __name__ == '__main__':
    originDir = os.getcwd()
    try:
        os.chdir(rrdTestSetup.RRD_DIR)
        unittest.main()
    except:
        # restore path
        os.chdir(originDir)













