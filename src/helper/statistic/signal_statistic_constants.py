#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.08.2016

:author: Paul Pasler
:organization: Reutlingen University
'''
from collections import OrderedDict
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config.config import ConfigProvider


TITLE = "%s for EEG of proband #%s"

SIGNALS_KEY = "signals"
GENERAL_KEY = "general"
RAW_KEY = "raw"

TIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"
DURATION_FORMAT_STRING = "%M:%S"

MAX_TYPE = "max"
MIN_TYPE = "min"
MEAN_TYPE = "mean"
AGGREGATION_TYPE = "aggregation"
DIFF_TYPE = "diff"

METHOD = "method"
TYPE = "type"

FREQ_RANGE = range(1, 15)

def initFields():
    return OrderedDict({
        "max": _initField(MAX_TYPE), 
        "min": _initField(MIN_TYPE), 
        "mean": _initField(MEAN_TYPE),
        "std": _initField(MEAN_TYPE),
        "var": _initField(MEAN_TYPE),
        "zeros": _initField(AGGREGATION_TYPE),
        "seq": _initField(AGGREGATION_TYPE),
        "out": _initField(AGGREGATION_TYPE),
        "energy": _initField(MEAN_TYPE),
        "zcr": _initField(AGGREGATION_TYPE),
    })

def _initField(typ, method=None):
    return {TYPE: typ,
             METHOD: method}

STAT_FIELDS = initFields()

def addMethods(util):
    util.statFields = STAT_FIELDS
    util.statFields["max"][METHOD] = util.su.maximum 
    util.statFields["min"][METHOD] = util.su.minimum
    util.statFields["mean"][METHOD] = util.su.mean
    util.statFields["std"][METHOD] = util.su.std
    util.statFields["var"][METHOD] = util.su.var
    util.statFields["zeros"][METHOD] = util.qu.countZeros
    util.statFields["seq"][METHOD] = util.qu.countSequences
    util.statFields["out"][METHOD] = util.qu.countOutliners
    util.statFields["energy"][METHOD] = util.su.energy
    util.statFields["zcr"][METHOD] = util.su.zcr

FILE_NAME = "EEG.csv"

def getNewFileName(filePath, fileExtension, suffix=None):
    fileName, _ = os.path.splitext(filePath)
    if suffix:
        fileName += suffix
    return "%s.%s" % (fileName, fileExtension)

experimentDir = ConfigProvider().getExperimentConfig().get("filePath")