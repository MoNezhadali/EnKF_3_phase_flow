import pandas as pd
import matplotlib.pyplot as plt
from beggs_and_brill import calculate_total_pressure_drop
from initial_and_boundary_conditions import get_initial_and_boundary_conditions

all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
bottom_hole_pressure = all_initial_and_boundary_conditions["bottom_hole_pressure"]
bottom_hole_temperature = all_initial_and_boundary_conditions["bottom_hole_temperature"]
liquid_rate = all_initial_and_boundary_conditions["liquid_rate"]
water_cut = all_initial_and_boundary_conditions["water_cut"]
gas_oil_ratio = all_initial_and_boundary_conditions["gas_oil_ratio"]
gas_gravity = all_initial_and_boundary_conditions["gas_gravity"]
oil_gravity = all_initial_and_boundary_conditions["oil_gravity"]
water_gravity = all_initial_and_boundary_conditions["water_gravity"]
pipe_diameter = all_initial_and_boundary_conditions["pipe_diameter"]
inclination_angle = all_initial_and_boundary_conditions["inclination_angle"]
pipe_roughness = all_initial_and_boundary_conditions["pipe_roughness"]
total_pipe_length = all_initial_and_boundary_conditions["total_pipe_length"]
separator_pressure = all_initial_and_boundary_conditions["separator_pressure"]
separator_temperature = all_initial_and_boundary_conditions["separator_temperature"]


num_sections_list = list(range(1, 1000))
pressure_loss_list = []

for i in num_sections_list:
    print(f"step {i}")
    total_pressure_loss = calculate_total_pressure_drop(
        num_sections=i, 
        P_initial=bottom_hole_pressure,
        T_initial=bottom_hole_temperature, 
        liquid_rate=liquid_rate, 
        GOR=gas_oil_ratio, 
        wtr_grav=water_gravity, 
        WC=water_cut,
        gas_grav=gas_gravity, 
        oil_grav=oil_gravity,
        diameter=pipe_diameter, 
        angle=inclination_angle,
        roughness=pipe_roughness, 
        Psep=separator_pressure, 
        Tsep=separator_temperature, 
        length=total_pipe_length
    )
    pressure_loss_list.append(total_pressure_loss)

# Creating a DataFrame to store the results
data = {
    'num_sections': num_sections_list,
    'total_pressure_loss': pressure_loss_list
}
df = pd.DataFrame(data)

# Saving the DataFrame to an Excel file
df.to_excel('pressure_loss_data.xlsx', index=False)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(df['num_sections'], df['total_pressure_loss'], label='Total Pressure Loss')
plt.xlabel('Number of Sections')
plt.ylabel('Total Pressure Loss')
plt.title('Effect of Discretization on Pressure Drop')
plt.legend()
plt.grid(True)
plt.show() 