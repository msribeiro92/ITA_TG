class TrendChecker:

    def checkTrend(self, rawData, trendPrediction):
        if len(rawData) != len(trendPrediction):
            raise(ValueError("Raw data and prediction have diferent sizes"))

        lastPrediction = trendPrediction[0][0]
        lastPredictionIndex = 0
        contReversals = 0
        contRightPredictions = 0

        for i in range(len(rawData)):
            # Look for next reversal prediction
            if not trendPrediction[i][1]:  # not reversal
                continue
            else:
                contReversals += 1
                if ((rawData[i] > rawData[lastPredictionIndex])
                    == lastPrediction):
                    contRightPredictions += 1
                lastPrediction = trendPrediction[i][0]
                lastPredictionIndex = i

        return float(contRightPredictions) / contReversals

    def checkTrendNoReversal(self, rawData, trendPrediction):
        if len(rawData)-1 != len(trendPrediction):
            raise(ValueError("Raw data and prediction have diferent sizes"))

        trends = self.identifyAllTrends(rawData)
        cont = 0
        for i in range(len(trends)):
            if trends[i] == trendPrediction[i][0]:
                cont += 1

        return float(cont) / len(trends)

    def checkSingleTrend(self, trendData, prediction):
        return (trendData[len(trendData-1)] > trendData[0]) == prediction

    def identifyTrend(self, trendData):
        return trendData[len(trendData)-1] > trendData[0]

    def identifyAllTrends(self, trendData):
        trends = []
        lastData = trendData[0]
        for i in range(len(trendData)-1):
            previousData = trendData[i]
            currentData = trendData[i+1]
            trend = currentData > previousData
            trends.append(trend)

        return trends


    def checkPNL(self):
        # TO DO
        return
