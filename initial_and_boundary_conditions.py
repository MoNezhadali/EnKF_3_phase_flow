import numpy as np

def get_initial_and_boundary_conditions():
    bottom_hole_pressure = 988
    bottom_hole_temperature = 132.8
    # oil_rate = 597 bbl/day
    # water_rate = 443 bbl/day
    liquid_rate = 1040
    water_cut = 0.426
    gas_oil_ratio = 237.86
    gas_gravity = 0.25
    oil_gravity = 20.22
    water_gravity = 1.121
    pipe_diameter = 3.5
    inclination_angle = 90
    total_pipe_length = 3500
    pipe_roughness = 0.001
    separator_pressure = 14.3
    separator_temperature = 68

    all_initial_and_boundary_conditions = {}
    all_initial_and_boundary_conditions["bottom_hole_pressure"] = bottom_hole_pressure
    all_initial_and_boundary_conditions["bottom_hole_temperature"] = bottom_hole_temperature
    all_initial_and_boundary_conditions["liquid_rate"] = liquid_rate
    all_initial_and_boundary_conditions["water_cut"] = water_cut
    all_initial_and_boundary_conditions["gas_oil_ratio"] = gas_oil_ratio
    all_initial_and_boundary_conditions["gas_gravity"] = gas_gravity
    all_initial_and_boundary_conditions["oil_gravity"] = oil_gravity
    all_initial_and_boundary_conditions["water_gravity"] = water_gravity
    all_initial_and_boundary_conditions["pipe_diameter"] = pipe_diameter
    all_initial_and_boundary_conditions["inclination_angle"] = inclination_angle
    all_initial_and_boundary_conditions["total_pipe_length"] = total_pipe_length
    all_initial_and_boundary_conditions["pipe_roughness"] = pipe_roughness
    all_initial_and_boundary_conditions["separator_pressure"] = separator_pressure
    all_initial_and_boundary_conditions["separator_temperature"] = separator_temperature

    
    return all_initial_and_boundary_conditions