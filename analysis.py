from initial_and_boundary_conditions import get_initial_and_boundary_conditions
import numpy as np

def get_synthetic_data(total_time_steps=100, random_seed=678):
    bottom_pressure = get_initial_and_boundary_conditions()["bottom_hole_pressure"]
    surface_pressure = get_initial_and_boundary_conditions()["surface_pressure"]
    bottom_temperature = get_initial_and_boundary_conditions()["bottom_hole_temperature"]
    surface_temperature = get_initial_and_boundary_conditions()["surface_temperature"]
    Q_oil_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_oil"]
    Q_gas_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_gas"]
    Q_water_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_water"]

    true_data = np.array([bottom_pressure, 
                        surface_pressure, 
                        bottom_temperature, 
                        surface_temperature, 
                        Q_oil_bottom, 
                        Q_gas_bottom, 
                        Q_water_bottom])
    
    print(true_data)

    np.random.seed(random_seed)

    synthetic_data =np.zeros((true_data.shape[0], total_time_steps))
    standard_deviation = np.array([ 0.05 * data for data in true_data])
    for time in range(total_time_steps):
        for i in range(len(true_data)):
            synthetic_data[i,time] = np.random.normal(true_data[i], standard_deviation[i])
    
    return synthetic_data

print(get_synthetic_data(total_time_steps=2))

def get_prior_state():
    

print("")





    