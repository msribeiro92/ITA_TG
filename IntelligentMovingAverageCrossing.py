from sklearn.neural_network import MLPClassifier
import numpy as np

from random import randint

from MovingAverageCrossing import MovingAverageCrossing
from TrendChecker import TrendChecker
from FeatureSelection import FeatureSelection

class IntelligentMovingAverageCrossing:

    def __init__(self, featureSelection=False, initialData=[], trainingData=[]):
        """
        mac1 = MovingAverageCrossing(5, 20)
        mac2 = MovingAverageCrossing(10, 20)
        mac3 = MovingAverageCrossing(5, 10)
        mac4 = MovingAverageCrossing(7, 20)
        mac5 = MovingAverageCrossing(14, 20)
        mac6 = MovingAverageCrossing(7, 10)
        mac7 = MovingAverageCrossing(7, 30)
        mac8 = MovingAverageCrossing(14, 30)
        mac9 = MovingAverageCrossing(7, 40)
        """
        self.neuralNetwork = MLPClassifier(
            activation='relu',
            solver='lbfgs',
            alpha=1e-4,
            hidden_layer_sizes=(10),
            random_state=1
        )

        if featureSelection:
            fs = FeatureSelection()
            self.features = fs.generateFeatures(3, initialData, trainingData)
        else:
            mac1 = MovingAverageCrossing(5, 20)
            mac2 = MovingAverageCrossing(10, 20)
            mac3 = MovingAverageCrossing(5, 10)
            mac4 = MovingAverageCrossing(7, 20)
            mac5 = MovingAverageCrossing(14, 20)
            mac6 = MovingAverageCrossing(7, 10)
            mac7 = MovingAverageCrossing(7, 30)
            mac8 = MovingAverageCrossing(14, 30)
            mac9 = MovingAverageCrossing(7, 40)
            self.features = [mac1, mac2, mac3, mac4, mac5, mac6, mac7, mac8, mac9]

        self.trend = False
        self.lastValue = (False, True)
        self.trendLength = 1

        self.trendChecker = TrendChecker()
        self.lastData = None

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

        # train
        for data in trainingData:
            X = []
            for data in trainingData:
                x_i = []
                for f in self.features:
                    x_i.append(f.onData(data)[0])
                X.append(x_i)
            X = np.array(X[1:])

            y = self.trendChecker.identifyAllTrends(np.array(trainingData))
            y = np.array(y)

            self.neuralNetwork.fit(X, y)

    def onData(self, data, onlineLearning=False):
        featuresData = []
        for f in self.features:
            featuresData.append(f.onData(data)[0])
        featuresData = np.array(featuresData)
        featuresData = featuresData.reshape(1, -1)

        trend = self.neuralNetwork.predict(featuresData)
        reversal = trend != self.trend
        self.trend = trend
        self.lastValue = (trend, reversal)

        if onlineLearning and self.lastData is not None:
            y = self.trendChecker.identifyAllTrends(np.array([self.lastData, data]))
            y = np.array(y)
            self.neuralNetwork.partial_fit(featuresData, y)

        self.lastData = data

        return (trend, reversal)
