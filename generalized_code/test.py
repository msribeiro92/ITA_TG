import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
import time
import operator
import sys

from MovingAverageStreamer import MovingAverageStreamer
from MovingAverageCrossing import MovingAverageCrossing
from IntelligentMovingAverageCrossing import IntelligentMovingAverageCrossing
from TrendChecker import TrendChecker

class Test:

    def __init__(self, fileName):
        self.dataFrame =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/' + fileName)

    def testSampleData(self, fileName):
        dataFrame = self.dataFrame =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/' + fileName)
        dataFrame["Close"].plot()
        plt.show()

    def testMovingAverageStremer(self):
        dataArray = self.dataFrame["Close"]

        movingAverageStreamer = MovingAverageStreamer(20)
        movingAverageStreamer.setup(dataArray[:20])

        movingAverageArray = [movingAverageStreamer.lastValue]
        for data in dataArray[20:]:
            movingAverageArray.append(movingAverageStreamer.onData(data))

        plt.plot(range(len(dataArray)-19), dataArray[19:])
        plt.plot(movingAverageArray, 'r')
        plt.show()

    def testReversals(self):
        dataArray = self.dataFrame["Close"]
        dataArray = np.array(dataArray)
        trend = TrendChecker()

        plt.plot(dataArray[1:100])
        #plt.plot(trend.identifyAllTrends(dataArray[:100]), 'g')
        dat = dataArray[1:100]
        rev = trend.identifyAllReversions(dat)
        rev2 = []
        for i in range(len(rev)):
            if rev[i]:
                rev2.append(dat[i] + 1)
            else:
                rev2.append(0)
        plt.plot(rev2,  color='r', marker='x', linestyle='')
        plt.show()
