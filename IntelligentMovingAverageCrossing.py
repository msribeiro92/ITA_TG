from sklearn.neural_network import MLPClassifier
import numpy as np

from MovingAverageCrossing import MovingAverageCrossing

class IntelligentMovingAverageCrossing:

    def __init__(self):
        mac1 = MovingAverageCrossing(5, 20)
        mac2 = MovingAverageCrossing(10, 20)
        mac3 = MovingAverageCrossing(5, 10)
        self.neuralNetwork = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(5,),
            random_state=1
        )

        self.features = [mac1, mac2, mac3]
        self.trend = False
        self.lastValue = (False, True)


    def setup(self, initialData, trainingData):
        # Setup
        longPeriods = []
        for f in self.features:
            longPeriods.append(f.longPeriod)
        longestPeriod = max(longPeriods)

        if len(initialData) < longestPeriod:
            raise(ValueError("Not enough initialization data."))

        for f in self.features:
            f.setup(initialData)

        # Train
        X = []
        for data in trainingData:
            x_i = []
            for f in self.features:
                x_i.append(f.onData(data)[0])
            X.append(x_i)

        y = []
        for x_i in X:
            trendCount = 0
            for i in x_i:
                if i > 0:
                    trendCount += 1
                else:
                    trendCount -=1
            trend = trendCount > 0
            y.append(trend)

        X = np.array(X)
        y = np.array(y)
        self.neuralNetwork.fit(X, y)

        lastTrends = []
        for f in self.features:
            lastTrends.append(f.trend)
        trendCount = 0
        for i in lastTrends:
            if i > 0:
                trendCount += 1
            else:
                trendCount -=1
        trend = trendCount > 0
        self.trend = trend
        self.lastValue = (trend, True)

    def onData(self, data):
        featuresData = []
        for f in self.features:
            featuresData.append(f.onData(data)[0])
        featuresData = np.array(featuresData)
        featuresData = featuresData.reshape(1, -1)

        trend = self.neuralNetwork.predict(featuresData)
        reversal = trend != self.trend
        self.trend = trend
        self.lastValue = (trend, reversal)

        return (trend, reversal)
