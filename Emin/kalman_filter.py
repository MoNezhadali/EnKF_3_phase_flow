import numpy as np
from beggs_and_brill import beggs_and_brill


def initialize_ensemble(initial_state, process_noise, num_ensemble_members):
    state_dim = initial_state.shape[0]
    ensemble = np.array([initial_state + process_noise * np.random.randn(state_dim) 
                         for _ in range(num_ensemble_members)])
    return ensemble

def predict(ensemble, process_noise, process_model):
    predicted_ensemble = np.array([process_model(member) + process_noise * np.random.randn(member.shape[0])
                                   for member in ensemble])
    return predicted_ensemble

def update(ensemble, observation, observation_noise, observation_model):
    num_ensemble_members = ensemble.shape[0]
    state_dim = ensemble.shape[1]
    
    # Compute the ensemble mean and perturbations
    ensemble_mean = np.mean(ensemble, axis=0)
    perturbations = ensemble - ensemble_mean
    
    # Compute the predicted observations and their mean
    predicted_observations = np.array([observation_model(member) for member in ensemble])
    observation_mean = np.mean(predicted_observations, axis=0)
    observation_perturbations = predicted_observations - observation_mean
    
    # Compute the Kalman gain
    P_xy = np.dot(perturbations.T, observation_perturbations) / (num_ensemble_members - 1)
    P_yy = np.dot(observation_perturbations.T, observation_perturbations) / (num_ensemble_members - 1) + observation_noise
    Kalman_gain = np.dot(P_xy, np.linalg.inv(P_yy))
    
    # Update ensemble members
    updated_ensemble = np.array([member + np.dot(Kalman_gain, (observation - obs)) 
                                 for member, obs in zip(ensemble, predicted_observations)])
    return updated_ensemble

# Example usage:
def process_model(state):
    # Placeholder process model
    P = 3000
    T = 150
    liquid_rate = 1000
    WC = 0.1
    GOR = 100
    gas_grav = 0.75
    oil_grav = 35
    wtr_grav = 1.121
    diameter = 3
    angle = 90
    roughness = 0.005
    Psep = 114.7
    Tsep=50

    pressure_gradient = beggs_and_brill(P,T,liquid_rate, WC, GOR, gas_grav, oil_grav, 
                wtr_grav, diameter, angle, roughness, Psep,Tsep)
                
    print("pressure_gradient", pressure_gradient)
    return state  # Replace with your specific process model (e.g., Beggs and Brill correlation)

def observation_model(state):
    # Placeholder observation model
    return state[0]  # Replace with your specific observation model

# Define initial parameters
initial_state = np.array([10.0, 5.0, 3.0])  # Initial guess for [q_o, q_g, q_w]
process_noise = 0.1  # Standard deviation of process noise
observation_noise = 1.0  # Standard deviation of observation noise
num_ensemble_members = 100
num_time_steps = 10

# Initialize ensemble
ensemble = initialize_ensemble(initial_state, process_noise, num_ensemble_members)

# Run the filter for a number of time steps
for t in range(num_time_steps):
    observation = np.array([15.0])  # Placeholder for the actual observed surface pressure
    ensemble = predict(ensemble, process_noise, process_model)
    ensemble = update(ensemble, observation, observation_noise, observation_model)
    ensemble_mean = np.mean(ensemble, axis=0)
    print(f"Time step {t+1}, Ensemble mean: {ensemble_mean}")
