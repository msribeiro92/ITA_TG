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
        for i in range(len(initialData)):
            for j in range(i):
                featuresArray.append( MovingAverageCrossing(j+1, i+1))

        for feature in featuresArray:
            feature.setup(initialData)

        X = []
        for data in trainingData:
            x_i = []
            for feature in featuresArray:
                x_i.append(feature.onData(data)[0])
            X.append(x_i)

        y = self.trendChecker.identifyAllTrends(np.array(trainingData))

        model = LogisticRegression()
        rfe = RFE(model, numberOfFeatures)
        fit = rfe.fit(X[1:], y)

        selectedFeatures = []
        for i in range(len(featuresArray)):
            if fit.support_[i]:
                selectedFeatures.append(featuresArray[i])

        return selectedFeatures
