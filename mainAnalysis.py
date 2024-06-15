import numpy as np
import matplotlib.pyplot as plt
from mathematical_calculations import calcCov, calcCrossCov, calcKalmanGain
from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from model_forecast_functions import model_forecast

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

optional_data = ["bottom_hole_pressure", "bottom_hole_temperature", \
                                          "surface_pressure", "surface_temperature"]

optional_states=["bottom_hole_pressure", "bottom_hole_temperature", \
                        "surface_pressure", "surface_temperature"]

def get_observation_data(optional_data = [],
                                          data_var_ratio = 0.01, time_steps=100):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    data =[]
    for data_type in optional_data:
        data.append(all_initial_and_boundary_conditions[data_type])
    P_bottom = all_initial_and_boundary_conditions["bottom_hole_pressure"]
    P_surface = all_initial_and_boundary_conditions["surface_pressure"]
    T_bottom = all_initial_and_boundary_conditions["bottom_hole_temperature"]
    T_surface = all_initial_and_boundary_conditions["surface_temperature"]
    Q_oil_bottom = all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"]
    Q_gas_bottom = all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"]
    Q_water_bottom = all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"]
    Q_oil_surface, Q_gas_surface, Q_water_surface = model_forecast( P_bottom= P_bottom,
                                                                    P_surface= P_surface,
                                                                    T_bottom= T_bottom,
                                                                    T_surface= T_surface,
                                                                    Q_oil_bottom= Q_oil_bottom,
                                                                    Q_gas_bottom= Q_gas_bottom,
                                                                    Q_water_bottom= Q_water_bottom,
                                                                    )
    data+=[Q_oil_surface, Q_gas_surface, Q_water_surface]
    data = np.array(data)
    data_std = data_var_ratio * data
    data_var = np.diag(data_std*data_std)
    observation_data = np.random.multivariate_normal(data, data_var, time_steps)
    # data_std is assumed to be constant throughout the entire period
    return observation_data.T, data_std

def get_states(n=50, optional_states=[], state_var_ratio=0.01):
    required_states = ["bottom_hole_flow_rate_oil", "bottom_hole_flow_rate_gas", "bottom_hole_flow_rate_water",]
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

def get_model_forecast(state, optional_states=None):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    # P_surface = all_initial_and_boundary_conditions["surface_pressure"]
    # T_surface = all_initial_and_boundary_conditions["surface_temperature"]
    forecast = np.zeros((3+len(optional_states), state.shape[1]))
    for i in range(state.shape[1]):
        P_bottom = state[0,i]
        T_bottom = state[1,i]
        P_surface = state[2,i]
        T_surface = state[3,i]
        Q_oil_bottom = state[4,i]
        Q_gas_bottom = state[5,i]
        Q_water_bottom = state[6,i]
        Q_oil_surface, Q_gas_surface, Q_water_surface = model_forecast( P_bottom= P_bottom,
                                                                        P_surface= P_surface,
                                                                        T_bottom= T_bottom,
                                                                        T_surface= T_surface,
                                                                        Q_oil_bottom= Q_oil_bottom,
                                                                        Q_gas_bottom= Q_gas_bottom,
                                                                        Q_water_bottom= Q_water_bottom,
                                                                        )
        forecast[0:4,i] = state[0:4,i]
        forecast[4,i]=Q_oil_surface
        forecast[5,i]=Q_gas_surface
        forecast[6,i]=Q_water_surface
    
    return forecast



def main():
    total_obs_data, data_std = get_observation_data(optional_data=optional_data)
    state = get_states(optional_states=optional_states)

    total_time = total_obs_data.shape[1]
    n = state.shape[1]

    # Initialize lists to store estimated flow rates for plotting
    estimated_bottom_hole_flow_rate_oil = []
    estimated_bottom_hole_flow_rate_gas = []
    estimated_bottom_hole_flow_rate_water = []

    # Enable interactive mode
    plt.ion()
    fig, axs = plt.subplots(3, 1, figsize=(12, 12))
    
    # Initialize the plots
    lines = {}
    lines['bottom_hole_flow_rate_oil'], = axs[0].plot([], [], label='Oil Flow Rate')
    axs[0].set_xlabel('Time Step')
    axs[0].set_ylabel('Flow Rate')
    axs[0].legend()

    lines['bottom_hole_flow_rate_gas'], = axs[1].plot([], [], label='Gas Flow Rate')
    axs[1].set_xlabel('Time Step')
    axs[1].set_ylabel('Flow Rate')
    axs[1].legend()

    lines['bottom_hole_flow_rate_water'], = axs[2].plot([], [], label='Water Flow Rate')
    axs[2].set_xlabel('Time Step')
    axs[2].set_ylabel('Flow Rate')
    axs[2].legend()

    time_steps = []

    for i in range(total_time):
        priorState = state
        forecast = get_model_forecast(state=priorState, optional_states=optional_states)
        data_mean_i = total_obs_data[:, i]
        data_var_i = np.diag(data_std * data_std)
        
        data = np.random.multivariate_normal(data_mean_i, data_var_i, n).T
        dataErrorCov = data_var_i
        
        stateMean = np.mean(state, axis=1)
        statePert = state - np.matmul(stateMean.reshape((stateMean.size, 1)), np.ones((1, n)))

        forecastMean = np.mean(forecast, axis=1)
        forecastPert = forecast - np.matmul(forecastMean.reshape((forecastMean.size, 1)), np.ones((1, n)))
        forecastCov = calcCov(forecastPert)

        StateForecastCrossCov = calcCrossCov(statePert, forecastPert)

        kalmanGain = calcKalmanGain(StateForecastCrossCov, forecastCov=forecastCov, dataErrorCov=dataErrorCov)

        state = state + np.matmul(kalmanGain, (data - forecast))
        stateMean = np.mean(state, axis=1)

        # Append the estimated values to the lists
        estimated_bottom_hole_flow_rate_oil.append(stateMean[4])
        estimated_bottom_hole_flow_rate_gas.append(stateMean[5])
        estimated_bottom_hole_flow_rate_water.append(stateMean[6])
        time_steps.append(i)

        # Update the plots
        lines['bottom_hole_flow_rate_oil'].set_data(time_steps, estimated_bottom_hole_flow_rate_oil)
        lines['bottom_hole_flow_rate_gas'].set_data(time_steps, estimated_bottom_hole_flow_rate_gas)
        lines['bottom_hole_flow_rate_water'].set_data(time_steps, estimated_bottom_hole_flow_rate_water)

        # Adjust the axes
        for ax in axs:
            ax.relim()
            ax.autoscale_view()

        plt.pause(0.1)

        print(f"Estimated bottom_hole_flow_rate_oil is: {stateMean[4]}\n"
              f"Estimated bottom_hole_flow_rate_gas is: {stateMean[5]}\n"
              f"Estimated bottom_hole_flow_rate_water is: {stateMean[6]}\n"
              "*******")

    plt.ioff()
    plt.show()




if __name__=="__main__":
    main()