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

    def checkPNL(self):
        # TO DO
        return
