from ExponentialMovingAverageStreamer import ExponentialMovingAverageStreamer

class MovingAverageConvergenceDivergence:

    def __init__(self, shortPeriod, longPeriod, signalPeriod):
        self.shortAverage = ExponentialMovingAverageStreamer(shortPeriod)
        self.shortPeriod = shortPeriod
        self.longAverage = ExponentialMovingAverageStreamer(longPeriod)
        self.longPeriod = longPeriod
        self.signalAverage = ExponentialMovingAverageStreamer(signalPeriod)
        self.signalPeriod = signalPeriod

        self.trend = False  #False: downtrend; True: uptrend
        self.lastValue = (False, True)

    def getInitializationSize(self):
        return self.longPeriod + self.signalPeriod

    def setup(self, initialData):
        if len(initialData) < self.getInitializationSize():
            raise(ValueError("Not enough initialization data."))

        self.shortAverage.setup(initialData[:self.longPeriod])
        self.longAverage.setup(initialData[:self.longPeriod])

        initialValuesMACD = []
        for data in initialData[self.longPeriod:]:
            macd = self.longAverage.onData(data) - self.shortAverage.onData(data)
            initialValuesMACD.append(macd)
        self.signalAverage.setup(initialValuesMACD)

        macdLine = self.longAverage.lastValue - self.shortAverage.lastValue
        signalLine = self.signalAverage.lastValue

        if macdLine > signalLine:
            trend = True
            reversal = trend != self.trend
        elif macdLine < signalLine:
            trend = False
            reversal = trend != self.trend
        else:
            trend = self.trend
            reversal = False

        self.trend = trend
        self.lastValue = (trend, reversal)

    def onData(self, data):
        macdLine = self.longAverage.onData(data) - self.shortAverage.onData(data)
        signalLine = self.signalAverage.onData(macdLine)

        if macdLine > signalLine:
            trend = True
            reversal = trend != self.trend
        elif macdLine < signalLine:
            trend = False
            reversal = trend != self.trend
        else:
            trend = self.trend
            reversal = False

        self.trend = trend
        self.lastValue = (trend, reversal)

        return (trend, reversal)
