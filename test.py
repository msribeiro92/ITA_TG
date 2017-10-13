import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
import time

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
        return (
            trend.checkTrendNoReversal(
                list(dataArray[longPeriod-1:]),
                predictionArray[1:]
            ),
            trend.checkPNL(
                list(dataArray[longPeriod-1:]),
                predictionArray[1:]
            )
        )

    def testIntelligentMovingAverageCrossing(self, featureSelection=False):
        dataArray = self.dataFrame["Close"]
        initializationIndex = 20
        trainingIndex = 300 # 100, 170, 180, 190. 200, 210, 220, 400
        initialData = dataArray[:initializationIndex]
        trainingData = dataArray[initializationIndex:trainingIndex]

        if featureSelection:
            intelligentMovingAverageCrossing = \
                IntelligentMovingAverageCrossing(
                    featureSelection=True,
                    initialData=initialData,
                    trainingData=trainingData
                )
        else:
            intelligentMovingAverageCrossing = \
                IntelligentMovingAverageCrossing()

        intelligentMovingAverageCrossing.setup(
            initialData,
            trainingData
        )

        predictionArray = [intelligentMovingAverageCrossing.lastValue]
        for data in dataArray[trainingIndex:]:
            predictionArray.append(
                intelligentMovingAverageCrossing.onData(data)
            )

        trend = TrendChecker()
        return (
            trend.checkTrendNoReversal(
                list(dataArray[trainingIndex-1:]),
                predictionArray[1:]
            ),
            trend.checkPNL(
                list(dataArray[trainingIndex-1:]),
                predictionArray[1:]
            )
        )

    def testFeatureSelection(self):
        print test.testTrendChecker(5, 20)
        print test.testTrendChecker(10, 20)
        print test.testTrendChecker(5, 10)
        print test.testTrendChecker(7, 20)
        print test.testTrendChecker(14, 20)
        print test.testTrendChecker(7, 10)
        print test.testTrendChecker(7, 30)
        print test.testTrendChecker(14, 30)
        print test.testTrendChecker(7, 40)
        print "no fs", test.testIntelligentMovingAverageCrossing()
        print "fs", test.testIntelligentMovingAverageCrossing(
            featureSelection=True)

#test = Test("AAPL_data.csv")
#test.testSampleData("IBM_data.csv")
#test.testMovingAverageStremer()
#print test.testIntelligentMovingAverageCrossing()
#test.testFeatureSelection()

start_time = time.time()

mypath = '/home/marcel/TG/individual_stocks_5yr/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
better = []
worse = []
for f in onlyfiles:
    test = Test(f)
    try:
        r1 = test.testTrendChecker(5, 20)
        r2 = test.testTrendChecker(10, 20)
        r3 = test.testTrendChecker(5, 10)
        best = max([ r1[1], r2[1], r3[1] ])

        r4 = test.testIntelligentMovingAverageCrossing(featureSelection=True)
        if r4[1] > best:
            better.append((f, r1, r2, r3, r4))
        else:
            worse.append((f, r1, r2, r3, r4))
    except:
        continue

print("Better: " + str(len(better)))
print("Worse: " + str(len(worse)))
print("Better:")
for r in better:
    print(r)
print("Worse:")
for r in worse:
    print(r)

print("--- %s seconds ---" % (time.time() - start_time))
