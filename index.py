import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_PT import model_forecast

def get_observation_data(data_var_ratio=0.1, time_steps=200):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    bottom_hole_pressure = all_initial_and_boundary_conditions['bottom_hole_pressure']
    bottom_hole_temperature = all_initial_and_boundary_conditions['bottom_hole_temperature']
    
    bottom_hole_pressure_data = [bottom_hole_pressure] * time_steps
    bottom_hole_temperature_data = [bottom_hole_temperature] * time_steps
    
    data = np.array([bottom_hole_pressure_data, bottom_hole_temperature_data])
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
    forecast = np.zeros((2, state.shape[1]))
    liquid_hold_up_forecast = np.zeros(state.shape[1])
    Q_O_forecast = np.zeros(state.shape[1])
    Q_W_forecast = np.zeros(state.shape[1])
    Q_G_forecast = np.zeros(state.shape[1])

    for i in range(state.shape[1]):
        bottom_hole_pressure = state[0, i]
        bottom_hole_temperature = state[1, i]
        liquid_rate = state[2, i]
        water_cut = state[3, i]
        gas_oil_ratio = state[4, i]
        bottom_hole_pressure_forecast, bottom_hole_temperature_forecast, flow_regime_forecast, liquid_hold_up, qo, qw, qg = model_forecast(
                                            bottom_hole_pressure=bottom_hole_pressure,
                                            bottom_hole_temperature=bottom_hole_temperature,
                                            liquid_rate=liquid_rate, water_cut=water_cut,
                                            gas_oil_ratio=gas_oil_ratio)
        
        forecast[0, i] = bottom_hole_pressure_forecast
        print(f"bottom_hole_pressure_forecast is: {bottom_hole_pressure_forecast}")
        forecast[1, i] = bottom_hole_temperature_forecast

        liquid_hold_up_forecast[i] = liquid_hold_up  # Storing liquid_hold_up_forecast separately
        Q_O_forecast[i] = qo  # Storing Q_O separately
        Q_W_forecast[i] = qw  # Storing Q_W separately
        Q_G_forecast[i] = qg  # Storing Q_G separately
    return forecast, liquid_hold_up_forecast, Q_O_forecast, Q_W_forecast, Q_G_forecast

def main():
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    total_obs_data, data_std = get_observation_data()
    state = get_states()
    total_time = total_obs_data.shape[1]
    n = state.shape[1]
    
    # Initialize data structures for storing results
    state_labels = ["bottom_hole_pressure", "bottom_hole_temperature", "liquid_rate", "water_cut", "gas_oil_ratio"]
    forecast_labels = ["bottom_hole_pressure_forecast", "bottom_hole_temperature_forecast"]
    time_steps = []
    state_means = {label: [] for label in state_labels}
    forecast_means = {label: [] for label in forecast_labels}
    liquid_hold_up_means = []  # Separate list for liquid_hold_up_forecast
    Q_O_means = []  # Separate list for Q_O_forecast
    Q_W_means = []  # Separate list for Q_W_forecast
    Q_G_means = []  # Separate list for Q_G_forecast
    rmses = {label: [] for label in state_labels}
    
    true_values = {
        "bottom_hole_pressure": all_initial_and_boundary_conditions['bottom_hole_pressure'],
        "bottom_hole_temperature": all_initial_and_boundary_conditions['bottom_hole_temperature'],
        "liquid_rate": all_initial_and_boundary_conditions['liquid_rate'],
        "water_cut": all_initial_and_boundary_conditions['water_cut'],
        "gas_oil_ratio": all_initial_and_boundary_conditions['gas_oil_ratio']
    }
    
    for i in range(total_time):
        priorState = state.copy()
        forecast, liquid_hold_up_forecast, Q_O_forecast, Q_W_forecast, Q_G_forecast = get_model_forecast(state=priorState)
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
        kalmanGain = calcKalmanGain(crossCov=StateForecastCrossCov,
                                    forecastCov=forecastCov, 
                                    dataErrorCov=dataErrorCov)

        # UPDATE STATE
        state = state + np.matmul(kalmanGain, (data - forecast))
        stateMean = np.mean(state, axis=1)
        
        time_steps.append(i)
        for idx, label in enumerate(state_labels):
            state_means[label].append(stateMean[idx])
        
        for idx, label in enumerate(forecast_labels):
            forecast_means[label].append(forecastMean[idx])
        
        liquid_hold_up_mean = np.mean(liquid_hold_up_forecast)  # Mean of liquid_hold_up_forecast
        liquid_hold_up_means.append(liquid_hold_up_mean)  # Append mean to list
        Q_O_mean = np.mean(Q_O_forecast)  # Mean of Q_O_forecast
        Q_O_means.append(Q_O_mean)  # Append mean to list
        Q_W_mean = np.mean(Q_W_forecast)  # Mean of Q_W_forecast
        Q_W_means.append(Q_W_mean)  # Append mean to list
        Q_G_mean = np.mean(Q_G_forecast)  # Mean of Q_G_forecast
        Q_G_means.append(Q_G_mean)  # Append mean to list

        
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
        results[f'{label}_true'] = [true_values[label]] * total_time
    for label in forecast_labels:
        results[label] = forecast_means[label]

    results['liquid_hold_up_forecast'] = liquid_hold_up_means  # Add liquid_hold_up_forecast to DataFrame
    results['Q_O_forecast'] = Q_O_means  # Add Q_O_forecast to DataFrame
    results['Q_W_forecast'] = Q_W_means  # Add Q_W_forecast to DataFrame
    results['Q_G_forecast'] = Q_G_means  # Add Q_G_forecast to DataFrame
    
    # Get user input to be added at the end of the file name and creating excel
    user_input = input("Enter a string to be added to the file name: ")
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    file_name = f'z - {user_input} - {formatted_time}.xlsx'
    results.to_excel(file_name, index=False)    
    
    # Plotting the results from Excel
    plt.ioff()
    data = pd.read_excel(f'z - {user_input} - {formatted_time}.xlsx')

    fig, axs = plt.subplots(9, 2, figsize=(12, 32))
    for idx, label in enumerate(state_labels):
        state_data = data[label]
        true_value = true_values[label]
        axs[idx, 0].plot(data['time_step'], state_data, label=label)
        axs[idx, 0].plot(data['time_step'], data[f'{label}_true'], 'r--', label='True')
        
        # Set y-axis limits to provide some margin around true values
        y_margin = (max(state_data) - min(state_data)) * 0.1
        axs[idx, 0].set_ylim(min(min(state_data), true_value) - y_margin, max(max(state_data), true_value) + y_margin)
        
        axs[idx, 0].set_xlabel('Time Step')
        axs[idx, 0].legend()

        axs[idx, 1].plot(data['time_step'], data[f'{label}_rmse'], label=f'{label} RMSE')
        axs[idx, 1].set_xlabel('Time Step')
        axs[idx, 1].legend()

    # Adding plots for liquid_hold_up_forecast, Q_O_forecast, Q_W_forecast, and Q_G_forecast
    forecast_idx = len(state_labels)
    forecast_labels = ["liquid_hold_up_forecast", "Q_O_forecast", "Q_W_forecast", "Q_G_forecast"]
    for i, forecast_label in enumerate(forecast_labels):
        axs[forecast_idx + i, 0].plot(data['time_step'], data[forecast_label], label=forecast_label)
        axs[forecast_idx + i, 0].set_xlabel('Time Step')
        axs[forecast_idx + i, 0].legend()

    plt.show()

if __name__ == "__main__":
    main()
