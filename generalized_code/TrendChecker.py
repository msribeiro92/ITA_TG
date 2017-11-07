class TrendChecker:

    def identifyAllTrends(self, rawData):
        trends = []
        lastTrend = False
        for i in range(len(rawData)-1):
            if rawData[i+1] > rawData[i]:
                trend = True
            elif rawData[i+1] < rawData[i]:
                trend = False
            else:
                trend = lastTrend

            lastTrend = trend
            trends.append(trend)

        return trends

    def identifyAllReversions(self, trendData):
        trends = self.identifyAllTrends(trendData)
        reversions = [True]
        for i in range(len(trends)-1):
            reversions.append(trends[i] != trends[i+1])

        return reversions

    def checkPrediction(self, rawData, prediction):
        if len(rawData)-1 != len(prediction):
            raise(ValueError("Raw data and prediction have diferent sizes"))

        trends = self.identifyAllTrends(rawData)
        contT = 0
        for i in range(len(trends)):
            if trends[i] == prediction[i][0]:
                contT += 1

        reversals = self.identifyAllReversions(rawData)
        contR = 0
        for i in range(len(reversals)):
            if reversals[i] == prediction[i][1]:
                contR += 1

        return float(contT) / len(trends), float(contR) / len(reversals)


    def checkPNL(self, rawData, trendPrediction):
        if len(rawData) != len(trendPrediction):
            raise(ValueError("Raw data and prediction have diferent sizes"))

        position = None
        pnl = 0

        debug = []
        for i in range(len(trendPrediction)): # trades at at most one from the last
            data = trendPrediction[i]

            if data[1]:
                if position is None:
                    if data[0]:         # uptrend: buy
                        pnl -= rawData[i]
                        position = "long"
                        debug.append(rawData[i])
                    else:              # downtrend: sell
                        pnl += rawData[i]
                        position = "short"
                        debug.append(rawData[i])
                elif position == "long":
                    if not data[0]:    # downtrend: sell
                        pnl += 2*rawData[i]
                        position = "short"
                        debug.append(rawData[i])
                else:                  # position == short
                    if data[0]:        # uptrend: buy
                        pnl -= 2*rawData[i]
                        position = "long"
                        debug.append(rawData[i])

        # close opened position
        if position == "long":
            pnl += rawData[-1]
            position = None
            debug.append(rawData[i])

        elif position == "short":
            pnl -= rawData[-1]
            position = None
            debug.append(rawData[i])

        diffs = []
        for i in range(len(debug)-1):
            diffs.append(abs(debug[i]-debug[i+1]))

        return pnl
