#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.07.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

from base_test import *  # @UnusedWildImport

from Queue import Queue
import threading
from time import sleep

from posdbos.test.test_factory import TestFactory
from posdbos.collector.data_collector import EEGDataCollector
from posdbos.collector.window_dto import WindowDto

WINDOW_SECONDS = 1
SAMPLING_RATE = 4
WINDOW_COUNT = 2
FIELDS = ["F3", "F4", "X", "Y"]
WINDOW_SIZE = EEGDataCollector.calcWindowSize(WINDOW_SECONDS, SAMPLING_RATE)

class DataCollectorTest(BaseTest):

    def setUp(self):
        self.collectedQueue = Queue()
        self.collector = TestFactory.createTestDataCollector(self.collectedQueue, FIELDS, WINDOW_SECONDS, SAMPLING_RATE, WINDOW_COUNT)

    def _fillValues(self, count):
        data = self.collector.datasource.data
        fields = self.collector.fields
        for i in range(count):
            row = data[i].sensors
            fData = {x: row[x] for x in fields}
            self.collector._addData(fData)

    def _fillWindowFull(self):
        self._fillValues(WINDOW_SECONDS)

    def getEmptyDto(self):
        return WindowDto(WINDOW_SIZE, FIELDS)

    def test_windowsFilled(self):
        emptyDto = self.getEmptyDto()
        windowSize = EEGDataCollector.calcWindowSize(WINDOW_SECONDS, SAMPLING_RATE)

        win1 = self.collector.windows[0]
        win2 = self.collector.windows[1]

        self.assertEquals(win1.index, 0)
        self.assertEquals(win1.dto, emptyDto)
        self.assertEquals(win2.index, windowSize / 2)
        self.assertEquals(win2.dto, emptyDto)

        self._fillValues(windowSize / 2)
        self.assertEquals(win1.index, windowSize / 2)
        self.assertEquals(win1.dto.getData()["X"], {'quality': [0, 0], 'value': [24.0, 24.0]})
        self.assertEquals(win2.dto, emptyDto)
        self.assertEquals(win2.index, 0) 

        self._fillValues(windowSize / 2)
        self.assertEquals(win1.dto, emptyDto) 
        self.assertEquals(win2.index, 2) 

    def test_addData(self):
        self.assertEqual(self.collectedQueue.qsize(), 0)

        # stop populating after 1 round
        collectorThread = threading.Thread(target=self.collector.collectData)
        collectorThread.start()

        sleep(0.1)
        self.collector.close()
        collectorThread.join()

        self.assertTrue(self.collectedQueue.qsize() > 0)

    def test_filter(self):
        fields = ["F3", "X"]
        self.collector.fields = fields
        
        data = self.collector.datasource.data;
        
        filteredData = self.collector._filter(data[0].sensors)
        
        self.assertEqual(len(filteredData), len(fields))
        self.assertTrue(set(filteredData.keys()).issubset(set(fields)))
        self.assertTrue(set(filteredData.keys()).issuperset(set(fields)))

    def test_calcWindowSize(self):
        self.assertEqual(EEGDataCollector.calcWindowSize(1, 64), 64)
        self.assertEqual(EEGDataCollector.calcWindowSize(2, 32), 64)

    def test__calcWindowRatio(self):
        self.assertEqual(EEGDataCollector.calcWindowRatio(128, 2), 64)
        self.assertEqual(EEGDataCollector.calcWindowRatio(4, 4), 1)
        self.assertEqual(EEGDataCollector.calcWindowRatio(64, 4), 16)

    def test__buildSignalWindows_windowCount(self):
        col = self.collector
        winCount = 4
        self.collector._buildSignalWindows(4, winCount, 4)
        self.assertEqual(len(col.windows), winCount)
        for i in range(winCount):
            self.assertEqual(col.windows[i].index, i * col.windowRatio)

if __name__ == '__main__':
    unittest.main()