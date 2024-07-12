import numpy as np
import matplotlib.pyplot as plt
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain, calculate_rmse
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_mechanical import model_forecast

def get_observation_data(data_var_ratio=0.01, time_steps=100):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    data = np.array([[988] * time_steps])
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
    
    # Enable interactive mode
    plt.ion()
    fig, axs = plt.subplots(5, 1, figsize=(12, 18))
    
    # Initialize the plots for each state variable
    state_labels = ["bottom_hole_pressure", "bottom_hole_temperature", "liquid_rate", "water_cut", "gas_oil_ratio"]
    lines = {}
    for idx, label in enumerate(state_labels):
        lines[label], = axs[idx].plot([], [], label=label)
        axs[idx].set_xlabel('Time Step')
        axs[idx].set_ylabel(label)
        axs[idx].legend()
    
    time_steps = []
    state_means = {label: [] for label in state_labels}
    
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
        for idx, label in enumerate(state_labels):
            state_means[label].append(stateMean[idx])
        
        # Update the plots
        for idx, label in enumerate(state_labels):
            lines[label].set_data(time_steps, state_means[label])
            axs[idx].relim()
            axs[idx].autoscale_view()

        # Calculate RMSE
        # for idx, label in enumerate(state_labels):
        #     rmse = calculate_rmse(state_means[label][-1], ground_truth[0, i])  # Replace 0 with actual index for each state
        #     rmses[label].append(rmse)
        #     print(f"RMSE for {label} at time step {i}: {rmse}")    
        plt.pause(0.01)
        
        print(f"Estimated {state_labels[0]} is: {stateMean[0]}\n"
              f"Estimated {state_labels[1]} is: {stateMean[1]}\n"
              f"Estimated {state_labels[2]} is: {stateMean[2]}\n"
              f"Estimated {state_labels[3]} is: {stateMean[3]}\n"
              f"Estimated {state_labels[4]} is: {stateMean[4]}\n"
              "*******")
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
