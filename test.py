import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from MovingAverageStreamer import MovingAverageStreamer

class Test:
    def __init__(self):
        self.dataFrame =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/AAPL_data.csv')

    def testSampleData(self):
        self.dataFrame["Close"].plot()
        plt.show()


    def testMovingAverageStremmer(self):
        dataArray = self.dataFrame["Close"]

        movingAverageStreamer = MovingAverageStreamer(20)
        movingAverageStreamer.setup(dataArray[:20])

        movingAverageArray = [movingAverageStreamer.lastValue]
        for data in dataArray[20:]:
            movingAverageArray.append(movingAverageStreamer.onData(data))

        plt.plot(range(len(dataArray)-19), dataArray[19:])
        plt.plot(movingAverageArray, 'r')
        plt.show()


test = Test()
#test.testSampleData()
test.testMovingAverageStremmer()
