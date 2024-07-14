import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_mechanical import model_forecast

def get_observation_data(data_var_ratio=0.1, time_steps=200):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    data = np.array([[210.3] * time_steps])
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
    
    # Initialize data structures for storing results
    state_labels = ["bottom_hole_pressure", "bottom_hole_temperature", "liquid_rate", "water_cut", "gas_oil_ratio"]
    time_steps = []
    state_means = {label: [] for label in state_labels}
    rmses = {label: [] for label in state_labels}
    
    for i in range(total_time):
        priorState = state.copy()
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
        for idx, label in enumerate(state_labels):
            state_means[label].append(stateMean[idx])
        
        # Calculate RMSE for each state variable
        for idx, label in enumerate(state_labels):
            rmse = np.sqrt(np.mean((stateMean[idx] - np.mean(priorState, axis=1)[idx])**2))
            rmses[label].append(rmse)
        
        print(f"Estimated {state_labels[0]} is: {stateMean[0]}\n"
              f"Estimated {state_labels[1]} is: {stateMean[1]}\n"
              f"Estimated {state_labels[2]} is: {stateMean[2]}\n"
              f"Estimated {state_labels[3]} is: {stateMean[3]}\n"
              f"Estimated {state_labels[4]} is: {stateMean[4]}\n"
              f"RMSE at time step {i}:\n"
              f" - {state_labels[0]}: {rmses[state_labels[0]][-1]}\n"
              f" - {state_labels[1]}: {rmses[state_labels[1]][-1]}\n"
              f" - {state_labels[2]}: {rmses[state_labels[2]][-1]}\n"
              f" - {state_labels[3]}: {rmses[state_labels[3]][-1]}\n"
              f" - {state_labels[4]}: {rmses[state_labels[4]][-1]}\n"
              "*******")
    
    # Create DataFrame to store results
    results = pd.DataFrame({'time_step': time_steps})
    for label in state_labels:
        results[label] = state_means[label]
        results[f'{label}_rmse'] = rmses[label]
    
    # Save results to Excel
    # Get the current date and time
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    results.to_excel(f'state_and_rmse_results - {formatted_time}.xlsx', index=False)
    
    # Plotting the results from Excel
    plt.ioff()
    data = pd.read_excel(f'state_and_rmse_results - {formatted_time}.xlsx')

    fig, axs = plt.subplots(5, 2, figsize=(12, 24))
    for idx, label in enumerate(state_labels):
        axs[idx, 0].plot(data['time_step'], data[label], label=label)
        axs[idx, 0].set_xlabel('Time Step')
        axs[idx, 0].set_ylabel(label)
        axs[idx, 0].legend()

        axs[idx, 1].plot(data['time_step'], data[f'{label}_rmse'], label=f'{label} RMSE')
        axs[idx, 1].set_xlabel('Time Step')
        axs[idx, 1].set_ylabel(f'{label} RMSE')
        axs[idx, 1].legend()

    plt.show()

if __name__ == "__main__":
    main()
