import numpy as np

def get_initial_and_boundary_conditions():
    # Initial and Boundary Conditions
    # Initial Conditions
    bottom_hole_pressure = 3e6   # Pressure in Pa
    bottom_hole_temperature = 127 + 273 # K
    # bottom_hole_flow_rate_oil = 0.05 # m3/s
    bottom_hole_flow_rate_water = 0.01 # m3/s
    # bottom_hole_flow_rate_gas = 0.01 # m3/s

    # Boundary Conditions
    surface_pressure = 1e6  # Pressure in Pa
    surface_temperature = 30 + 273 # K
    # surface_flow_rate_oil = 0.05 # m3/s
    # surface_flow_rate_water = 0.05 # m3/s
    # surface_flow_rate_gas = 0.05 # m3/s

    # Water Expansion Coefficients
    compressibility_coefficient = 4.6 * 10**-10 # compressibility coefficient of water reference(???)
    thermal_expansion_coefficient = 2.07 * 10**-4 # thermal expansion coefficient of water Reference(???)

    components = [
        'methane',
        'ethane',
        'propane',
        'butane',
        'pentane',
        'hexane',
        'heptane',
        'octane',
        'nonane',
        'decane'
    ]
    total_molar_composition = [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]
    bottom_hole_gas_composition = ([0.4383903036985637, 0.20515819584012132, 0.14251699712630705, 0.09042043120227337,
                         0.05475539445135624, 0.031347092372503535, 0.01854459590386216, 0.010787754071616782,
                           0.006242694772852111, 0.001836540560543837])
    bottom_hole_oil_composition = ([0.055457203469571836, 0.06552606039344791, 0.08606168183588182, 0.10314046350406898,
                            0.11483250817252152, 0.12250643587460186, 0.12670346955844383, 0.12924638972482785,
                              0.13073639341424098, 0.06578939405239342])
    bottom_hole_oil_fraction = 0.7531088420565052
    bottom_hole_gas_fraction = 0.2468911579434948
    multiplicant = 1/15
    bottom_hole_flow_rate_oil = bottom_hole_oil_fraction * multiplicant
    bottom_hole_flow_rate_gas = bottom_hole_gas_fraction * multiplicant
    bottom_hole_gas_molar_density = 1037.1188613836357
    bottom_hole_oil_molar_density = 6312.944033615407

    all_initial_and_boundary_conditions = {}
    all_initial_and_boundary_conditions["components"] = components
    all_initial_and_boundary_conditions["total_molar_composition"] = total_molar_composition
    all_initial_and_boundary_conditions["bottom_hole_gas_composition"] = bottom_hole_gas_composition
    all_initial_and_boundary_conditions["bottom_hole_oil_composition"] = bottom_hole_oil_composition
    all_initial_and_boundary_conditions["bottom_hole_oil_fraction"] = bottom_hole_oil_fraction
    all_initial_and_boundary_conditions["bottom_hole_gas_fraction"] = bottom_hole_gas_fraction
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"] = bottom_hole_flow_rate_oil
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"] = bottom_hole_flow_rate_gas
    all_initial_and_boundary_conditions["bottom_hole_pressure"] = bottom_hole_pressure
    all_initial_and_boundary_conditions["bottom_hole_temperature"] = bottom_hole_temperature
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"] = bottom_hole_flow_rate_oil
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"] = bottom_hole_flow_rate_water
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"] = bottom_hole_flow_rate_gas
    all_initial_and_boundary_conditions["bottom_hole_gas_molar_density"] = bottom_hole_gas_molar_density
    all_initial_and_boundary_conditions["bottom_hole_oil_molar_density"] = bottom_hole_oil_molar_density
    all_initial_and_boundary_conditions["surface_pressure"] = surface_pressure
    all_initial_and_boundary_conditions["surface_temperature"] = surface_temperature
    # all_initial_and_boundary_conditions["surface_flow_rate_oil"] = surface_flow_rate_oil
    # all_initial_and_boundary_conditions["surface_flow_rate_water"] = surface_flow_rate_water
    # all_initial_and_boundary_conditions["surface_flow_rate_gas"] = surface_flow_rate_gas
    all_initial_and_boundary_conditions["compressibility_coefficient"] = compressibility_coefficient
    all_initial_and_boundary_conditions["thermal_expansion_coefficient"] = thermal_expansion_coefficient
    # all_initial_and_boundary_conditions["components"] = components
    # all_initial_and_boundary_conditions["mole_fraction"] = mole_fraction
    
    return all_initial_and_boundary_conditions