import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

from MovingAverageCrossing import MovingAverageCrossing
from TrendChecker import TrendChecker

class FeatureSelection:
    def __init__(self):
        self.trendChecker = TrendChecker()

    def generateFeatures(
        self,
        numberOfFeatures,
        initialData,
        trainingData
    ):
        featuresArray = []
        for i in range(len(initialData)-3):
            for j in range(i):
                featuresArray.append(MovingAverageCrossing(j+4, i+4))

        for feature in featuresArray:
            feature.setup(initialData)

        X = []
        for data in trainingData:
            x_i = []
            for feature in featuresArray:
                x_i.append(feature.onData(data)[1])
            X.append(x_i)
        X = X[1:]
        X = np.matrix(X)

        y = self.trendChecker.identifyAllReversions(np.array(trainingData))
        y = np.array(y)

        model = LogisticRegression()
        rfe = RFE(model, numberOfFeatures)
        fit = rfe.fit(X, y)

        selectedFeatures = []
        for i in range(len(featuresArray)):
            if fit.support_[i]:
                selectedFeatures.append(featuresArray[i])

        return selectedFeatures
