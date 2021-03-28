''' GOAL: CREATE A DATABASE TO BE USED IN THE NEURAL NETWORK '''


''' DEPENDENCIES '''

import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

''' IMPORT TICKERS FROM "tickers.txt" AND APPEND THEM TO WHITELIST '''

tickers = open("data/tickers.txt", "r")
whitelist = []
for l in tickers:
    whitelist.append(l.strip())

''' Import CSV's '''
start_y = 2000
end_y = 2020
dates = pd.date_range("01/01/" + str(start_y - 1), "01/01/" + str(end_y)) #Range over which we will take data from csv's, We take one extra year to be safe when calculating moving averages

df = pd.DataFrame(index = dates) #create empty DF

for name in whitelist:
        dftemp = pd.read_csv("data/" + name + ".csv", index_col='Date',
                             parse_dates=True, usecols=['Date', 'Close', 'Volume'],
                             na_values=['nan']) #Create temp df of current stock price, take only columns Date, close and Volume
        dftemp = dftemp.rename(columns = {'Close': name + " Close", 'Volume': name + " Volume"}) #Rename columns
        df = df.join(dftemp) #join temp df to DF
        if name == "^GSPC":
            df = df.dropna(subset= ["^GSPC Close"]) #drop na values from first stock


mini_batches = []
for name in whitelist:
    mini_batches.append(df[[name + " Close", name + " Volume"]])

print("number of training examples: ", len(mini_batches) * len(mini_batches[0]))


'''CALCULATING INDICATORS'''

for i in range(len(mini_batches)):
    index = whitelist[i] + " Close" 
    df_temp = mini_batches[i]
    df_temp["EMA 12"] = ta.ema(df_temp.loc[: , index], length = 12) #Calculate 12 day exponential moving average, No need for adjust as we will remove first year
    df_temp["EMA 26"] = ta.ema(df_temp.loc[: , index], length = 26) #Calculate 26 day exponential moving average
    df_temp["MACD"] = mini_batches[i]["EMA 12"] - mini_batches[i]["EMA 26"] 
    df_temp["RSI"] = ta.rsi(df_temp.loc[: , index], length = 14, scalar = 1)

print(mini_batches[0])
print(type(mini_batches))

'''
plt.plot(mini_batches[i]["EMA 12"].tolist())
plt.plot(mini_batches[i]["EMA 26"].tolist())
plt.plot(mini_batches[i].iloc[:, 0].tolist())
plt.show()

'''