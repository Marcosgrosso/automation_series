import pandas as pd
from datetime import date, timedelta, datetime
from meteostat import Point, Daily
import statsmodels.api as sm

def read_data():
        # Set time period
    start = datetime(2010, 1, 1)
    end = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
    # Create Point for Vancouver, BC
    vancouver = Point(49.2497, -123.1193, 70)
    #campinas = Point(-22.9056, -47.0608, 686)
    #saopaulo = Point(-23.5475, -46.6361, 769)

    # Get daily data for 2018
    data = Daily(vancouver, start, end)
    data = data.fetch()
    data = data[['tavg', 'prcp']]

    return data

def predict():
        data = read_data()
        returns = data['tavg']
        valor_ontem = returns.tail(1)
        model =  sm.tsa.statespace.SARIMAX(returns , order=(1,1,3), seasonal_order=(0,1,1,7),
                                    enforce_stationarity=False, enforce_invertibility=False, freq='D')
        model = model.fit()

        forecast = model.get_forecast(steps=1)  # Previsão para 1 período à frente
        conf_interval = forecast.conf_int(alpha=0.05)  # Intervalo de confiança de 95%
        
        pred = forecast.predicted_mean[0] # Previsão um dia a frente
        lower_bound = conf_interval.iloc[0, 0]  # Limite inferior do intervalo de confiança
        upper_bound = conf_interval.iloc[0, 1]  # Limite superior do intervalo de confiança

        prediction = round(float(pred),4)
        lower_bound = round(float(lower_bound),4)
        upper_bound = round(float(upper_bound),4)
        valor_ontem = round(float(valor_ontem),4)

        data_atual = date.today()
        data_amanha = data_atual + timedelta(days=1)

        return [str(data_amanha), prediction, lower_bound, upper_bound]
