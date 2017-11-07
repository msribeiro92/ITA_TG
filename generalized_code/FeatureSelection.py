import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

from MovingAverageCrossing import MovingAverageCrossing
from MovingAverageConvergenceDivergence import MovingAverageConvergenceDivergence
from HiLoActivator import HiLoActivator
from TrendChecker import TrendChecker

class FeatureSelection:
    def __init__(self):
        self.trendChecker = TrendChecker()

    def generateFeatures(
        self,
        indicator,
        numberOfFeatures,
        initialData,
        trainingData
    ):
        if indicator == "MovingAverageCrossing":
            featuresArray = self.generateFeaturesMovingAverageCrossing(
                initialData
            )
        elif indicator == "MovingAverageConvergenceDivergence":
            featuresArray =  self.generateFeaturesMovingAverageConvergenceDivergence(
                initialData
            )
        elif indicator == "HiLoActivator":
            featuresArray =  self.generateFeaturesHiLoActivator(
                initialData
        )

        return self.selectFeatures(numberOfFeatures, featuresArray, initialData, trainingData)

    def selectFeatures(self, numberOfFeatures, featuresArray, initialData, trainingData):
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


    def generateFeaturesMovingAverageCrossing(
        self,
        initialData
    ):
        featuresArray = []
        for i in range(len(initialData)-3):
            for j in range(i):
                featuresArray.append(MovingAverageCrossing(j+4, i+4))

        return featuresArray

    def generateFeaturesMovingAverageConvergenceDivergence(
        self,
        initialData
    ):
        featuresArray = []
        for i in range(len(initialData)-3):
            for j in range(i):
                for k in range(len(initialData)-i-3):
                    featuresArray.append(
                        MovingAverageConvergenceDivergence(j+4, i+4, k+4)
                    )

        return featuresArray

    def generateFeaturesHiLoActivator(
        self,
        initialData
    ):
        featuresArray = []
        for i in range(len(initialData)-3):
            featuresArray.append(HiLoActivator(i+3))
        return featuresArray
