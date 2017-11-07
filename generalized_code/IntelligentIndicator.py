from sklearn.neural_network import MLPClassifier
import numpy as np

from random import randint

from TrendChecker import TrendChecker

class IntelligentIndicator:

    def __init__(
        self,
        features,
        nOutputs=1,
        architecture=(15,15)
    ):
        self.neuralNetwork = MLPClassifier(
            activation='logistic',
            solver='lbfgs',
            alpha=1e-4,
            hidden_layer_sizes=architecture,
            random_state=1
        )

        self.features = features

        self.trend = False
        self.lastValue = (False, True)

        self.nOutputs = nOutputs
        self.trendChecker = TrendChecker()

    def setup(self, initialData, trainingData):
        # Setup
        initializationPeriods = []
        for f in self.features:
            initializationPeriods.append(f.getInitializationSize())
        longestPeriod = max(initializationPeriods)

        if len(initialData) < longestPeriod:
            raise(ValueError("Not enough initialization data."))

        for f in self.features:
            f.setup(initialData)

        # train prediction
        X = []
        for data in trainingData:
            x_i = []
            for f in self.features:
                x_i.append(f.onData(data)[0])
            X.append(x_i)
        X = np.array(X[1:])

        if self.nOutputs == 2:
            y = []
            y.append(self.trendChecker.identifyAllTrends(np.array(trainingData)))
            y.append(self.trendChecker.identifyAllReversions(np.array(trainingData)))
            y = np.matrix(y)
            y = y.getT()
        else:
            y = self.trendChecker.identifyAllTrends(np.array(trainingData))
        self.neuralNetwork.fit(X, y)

    def onData(self, data):
        featuresData = []
        for f in self.features:
            featuresData.append(f.onData(data)[0])
        featuresData = np.array(featuresData)
        featuresData = featuresData.reshape(1, -1)

        if self.nOutputs == 2:
            self.lastValue = self.neuralNetwork.predict(featuresData)
            self.lastValue = (self.lastValue[0][0], self.lastValue[0][1])
        else:
            trend = self.neuralNetwork.predict(featuresData)
            reversal = trend != self.trend
            self.trend = trend
            self.lastValue = (trend, reversal)

        return self.lastValue
