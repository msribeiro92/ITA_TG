import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from MovingAverageStreamer import MovingAverageStreamer
from MovingAverageCrossing import MovingAverageCrossing
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

    def trendCheckerTest(self):
        dataArray = self.dataFrame["Close"]

        movingAverageCrossing  = MovingAverageCrossing(5, 20)
        movingAverageCrossing.setup(dataArray[:20])

        longAverage = MovingAverageStreamer(20)
        longAverage.setup(dataArray[:20])
        shortAverage = MovingAverageStreamer(5)
        shortAverage.setup(dataArray[:20])

        predictionArray = [movingAverageCrossing.lastValue]
        longAverageArray = [longAverage.lastValue]
        shortAverageArray = [shortAverage.lastValue]
        for data in dataArray[20:]:
            predictionArray.append(movingAverageCrossing.onData(data))
            longAverageArray.append(longAverage.onData(data))
            shortAverageArray.append(shortAverage.onData(data))

        trend = TrendChecker()
        print(trend.checkTrend(list(dataArray[19:]), predictionArray))

        plt.plot(range(len(dataArray)-19), dataArray[19:])
        plt.plot(longAverageArray, 'g')
        plt.plot(shortAverageArray, 'r')
        plt.show()

test = Test()
#test.testSampleData()
#test.testMovingAverageStremer()
test.trendCheckerTest()
