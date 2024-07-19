from beggs_and_brill import calculate_total_pressure_drop
from initial_and_boundary_conditions import get_initial_and_boundary_conditions


def model_forecast(bottom_hole_pressure, bottom_hole_temperature,
                   liquid_rate, water_cut, gas_oil_ratio):
                   
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    gas_gravity = all_initial_and_boundary_conditions["gas_gravity"]
    oil_gravity = all_initial_and_boundary_conditions["oil_gravity"]
    water_gravity = all_initial_and_boundary_conditions["water_gravity"]
    pipe_diameter = all_initial_and_boundary_conditions["pipe_diameter"]
    inclination_angle = all_initial_and_boundary_conditions["inclination_angle"]
    pipe_roughness = all_initial_and_boundary_conditions["pipe_roughness"]
    total_pipe_length = all_initial_and_boundary_conditions["total_pipe_length"]
    separator_pressure = all_initial_and_boundary_conditions["separator_pressure"]
    separator_temperature = all_initial_and_boundary_conditions["separator_temperature"]
    pressure_drop, estimated_bottom_hole_temperature, flow_regime, liquid_hold_up, qo, qw, qg = calculate_total_pressure_drop(
                    num_sections=100 , P_initial=bottom_hole_pressure, 
                    T_initial=bottom_hole_temperature, length=total_pipe_length,
                    liquid_rate=liquid_rate, WC=water_cut, GOR=gas_oil_ratio,
                    gas_grav=gas_gravity, oil_grav=oil_gravity, wtr_grav=water_gravity,
                    diameter=pipe_diameter, angle=inclination_angle, roughness=pipe_roughness,
                    Psep=separator_pressure, Tsep=separator_temperature)

    estimated_bottom_hole_pressure = separator_pressure + pressure_drop
    return estimated_bottom_hole_pressure, estimated_bottom_hole_temperature, flow_regime, liquid_hold_up, qo, qw, qg

    # estimated_surface_pressure = bottom_hole_pressure - pressure_drop
    # estimated_surface_temperature = estimated_bottom_hole_temperature
    # return estimated_surface_pressure, estimated_surface_temperature, flow_regime, liquid_hold_up