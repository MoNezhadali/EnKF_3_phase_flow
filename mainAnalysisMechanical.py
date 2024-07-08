import numpy as np
import matplotlib.pyplot as plt
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_mechanical import model_forecast

""" 
Some Notes:
Structure of data, state, and forecast:
assuming you have seven data (p_s, t_s, p_b, t_b, f_gs, f_os, f_ws),
assuming you want to estimate gas, water, and oil in bottomhole,  (f_gb, f_wb, f_ob, p_b, t_b)
assuming you have 100 realizations (N=100) the shape of state, forecast and data at each time step will be:
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

optional_data = ["bottom_hole_pressure", "bottom_hole_temperature", \
                                          "surface_pressure", "surface_temperature"]

def get_observation_data(optional_data = [],
                                          data_var_ratio = 0.01, time_steps=100):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    file_path = './data/obs_data.csv'

    # Read the CSV file into a NumPy array
    # data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
    data = np.array([[988]*100])

    data_std = data_var_ratio * data
    # data_var = np.diag(data_std*data_std)
    # observation_data = np.random.multivariate_normal(data, data_var, time_steps)
    # data_std is assumed to be constant throughout the entire period
    return data, data_std

# print(get_observation_data())
 
def get_states(n=100, optional_states=[], state_var_ratio=0.01):
    required_states = ["bottom_hole_pressure", "bottom_hole_temperature",
                        "liquid_rate", "water_cut", "gas_oil_ratio"]
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    all_states = optional_states + required_states
    state_mean = []
    for state in all_states:
        state_mean.append(all_initial_and_boundary_conditions[state])
    state_mean = np.array(state_mean)
    state_std = state_mean * state_var_ratio
    state_var = np.diag(state_std*state_std)
    states=np.random.multivariate_normal(state_mean,state_var,n)
        
    return states.T

def get_model_forecast(state):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    # P_surface = all_initial_and_boundary_conditions["surface_pressure"]
    # T_surface = all_initial_and_boundary_conditions["surface_temperature"]
    forecast = np.zeros((1, state.shape[1]))
    for i in range(state.shape[1]):
        bottom_hole_pressure = state[0,i]
        bottom_hole_temperature = state[1,i]
        liquid_rate = state[2,i]
        water_cut = state[3,i]
        gas_oil_ratio = state[4,i]
        bottom_hole_pressure_forecast = model_forecast( bottom_hole_pressure=bottom_hole_pressure,
                                                                       bottom_hole_temperature=bottom_hole_temperature,
                                                                       liquid_rate=liquid_rate, water_cut=water_cut,
                                                                       gas_oil_ratio=gas_oil_ratio)
        # forecast[1:5,i] = state[1:5,i]
        forecast[0,i]=bottom_hole_pressure_forecast
    
    return forecast
 
 
 
def main(): 
    total_obs_data, data_std = get_observation_data(optional_data=optional_data)
    state = get_states(optional_states=[])

    total_time = total_obs_data.shape[1]
    n = state.shape[1]

    # Initialize lists to store estimated flow rates for plotting
    # estimated_bottom_hole_flow_rate_oil = []
    # estimated_bottom_hole_flow_rate_gas = []
    # estimated_bottom_hole_flow_rate_water = []

    # Enable interactive mode
    # plt.ion()
    # fig, axs = plt.subplots(3, 1, figsize=(12, 12))
    
    # Initialize the plots
    # lines = {}
    # lines['bottom_hole_flow_rate_oil'], = axs[0].plot([], [], label='Oil Flow Rate')
    # axs[0].set_xlabel('Time Step')
    # axs[0].set_ylabel('Flow Rate')
    # axs[0].legend()

    # lines['bottom_hole_flow_rate_gas'], = axs[1].plot([], [], label='Gas Flow Rate')
    # axs[1].set_xlabel('Time Step')
    # axs[1].set_ylabel('Flow Rate')
    # axs[1].legend()

    # lines['bottom_hole_flow_rate_water'], = axs[2].plot([], [], label='Water Flow Rate')
    # axs[2].set_xlabel('Time Step')
    # axs[2].set_ylabel('Flow Rate')
    # axs[2].legend()

    time_steps = []

    for i in range(total_time):
        priorState = state
        forecast = get_model_forecast(state=priorState)
        data_mean_i = total_obs_data[:, i]
        data_var_i = np.diag(data_std[:,i] * data_std[:,i])
        
        data = np.random.multivariate_normal(data_mean_i, data_var_i, n).T
        dataErrorCov = data_var_i
        
        stateMean = np.mean(state, axis=1)
        statePert = state - np.matmul(stateMean.reshape((stateMean.size, 1)), np.ones((1, n)))

        forecastMean = np.mean(forecast, axis=1)
        forecastPert = forecast - np.matmul(forecastMean.reshape((forecastMean.size, 1)), np.ones((1, n)))
        forecastCov = calcCov(forecastPert)

        StateForecastCrossCov = calcCrossCov(statePert, forecastPert)

        kalmanGain = calcKalmanGain(StateForecastCrossCov, forecastCov=forecastCov, dataErrorCov=dataErrorCov)

        print(f"sample from forecast: {forecast[:,10]}")

        state = state + np.matmul(kalmanGain, (data - forecast))
        stateMean = np.mean(state, axis=1)

        # Append the estimated values to the lists
        time_steps.append(i)

        # Update the plots
        # lines['bottom_hole_flow_rate_oil'].set_data(time_steps, estimated_bottom_hole_flow_rate_oil)
        # lines['bottom_hole_flow_rate_gas'].set_data(time_steps, estimated_bottom_hole_flow_rate_gas)
        # lines['bottom_hole_flow_rate_water'].set_data(time_steps, estimated_bottom_hole_flow_rate_water)

        # Adjust the axes
        # for ax in axs:
        #     ax.relim()
        #     ax.autoscale_view()

        # plt.pause(0.1)

        print(f"Estimated bottom_hole_pressure is: {stateMean[0]}\n"
              f"Estimated bottom_hole_temperature is: {stateMean[1]}\n"
              f"Estimated liquid_rate is: {stateMean[2]}\n"
              f"Estimated water_cut is: {stateMean[3]}\n"
              f"Estimated gas_oil_ratio is: {stateMean[4]}\n"
              "*******")
        # liquid_rate, water_cut, gas_oil_ratio

    # plt.ioff()
    # plt.show()




if __name__=="__main__":
    main()