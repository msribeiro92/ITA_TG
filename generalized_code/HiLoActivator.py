from MovingAverageStreamer import MovingAverageStreamer

class HiLoActivator:

    def __init__(self, period):
        self.movingAverage = MovingAverageStreamer(period)
        self.period = period
        self.trend = False  #False: downtrend; True: uptrend
        self.lastValue = (False, True)

    def getInitializationSize(self):
        return self.period + 1

    def setup(self, initialData):
        if len(initialData) < self.getInitializationSize():
            raise(ValueError("Not enough initialization data."))

        self.movingAverage.setup(initialData[:-1])

        movingAverage = self.movingAverage.lastValue
        lastClose = initialData[len(initialData)-1]

        if movingAverage > lastClose:
            trend = True
            reversal = trend != self.trend
        elif movingAverage < lastClose:
            trend = False
            reversal = trend != self.trend
        else:
            trend = self.trend
            reversal = False

        self.trend = trend
        self.lastValue = (trend, reversal)

        self.movingAverage.onData(lastClose)

    def onData(self, data):
        movingAverage = self.movingAverage.lastValue
        lastClose = data

        if movingAverage > lastClose:
            trend = True
            reversal = trend != self.trend
        elif movingAverage < lastClose:
            trend = False
            reversal = trend != self.trend
        else:
            trend = self.trend
            reversal = False

        self.trend = trend
        self.lastValue = (trend, reversal)

        self.movingAverage.onData(data)

        return (trend, reversal)
