from math import exp
from initial_and_boundary_conditions import get_initial_and_boundary_conditions

def get_surface_flow_rate_water(bottom_hole_pressure, surface_pressure, bottom_hole_temperature, surface_temperature, bottom_hole_flow_rate_water):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    compressibility_coefficient = all_initial_and_boundary_conditions["compressibility_coefficient"]
    thermal_expansion_coefficient = all_initial_and_boundary_conditions["thermal_expansion_coefficient"]
    bottom_hole_flow_rate_water_const_tmp = bottom_hole_flow_rate_water * exp(compressibility_coefficient * (bottom_hole_pressure - surface_pressure))
    surface_flow_rate_water = bottom_hole_flow_rate_water_const_tmp * exp(thermal_expansion_coefficient * (surface_temperature - bottom_hole_temperature))
    return surface_flow_rate_water

# Test get_surface_flow_rage_water
# def test_get_surface_flow_rate_water():
#     all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
#     bottom_hole_pressure = all_initial_and_boundary_conditions["bottom_hole_pressure"]
#     surface_pressure = all_initial_and_boundary_conditions["surface_pressure"]
#     bottom_hole_temperature = all_initial_and_boundary_conditions["bottom_hole_temperature"]
#     surface_temperature = all_initial_and_boundary_conditions["surface_temperature"]
#     bottom_hole_flow_rate_water = all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"]

#     tmp = get_surface_flow_rate_water(bottom_hole_pressure = bottom_hole_pressure,
#                                   surface_pressure = surface_pressure,
#                                   bottom_hole_temperature = bottom_hole_temperature,
#                                   surface_temperature = surface_temperature,
#                                   bottom_hole_flow_rate_water = bottom_hole_flow_rate_water)

#     assert abs(tmp - 0.04972476036029373) < 1e-3
#     print("get_surface_flow_rate_water PASSED: ", tmp)

# test_get_surface_flow_rate_water()