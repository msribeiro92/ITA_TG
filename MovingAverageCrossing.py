import MovingAverageStreamer

class MovingAverageCrossing:
    def __init__(self, shortPeriod, longPeriod):
        self.shortAverage = MovingAverageStreamer(shortPeriod)
        self.shortPeriod = shortPeriod
        self.longAverage = MovingAverageStreamer(longPeriod)
        self.longPeriod = longPeriod
        self.trend = False  #False: downtrend; True: uptrend#

    def setup(self, initialData):
        if len(initialData) < min(self.shortPeriod, self.longPeriod)
            raise(ValueError("Not enough initialization data."))

        self.shortAverage.setup(initialData)
        self.longAverage.setup(initialData)

    def onData(self, data):
        shortAverage = self.shortAverage.onData(data)
        longAverage = self.longAverage.onData(data)

        if shortAverage > longAverage:
            trend = True
            reversal = trend != self.trend
        elif shortAverage < longAverage:
            trend = False
            reversal = trend != self.trend
        else:
            trend = self.trend
            reversal = False

        return (trend, reverval)
