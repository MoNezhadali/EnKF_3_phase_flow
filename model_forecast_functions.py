from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from water_flowrate_function import get_surface_flow_rate_water
from flash_calculation_function import flash_calculation

mole_fraction = get_initial_and_boundary_conditions()["mole_fraction"]
bottom_pressure = get_initial_and_boundary_conditions()["bottom_hole_pressure"]
surface_pressure = get_initial_and_boundary_conditions()["surface_pressure"]
bottom_temperature = get_initial_and_boundary_conditions()["bottom_hole_temperature"]
surface_temperature = get_initial_and_boundary_conditions()["surface_temperature"]
Q_oil_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_oil"]
Q_gas_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_gas"]
Q_water_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_water"]

water_result = get_surface_flow_rate_water(
    P_bottom= bottom_pressure,
    P_surface=surface_pressure,
    T_bottom= bottom_temperature,
    T_surface=surface_temperature,
    Q_water_bottom=Q_water_bottom
)

print(f"{water_result} \n *********")

oil_gas_results = flash_calculation(
    z=mole_fraction,
    P_bottom= bottom_pressure,
    P_surface=surface_pressure,
    T_bottom= bottom_temperature,
    T_surface=surface_temperature,
    Q_oil_bottom=Q_oil_bottom,
    Q_gas_bottom=Q_gas_bottom,
    )

for key, value in oil_gas_results.items():
    print(f"{key}: {value:.3f} \n *********")

def model_forecast(bottom_hole_pressure, bottom_hole_temperature, surface_pressure, surface_temperature, bottom_hole_flow_rate_oil, bottom_hole_flow_rate_water, bottom_hole_flow_rate_gas):
    # surface_flow_rate_water = get_surface_flow_rage_water(bottom_hole_pressure, surface_pressure, bottom_hole_temperature, surface_temperature, bottom_hole_flow_rate_water)
    pass
    # return surface_flow_rate_oil, surface_flow_rate_water, surface_flow_rate_gas