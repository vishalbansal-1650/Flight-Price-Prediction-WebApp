import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor

import pickle
import warnings
warnings.filterwarnings(action='ignore')

df = pd.read_csv('flight-data-cleaned.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)
print(df.head())

x = df.drop('Price',axis=1)
y = df['Price']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=101)

CB_model = CatBoostRegressor()
CB_model.fit(x_train,y_train)

y_train_pred = CB_model.predict(x_train)
y_test_pred = CB_model.predict(x_test)

pickle.dump(CB_model,open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
print(y_test_pred)
