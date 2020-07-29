import pandas as pd


data=pd.read_csv("../media/info/info.csv",header=None,index_col=0)
print(type(data.loc["P8hYgZ6L7F",2]))


