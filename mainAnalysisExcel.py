import numpy as np
import pandas as pd
# Import the required functions from your modules
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain, calculate_rmse
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_mechanical import model_forecast

def get_observation_data(data_var_ratio=0.01, time_steps=100):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    # data = np.array([[988] * time_steps])
    data = np.array([[217] * time_steps])
    data_std = data_var_ratio * data
    return data, data_std

def get_states(n=100, state_var_ratio=0.01):
    required_states = ["bottom_hole_pressure", "bottom_hole_temperature",
                       "liquid_rate", "water_cut", "gas_oil_ratio"]
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    state_mean = []
    for state in required_states:
        state_mean.append(all_initial_and_boundary_conditions[state])
    state_mean = np.array(state_mean)
    state_std = state_mean * state_var_ratio
    state_var = np.diag(state_std * state_std)
    states = np.random.multivariate_normal(state_mean, state_var, n)
    return states.T

def get_model_forecast(state):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    forecast = np.zeros((1, state.shape[1]))
    for i in range(state.shape[1]):
        bottom_hole_pressure = state[0, i]
        bottom_hole_temperature = state[1, i]
        liquid_rate = state[2, i]
        water_cut = state[3, i]
        gas_oil_ratio = state[4, i]
        bottom_hole_pressure_forecast = model_forecast(bottom_hole_pressure=bottom_hole_pressure,
                                                       bottom_hole_temperature=bottom_hole_temperature,
                                                       liquid_rate=liquid_rate, water_cut=water_cut,
                                                       gas_oil_ratio=gas_oil_ratio)
        forecast[0, i] = bottom_hole_pressure_forecast
    return forecast

def main():
    total_obs_data, data_std = get_observation_data()
    state = get_states()
    total_time = total_obs_data.shape[1]
    n = state.shape[1]
    
    time_steps = []
    state_means = {label: [] for label in ["bottom_hole_pressure", "bottom_hole_temperature", "liquid_rate", "water_cut", "gas_oil_ratio"]}
    
    for i in range(total_time):
        priorState = state
        forecast = get_model_forecast(state=priorState)
        data_mean_i = total_obs_data[:, i]
        data_var_i = np.diag(data_std[:, i] * data_std[:, i])
        data = np.random.multivariate_normal(data_mean_i, data_var_i, n).T
        dataErrorCov = data_var_i
        
        stateMean = np.mean(state, axis=1)
        statePert = state - np.outer(stateMean, np.ones(n))
        forecastMean = np.mean(forecast, axis=1)
        forecastPert = forecast - np.outer(forecastMean, np.ones(n))
        forecastCov = calcCov(forecastPert)
        StateForecastCrossCov = calcCrossCov(statePert, forecastPert)
        kalmanGain = calcKalmanGain(StateForecastCrossCov, forecastCov=forecastCov, dataErrorCov=dataErrorCov)
        state = state + np.matmul(kalmanGain, (data - forecast))
        stateMean = np.mean(state, axis=1)
        
        time_steps.append(i)
        for idx, label in enumerate(state_means):
            state_means[label].append(stateMean[idx])
        
        print(f"Estimated bottom_hole_pressure is: {stateMean[0]}\n"
              f"Estimated bottom_hole_temperature is: {stateMean[1]}\n"
              f"Estimated liquid_rate is: {stateMean[2]}\n"
              f"Estimated water_cut is: {stateMean[3]}\n"
              f"Estimated gas_oil_ratio is: {stateMean[4]}\n"
              "*******")
    
    # Create a DataFrame with the results
    results_df = pd.DataFrame(state_means, index=time_steps)
    
    # Save the DataFrame to an Excel file
    results_df.to_excel('output_data.xlsx', index_label='Time Step')

if __name__ == "__main__":
    main()
