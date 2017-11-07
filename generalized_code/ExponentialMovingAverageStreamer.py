class ExponentialMovingAverageStreamer:
    def __init__(self, period):
        self.period = period
        self.alpha = 2/(1.0+period)
        self.lastValue = 0

    def setup(self, initialData):
        if len(initialData) < self.period:
            raise(ValueError("Not enough initialization data."))

        for data in initialData:
            if self.lastValue == 0:
                self.lastValue = data
            else:
                self.lastValue = self.alpha * data + (1-self.alpha) * self.lastValue

    def onData(self, data):
        exponentialMovingAverage = self.alpha * data + (1-self.alpha) * self.lastValue
        self.lastValue = exponentialMovingAverage

        return exponentialMovingAverage
