from sklearn.neural_network import MLPClassifier
import numpy as np

from random import randint

from MovingAverageCrossing import MovingAverageCrossing
from TrendChecker import TrendChecker
from FeatureSelection import FeatureSelection

class IntelligentMovingAverageCrossing:

    def __init__(
        self,
        featureSelection=False,
        nFeatures=3,
        nOutputs=1,
        architecture=(15,15),
        initialData=[],
        trainingData=[]
    ):

        self.neuralNetwork = MLPClassifier(
            activation='logistic',
            solver='lbfgs',
            alpha=1e-4,
            hidden_layer_sizes=architecture,
            random_state=1
        )

        if featureSelection:
            fs = FeatureSelection()
            self.features = fs.generateFeatures(nFeatures, initialData, trainingData)
        else:
            if nFeatures > 9:
                raise(ValueError("MaxFeature == 9 when featureSelection == False"))
            mac1 = MovingAverageCrossing(5, 20)
            mac2 = MovingAverageCrossing(10, 20)
            mac3 = MovingAverageCrossing(5, 10)
            mac4 = MovingAverageCrossing(7, 20)
            mac5 = MovingAverageCrossing(14, 20)
            mac6 = MovingAverageCrossing(7, 10)
            mac7 = MovingAverageCrossing(7, 30)
            mac8 = MovingAverageCrossing(14, 30)
            mac9 = MovingAverageCrossing(7, 40)
            features = [mac1, mac2, mac3, mac4, mac5, mac6, mac7, mac8, mac9]
            self.features = features[:nFeatures]

        self.trend = False
        self.lastValue = (False, True)

        self.nOutputs = nOutputs
        self.trendChecker = TrendChecker()

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
