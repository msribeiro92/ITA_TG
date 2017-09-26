import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Test:
    def sampleData(self):
        df =  pd.read_csv('/home/marcel/TG/individual_stocks_5yr/AAPL_data.csv')
        df["Close"].plot()
        plt.show()

test = Test()
test.sampleData()
