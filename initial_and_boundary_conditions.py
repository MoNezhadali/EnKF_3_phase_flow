import numpy as np

def get_initial_and_boundary_conditions():
    # Initial and Boundary Conditions
    # Initial Conditions
    bottom_hole_pressure = 10e6   # Pressure in Pa
    bottom_hole_temperature = 127 + 273 # K
    bottom_hole_flow_rate_oil = 0.05 # m3/s
    bottom_hole_flow_rate_water = 0.01 # m3/s
    bottom_hole_flow_rate_gas = 0.01 # m3/s

    # Boundary Conditions
    surface_pressure = 2e6  # Pressure in Pa
    surface_temperature = 30 + 273 # K
    # surface_flow_rate_oil = 0.05 # m3/s
    # surface_flow_rate_water = 0.05 # m3/s
    # surface_flow_rate_gas = 0.05 # m3/s

    # Water Expansion Coefficients
    compressibility_coefficient = 4.6 * 10**-10 # compressibility coefficient of water reference(???)
    thermal_expansion_coefficient = 2.07 * 10**-4 # thermal expansion coefficient of water Reference(???)

    # Define the mixture components and their mole fractions in each phase
    # components = {
    #     'methane': {'Tc': 190.56, 'Pc': 4.6e6, 'omega': 0.011},
    #     'ethane': {'Tc': 305.32, 'Pc': 4.88e6, 'omega': 0.099},
    #     'propane': {'Tc': 369.83, 'Pc': 4.25e6, 'omega': 0.152},
    #     'butane': {'Tc': 425.12, 'Pc': 3.8e6, 'omega': 0.2},
    #     'pentane': {'Tc': 469.7, 'Pc': 3.37e6, 'omega': 0.251},
    #     'hexane': {'Tc': 507.6, 'Pc': 3.02e6, 'omega': 0.301},
    #     'heptane': {'Tc': 540.2, 'Pc': 2.74e6, 'omega': 0.35},
    #     'octane': {'Tc': 568.7, 'Pc': 2.49e6, 'omega': 0.398},
    #     'nonane': {'Tc': 594.6, 'Pc': 2.29e6, 'omega': 0.445},
    #     'decane': {'Tc': 617.7, 'Pc': 2.11e6, 'omega': 0.49}
    # }
    mole_fraction = np.array([0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05])

    all_initial_and_boundary_conditions = {}
    all_initial_and_boundary_conditions["bottom_hole_pressure"] = bottom_hole_pressure
    all_initial_and_boundary_conditions["bottom_hole_temperature"] = bottom_hole_temperature
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"] = bottom_hole_flow_rate_oil
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"] = bottom_hole_flow_rate_water
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"] = bottom_hole_flow_rate_gas
    all_initial_and_boundary_conditions["surface_pressure"] = surface_pressure
    all_initial_and_boundary_conditions["surface_temperature"] = surface_temperature
    # all_initial_and_boundary_conditions["surface_flow_rate_oil"] = surface_flow_rate_oil
    # all_initial_and_boundary_conditions["surface_flow_rate_water"] = surface_flow_rate_water
    # all_initial_and_boundary_conditions["surface_flow_rate_gas"] = surface_flow_rate_gas
    all_initial_and_boundary_conditions["compressibility_coefficient"] = compressibility_coefficient
    all_initial_and_boundary_conditions["thermal_expansion_coefficient"] = thermal_expansion_coefficient
    # all_initial_and_boundary_conditions["components"] = components
    all_initial_and_boundary_conditions["mole_fraction"] = mole_fraction
    
    return all_initial_and_boundary_conditions