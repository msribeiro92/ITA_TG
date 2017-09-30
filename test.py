import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from MovingAverageStreamer import MovingAverageStreamer
from MovingAverageCrossing import MovingAverageCrossing
from IntelligentMovingAverageCrossing import IntelligentMovingAverageCrossing
from TrendChecker import TrendChecker

class Test:

    def __init__(self):
        self.dataFrame =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/AAPL_data.csv')

    def testSampleData(self):
        self.dataFrame["Close"].plot()
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

    def testTrendChecker(self, shortPeriod, longPeriod):
        dataArray = self.dataFrame["Close"]

        movingAverageCrossing  = MovingAverageCrossing(shortPeriod, longPeriod)
        movingAverageCrossing.setup(dataArray[:longPeriod])

        longAverage = MovingAverageStreamer(longPeriod)
        longAverage.setup(dataArray[:longPeriod])
        shortAverage = MovingAverageStreamer(shortPeriod)
        shortAverage.setup(dataArray[:longPeriod])

        predictionArray = [movingAverageCrossing.lastValue]
        longAverageArray = [longAverage.lastValue]
        shortAverageArray = [shortAverage.lastValue]
        for data in dataArray[longPeriod:]:
            predictionArray.append(movingAverageCrossing.onData(data))
            longAverageArray.append(longAverage.onData(data))
            shortAverageArray.append(shortAverage.onData(data))

        trend = TrendChecker()
        print(trend.checkTrend(list(dataArray[longPeriod-1:]), predictionArray))

        #plt.plot(range(len(dataArray)-longPeriod+1), dataArray[longPeriod-1:])
        #plt.plot(longAverageArray, 'g')
        #plt.plot(shortAverageArray, 'r')
        #plt.show()

    def testIntelligentMovingAverageCrossing(self, flip):
        dataArray = self.dataFrame["Close"]
        trainingIndex = 400 # 100, 170, 180, 190. 200, 210, 220, 400

        intelligentMovingAverageCrossing = IntelligentMovingAverageCrossing()
        intelligentMovingAverageCrossing.setup(
            dataArray[:20],
            dataArray[20:trainingIndex]
        )

        if flip:
            trend = intelligentMovingAverageCrossing.trend
            intelligentMovingAverageCrossing.trend = not trend
            #lv = intelligentMovingAverageCrossing.lastValue
            #intelligentMovingAverageCrossing.lastValue = (not lv[0], lv[1])

        predictionArray = [intelligentMovingAverageCrossing.lastValue]
        for data in dataArray[trainingIndex:]:
            predictionArray.append(
                intelligentMovingAverageCrossing.onData(data)
            )

        trend = TrendChecker()
        print(trend.checkTrend(list(dataArray[trainingIndex-1:]), predictionArray))

test = Test()
#test.testSampleData()
#test.testMovingAverageStremer()
test.testTrendChecker(5, 20)
test.testTrendChecker(10, 20)
test.testTrendChecker(5, 10)
test.testIntelligentMovingAverageCrossing(False)
test.testIntelligentMovingAverageCrossing(True)
