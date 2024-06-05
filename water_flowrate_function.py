from math import exp
from initial_and_boundary_conditions import get_initial_and_boundary_conditions

def get_surface_flow_rate_water(P_bottom, P_surface, T_bottom, T_surface, Q_water_bottom):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    compressibility_coefficient = all_initial_and_boundary_conditions["compressibility_coefficient"]
    thermal_expansion_coefficient = all_initial_and_boundary_conditions["thermal_expansion_coefficient"]
    Q_water_bottom_const_tmp = Q_water_bottom * exp(compressibility_coefficient * (P_bottom - P_surface))
    surface_flow_rate_water = Q_water_bottom_const_tmp * exp(thermal_expansion_coefficient * (T_surface - T_bottom))
    return surface_flow_rate_water

# Test get_surface_flow_rage_water
# def test_get_surface_flow_rate_water():
#     all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
#     P_bottom = all_initial_and_boundary_conditions["P_bottom"]
#     P_surface = all_initial_and_boundary_conditions["P_surface"]
#     T_bottom = all_initial_and_boundary_conditions["T_bottom"]
#     T_surface = all_initial_and_boundary_conditions["T_surface"]
#     Q_water_bottom = all_initial_and_boundary_conditions["Q_water_bottom"]

#     tmp = get_surface_flow_rate_water(P_bottom = P_bottom,
#                                   P_surface = P_surface,
#                                   T_bottom = T_bottom,
#                                   T_surface = T_surface,
#                                   Q_water_bottom = Q_water_bottom)

#     assert abs(tmp - 0.04972476036029373) < 1e-3
#     print("get_surface_flow_rate_water PASSED: ", tmp)

# test_get_surface_flow_rate_water()