from initial_and_boundary_conditions import get_initial_and_boundary_conditions
from water_flowrate_function import get_surface_flow_rate_water
from flash_calculation_function import flash_calculation

def model_forecast(
        P_bottom,
        T_bottom,
        P_surface,
        T_surface,
        Q_oil_bottom,
        Q_gas_bottom,
        Q_water_bottom,
    ):

    oil_flow_rate, gas_flow_rate = flash_calculation(
        P_bottom= bottom_pressure,
        P_surface=surface_pressure,
        T_bottom= bottom_temperature,
        T_surface=surface_temperature,
        Q_oil_bottom=Q_oil_bottom,
        Q_gas_bottom=Q_gas_bottom,
    )

    water_flow_rate = get_surface_flow_rate_water(
        P_bottom= P_bottom,
        P_surface=P_surface,
        T_bottom= T_bottom,
        T_surface=T_surface,
        Q_water_bottom=Q_water_bottom
    )

    return oil_flow_rate, gas_flow_rate, water_flow_rate





# CALL MODEL_FORECAST_FUNCTIONS
bottom_pressure = get_initial_and_boundary_conditions()["bottom_hole_pressure"]
surface_pressure = get_initial_and_boundary_conditions()["surface_pressure"]
bottom_temperature = get_initial_and_boundary_conditions()["bottom_hole_temperature"]
surface_temperature = get_initial_and_boundary_conditions()["surface_temperature"]
Q_oil_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_oil"]
Q_gas_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_gas"]
Q_water_bottom = get_initial_and_boundary_conditions()["bottom_hole_flow_rate_water"]

final_flow_rates = model_forecast(
    P_bottom= bottom_pressure,
    P_surface= surface_pressure,
    T_bottom= bottom_temperature,
    T_surface= surface_temperature,
    Q_oil_bottom= Q_oil_bottom,
    Q_gas_bottom= Q_gas_bottom,
    Q_water_bottom= Q_water_bottom,
)

print(final_flow_rates)