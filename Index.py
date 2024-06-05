import numpy as np
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain

"""
Some Notes:
Structure of data, state, and forecast:
assuming you have seven data (p_s, t_s, p_b, t_b, f_gs, f_os, f_ws),
assuming you want to estimate gas, water, and oil in bottomhole,  (f_gb, f_wb, f_ob, p_b, t_b)
assuming you have 10 realizations (N=100) the shape of state, forecast and data at each time step will be:
state.shape = (5,100)
data.shape = (7,100)
forecast.shape = (7,100)



As for model forecast the input will be:
bottom-hole and surface pressure (p_s, p_b), bottom-hole and surface temp (t_s, t_b), bottom-hole flow rates (gas, water and oil; f_ob, f_wb, f_gb)
Output will be:
surface flow rates (f_os, f_ws, f_gs)

def model_forecast(p_s, p_b, t_s, t_b, f_ob, f_wb, f_gb)
    ...
    return f_os, f_ws, f_gs
"""


def model_forecast(X, V, time_step=1):
    X_forecast=X+V*time_step
    return X_forecast

def generate_observation_data(total_time, velocity, variance):
    data_mean = [velocity*(i+1) for i in range(total_time)]
    data_var = [variance]*total_time
    return np.array(data_mean), np.array(data_var)

def main():
    vMean=10
    xMean=0
    vVar=3
    xVar=1
    N=100
    V=(np.random.normal(vMean,vVar,N))
    V=V.reshape((1,N))
    X=np.random.normal(xMean,xVar,N)
    X=X.reshape((1,N))
    total_time= 100
    number_of_forecasts=1 # only location
    dataMean, dataVar = generate_observation_data(total_time, velocity=10, variance=1)
    # dVar=3*np.ones([t.shape[0],1])

    state=np.vstack((X,V))
    # state=state.reshape((state.shape[0],state.shape[1]))

    for i in range(total_time):
        priorState=state
        forecast=np.zeros((number_of_forecasts,N))
        for j in range(N):
            forecast[:,j]=model_forecast(X=priorState[0,j], V=priorState[1,j])
            state[0,j] = forecast[:,j] # bad coding!!!!
        # forecast=forecast.reshape((1,forecast.size))
        data=np.random.normal(dataMean[i],dataVar[i],N)
        dataErrorCov=np.array(dataVar[i])
        # dataErrorCov=dataErrorCov.reshape((dataErrorCov.shape[0],dataErrorCov.shape[0]))
        
        stateMean=np.mean(state,axis=1)
        statePert=state-np.matmul(stateMean.reshape((stateMean.size,1)),np.ones((1,N)))

        forecastMean=np.mean(forecast,axis=1)
        forecastPert=forecast-np.matmul(forecastMean.reshape((forecastMean.size,1)),np.ones((1,N)))
        forecastCov=calcCov(forecastPert)

        StateForecastCrossCov=calcCrossCov(statePert,forecastPert)

        kalmanGain=calcKalmanGain(StateForecastCrossCov,forecastCov=forecastCov,dataErrorCov=dataErrorCov)

        state=state+np.matmul(kalmanGain,(data-forecast))
        stateMean=np.mean(state,axis=1)

        print(f"Estimated location is: {stateMean[0]}\nEstimated velocity is: {stateMean[1]}\n*******")



if __name__=="__main__":
    main()