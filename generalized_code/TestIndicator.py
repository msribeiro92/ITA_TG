import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
import time
import operator
import sys
import copy

from FeatureSelection import FeatureSelection
from IntelligentIndicator import IntelligentIndicator
from TrendChecker import TrendChecker

class TestIndicator:

    def __init__(self, fileName):
        self.dataFrame =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/' + fileName)

    def testIndicator(self, indicator, initializationIndex, trainingIndex, finalIndex):
        dataArray = self.dataFrame["Close"]
        dataArray = np.array(dataArray)
        indicator.setup(dataArray[:indicator.getInitializationSize()])

        predictionArray = [indicator.lastValue]
        for data in dataArray[indicator.getInitializationSize():finalIndex]:
            predictionArray.append(indicator.onData(data))

        trend = TrendChecker()

        return (
            trend.checkPrediction(
                list(dataArray[trainingIndex-1:finalIndex]),
                predictionArray[trainingIndex-indicator.getInitializationSize()+
                    1:finalIndex-indicator.getInitializationSize()+1]
            ),
            trend.checkPNL(
                list(dataArray[trainingIndex:finalIndex]),
                predictionArray[trainingIndex-indicator.getInitializationSize()+
                    1:finalIndex-indicator.getInitializationSize()+1]
            )
        )

    def testIntelligentIndicator(
        self,
        indicatorType="MovingAverageCrossing",
        nFeatures=3,
        nOutputs=1,
        architecture=(15,15),
        trainingIndex=272,
        finalIndex=294
    ):
        dataArray = self.dataFrame["Close"]
        dataArray = np.array(dataArray)
        initializationIndex = 40
        initialData = dataArray[:initializationIndex]
        trainingData = dataArray[initializationIndex:trainingIndex]
        if finalIndex == -1:
            finalIndex = len(dataArray)

        fs = FeatureSelection()
        features = fs.generateFeatures(indicatorType, nFeatures, initialData, trainingData)
        featuresForTest = copy.deepcopy(features)

        intelligentIndicator = IntelligentIndicator(
                features,
                nOutputs=nOutputs,
                architecture=architecture
            )

        intelligentIndicator.setup(
            initialData,
            trainingData
        )

        predictionArray = [intelligentIndicator.lastValue]
        for data in dataArray[trainingIndex:finalIndex]:
            predictionArray.append(intelligentIndicator.onData(data))

        trend = TrendChecker()

        answer = []
        for f in featuresForTest:
            answer.append(self.testIndicator(f, initializationIndex, trainingIndex, finalIndex))

        answer.append(
            (
                trend.checkPrediction(
                    list(dataArray[trainingIndex-1:finalIndex]),
                    predictionArray[1:]
                ),
                trend.checkPNL(
                    list(dataArray[trainingIndex:finalIndex]),
                    predictionArray[1:]
                )
            )
        )
        answer.append(-dataArray[trainingIndex]+dataArray[finalIndex-1])
        answer.append(abs(dataArray[trainingIndex]-dataArray[finalIndex-1]))

        return answer

    @staticmethod
    def testPrediction(
        testType="trend",
        testMode="every",
        indicatorType="MovingAverageCrossing",
        verbose=True,
        nFeatures=3,
        nOutputs=1,
        architecture=(15,15),
        trainingIndex=106,
        finalIndex=128
    ):
        mypath = '/home/marcel/TG/individual_stocks_5yr/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        better = []
        equal = []
        worse = []
        scores = []
        score = -1
        for f in onlyfiles:
            test = TestIndicator(f)
            try:
                answer = test.testIntelligentIndicator(
                    indicatorType="MovingAverageCrossing",
                    nFeatures=nFeatures,
                    nOutputs=nOutputs,
                    architecture=architecture,
                    trainingIndex=trainingIndex,
                    finalIndex=finalIndex,
                )

                values = []
                for i in range(nFeatures):
                    if testType == "trend":
                        values.append(answer[i][0][0])
                    elif testType == "reversal":
                        values.append(answer[i][0][1])
                    elif testType == "PnL":
                        values.append(answer[i][1])
                if testType == "trend":
                    prediction = answer[nFeatures][0][0]
                elif testType == "reversal":
                    prediction = answer[nFeatures][0][1]
                elif testType == "PnL":
                    prediction = answer[nFeatures][1]

                if testMode == "every":
                    if prediction > max(values):
                        better.append((f, answer))
                    elif prediction == max(values):
                        equal.append((f, answer))
                    else:
                        worse.append((f, answer))
                else:  # testMode == "some"
                    scores.append(sum(i < prediction for i in values))
            except:
                continue

        if testMode == "every" and verbose:
            print("Better: " + str(len(better)))
            print("Equal: " + str(len(equal)))
            print("Worse: " + str(len(worse)))
            print("Score: " + str(score))
            print("Better:")
            for r in better:
                print(r)
            print("Equal:")
            for r in equal:
                print(r)
            print("Worse:")
            for r in worse:
                print(r)

        if testMode == "every":
            score = (len(better) + len(equal)) * 1.0 / (len(better) + len(equal) + len(worse))
        else:
            score = sum(scores) * 1.0 /(nFeatures * len(scores))

        return score

    @staticmethod
    def runMultipleTests(
        fileName,
        testType,
        testMode,
        indicatorType,
        trainingIndex,
        finalIndex
    ):
        start_time = time.time()

        f = open(fileName, 'w')
        numberOfFeatures = [3, 5, 7, 9]
        numberOfOutputs = [1, 2]
        architectures = [(10), (20), (10, 10), (20, 20)]

        answers = {}
        for nFeatures in numberOfFeatures:
            for nOutputs in numberOfOutputs:
                for architecture in architectures:
                        key = str((
                            nFeatures,
                            nOutputs,
                            architecture
                        ))
                        answers[key] = TestIndicator.testPrediction(
                            testType=testType,
                            testMode=testMode,
                            indicatorType=indicatorType,
                            verbose=False,
                            nFeatures=nFeatures,
                            nOutputs=nOutputs,
                            architecture=architecture,
                            trainingIndex=trainingIndex,
                            finalIndex=finalIndex,
                        )
        sortedAns = sorted(answers.iteritems(), key=operator.itemgetter(1))
        f.write(fileName + "\n")
        f.write("Sorted Answers:\n")
        for ans in sortedAns:
            f.write(ans[0] + ": " + str(ans[1]) + "\n")

        f.write("--- %s seconds ---" % (time.time() - start_time))

    @staticmethod
    def fullClassifierTest(
        fileName,
        indicatorType="MovingAverageCrossing",
        nFeatures=3,
        nOutputs=1,
        architecture=(15,15),
        trainingIndex=106,
        finalIndex=128
    ):
        start_time = time.time()

        fi = open(fileName, 'w')
        mypath = '/home/marcel/TG/individual_stocks_5yr/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        performance = {
            "trend": [],
            "meanTrendAccuracy": 0,
            "reversal": [],
            "meanReversalAccuracy": 0,
            "PnL": [],
            "meanPnL": 0,
            "BaH": 0,
            "BSaH": 0,
        }
        for testType in ["trend", "reversal", "PnL"]:
            performance[testType] = [0 for i in range(nFeatures)]

        totalFiles = 0
        for f in onlyfiles:
            test = TestIndicator(f)
            try:
                answer = test.testIntelligentIndicator(
                    indicatorType=indicatorType,
                    nFeatures=nFeatures,
                    nOutputs=nOutputs,
                    architecture=architecture,
                    trainingIndex=trainingIndex,
                    finalIndex=finalIndex,
                )

                for testType in ["trend", "reversal", "PnL"]:
                    if testType == "trend":
                        prediction = answer[nFeatures][0][0]
                        performance["meanTrendAccuracy"] += prediction
                    elif testType == "reversal":
                        prediction = answer[nFeatures][0][1]
                        performance["meanReversalAccuracy"] += prediction
                    elif testType == "PnL":
                        prediction = answer[nFeatures][1]
                        performance["meanPnL"] += prediction
                        performance["BaH"] += prediction >= answer[nFeatures+1]
                        performance["BSaH"] += prediction >= answer[nFeatures+2]

                    for i in range(nFeatures):
                        if testType == "trend":
                            performance["trend"][i] += prediction >= answer[i][0][0]
                        elif testType == "reversal":
                            performance["reversal"][i] += prediction >= answer[i][0][1]
                        elif testType == "PnL":
                            performance["PnL"][i] += prediction >= answer[i][1]

                totalFiles += 1
            except:
                continue

        for testType in ["trend", "reversal", "PnL"]:
            for i in range(nFeatures):
                performance[testType][i] = performance[testType][i] * 1.0 / totalFiles
        for result in ["BaH", "BSaH", "meanTrendAccuracy", "meanReversalAccuracy", "meanPnL"]:
            performance[result] = performance[result] * 1.0 / totalFiles

        fi.write(fileName + "\n")
        fi.write(str(performance)+"\n")
        fi.write("--- %s seconds ---" % (time.time() - start_time))

"""
TestIndicator.runMultipleTests(
    sys.argv[1],
    sys.argv[2],
    sys.argv[3],
    sys.argv[4],
    106,#int(sys.argv[4]),
    128#int(sys.argv[5])
)
"""
TestIndicator.fullClassifierTest(
    sys.argv[1],
    indicatorType="MovingAverageConvergenceDivergence",
    nFeatures=7,
    nOutputs=1,
    architecture=(20),
    trainingIndex=int(sys.argv[2]),
    finalIndex=int(sys.argv[3])
)
