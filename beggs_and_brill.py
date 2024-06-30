import numpy as np
from scipy.optimize import fsolve

# Constants for Peng-Robinson EoS
R = 8.314  # Universal gas constant, J/(mol*K)

def peng_robinson_eos(P, T, Tc, Pc, omega):
    """
    Peng-Robinson Equation of State to calculate molar volume.
    
    Parameters:
    P (float): Pressure (Pa).
    T (float): Temperature (K).
    Tc (float): Critical temperature (K).
    Pc (float): Critical pressure (Pa).
    omega (float): Acentric factor.
    
    Returns:
    Vm (float): Molar volume (m^3/mol).
    Z (float): Compressibility factor.
    """
    Tr = T / Tc
    a = 0.45724 * (R * Tc)**2 / Pc
    b = 0.07780 * R * Tc / Pc
    kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
    alpha = (1 + kappa * (1 - np.sqrt(Tr)))**2
    A = a * alpha * P / (R**2 * T**2)
    B = b * P / (R * T)
    
    # Cubic equation of state in terms of Z
    coeffs = [1, -1 + B, A - 2 * B - 3 * B**2, -A * B + B**2 + B**3]
    roots = np.roots(coeffs)
    Z = np.max(np.real(roots[np.isreal(roots)]))  # We take the largest real root
    
    Vm = Z * R * T / P
    return Vm, Z

def density(P, T, Tc, Pc, omega, MW):
    """
    Calculate fluid density using the Peng-Robinson EOS.
    
    Parameters:
    P (float): Pressure (Pa).
    T (float): Temperature (K).
    Tc (float): Critical temperature (K).
    Pc (float): Critical pressure (Pa).
    omega (float): Acentric factor.
    MW (float): Molecular weight (kg/mol).
    
    Returns:
    rho (float): Density (kg/m^3).
    """
    Vm, Z = peng_robinson_eos(P, T, Tc, Pc, omega)
    rho = MW / Vm
    return rho

def pressure_drop_with_compressibility(qo, qw, qg, pipe_length, pipe_diameter, pipe_roughness, pressure_end, temperature_end, oil_props, water_props, gas_props, elevation_change):
    """
    Calculate pressure drop with compressibility and phase changes.
    
    Parameters:
    qo, qw, qg (float): Flow rates of oil, water, and gas at the end of the pipeline (m^3/day).
    pipe_length (float): Length of the pipeline (m).
    pipe_diameter (float): Diameter of the pipeline (m).
    pipe_roughness (float): Roughness of the pipeline (m).
    pressure_end (float): Pressure at the end of the pipeline (Pa).
    temperature_end (float): Temperature at the end of the pipeline (K).
    oil_props, water_props, gas_props (dict): Properties of oil, water, and gas (Tc, Pc, omega, MW).
    elevation_change (float): Elevation change of the pipeline (m).
    
    Returns:
    pressure_start (float): Pressure at the beginning of the pipeline (Pa).
    """
    
    # Convert flow rates from m^3/day to m^3/s
    qo_m3s = qo / 86400
    qw_m3s = qw / 86400
    qg_m3s = qg / 86400
    
    # Total flow rate
    qt_m3s = qo_m3s + qw_m3s + qg_m3s
    
    # In-situ volumetric fractions
    alpha_o = qo_m3s / qt_m3s
    alpha_w = qw_m3s / qt_m3s
    alpha_g = qg_m3s / qt_m3s
    
    # Mixture properties at the end of the pipeline
    rho_o = density(pressure_end, temperature_end, oil_props['Tc'], oil_props['Pc'], oil_props['omega'], oil_props['MW'])
    rho_w = density(pressure_end, temperature_end, water_props['Tc'], water_props['Pc'], water_props['omega'], water_props['MW'])
    rho_g = density(pressure_end, temperature_end, gas_props['Tc'], gas_props['Pc'], gas_props['omega'], gas_props['MW'])
    
    rho_m = alpha_o * rho_o + alpha_w * rho_w + alpha_g * rho_g
    
    mu_o = oil_props['viscosity']
    mu_w = water_props['viscosity']
    mu_g = gas_props['viscosity']
    
    mu_m = alpha_o * mu_o + alpha_w * mu_w + alpha_g * mu_g
    
    # Cross-sectional area of the pipeline
    area = np.pi * (pipe_diameter / 2)**2
    
    # Superficial velocities
    vso = qo_m3s / area
    vsw = qw_m3s / area
    vsg = qg_m3s / area
    
    # Mixture velocity
    vm = vso + vsw + vsg
    
    # Fanning friction factor (using the Moody chart approximation)
    Re = (rho_m * vm * pipe_diameter) / mu_m  # Reynolds number
    if Re < 2000:
        f = 16 / Re
    else:
        f = 0.079 / (Re ** 0.25)
    
    # Beggs and Brill correlation for pressure drop
    dp_dz_friction = f * (rho_m * vm ** 2) / (2 * pipe_diameter)
    dp_dz_gravity = rho_m * 9.81 * (elevation_change / pipe_length)
    
    dp_dz = dp_dz_friction + dp_dz_gravity
    
    # Calculate pressure at the start of the pipeline
    pressure_start = pressure_end + dp_dz * pipe_length
    print(pressure_end)
    print(pressure_start)
    
    return pressure_start

def flow_rates_at_start(qo_end, qw_end, qg_end, pipe_length, pipe_diameter, pipe_roughness, pressure_end, temperature_end, oil_props, water_props, gas_props, elevation_change):
    """
    Estimate flow rates at the beginning of the pipeline with phase change and compressibility.
    
    Parameters:
    qo_end, qw_end, qg_end (float): Flow rates of oil, water, and gas at the end of the pipeline (m^3/day).
    pipe_length (float): Length of the pipeline (m).
    pipe_diameter (float): Diameter of the pipeline (m).
    pipe_roughness (float): Roughness of the pipeline (m).
    pressure_end (float): Pressure at the end of the pipeline (Pa).
    temperature_end (float): Temperature at the end of the pipeline (K).
    oil_props, water_props, gas_props (dict): Properties of oil, water, and gas (Tc, Pc, omega, MW).
    elevation_change (float): Elevation change of the pipeline (m).
    
    Returns:
    flow_rates_start (dict): Flow rates of oil, water, and gas at the beginning of the pipeline (m^3/day).
    """
    
    # Calculate the pressure at the start of the pipeline
    pressure_start = pressure_drop_with_compressibility(qo_end, qw_end, qg_end, pipe_length, pipe_diameter, pipe_roughness, pressure_end, temperature_end, oil_props, water_props, gas_props, elevation_change)
    
    # Assuming compressible flow and phase change
    rho_o_start = density(pressure_start, temperature_end, oil_props['Tc'], oil_props['Pc'], oil_props['omega'], oil_props['MW'])
    rho_w_start = density(pressure_start, temperature_end, water_props['Tc'], water_props['Pc'], water_props['omega'], water_props['MW'])
    rho_g_start = density(pressure_start, temperature_end, gas_props['Tc'], gas_props['Pc'], gas_props['omega'], gas_props['MW'])
    
    # Convert volumetric flow rates to mass flow rates
    mo_end = qo_end * rho_o_start
    mw_end = qw_end * rho_w_start
    mg_end = qg_end * rho_g_start
    
    # Mass flow rates remain constant
    mo_start = mo_end
    mw_start = mw_end
    mg_start = mg_end
    
    # Convert mass flow rates back to volumetric flow rates at the start
    qo_start = mo_start / rho_o_start
    qw_start = mw_start / rho_w_start
    qg_start = mg_start / rho_g_start
    
    # Return the flow rates as a dictionary
    flow_rates_start = {
        'oil': qo_start,
        'water': qw_start,
        'gas': qg_start,
        'pressure_start': pressure_start
    }
    
    return flow_rates_start

# Example usage
qo_end = 1000  # m^3/day
qw_end = 500  # m^3/day
qg_end = 2000  # m^3/day
pipe_length = 3000  # m
pipe_diameter = 0.2  # m
pipe_roughness = 0.000015  # m
pressure_end = 700000  # Pa
temperature_end = 300  # K

oil_props = {
    'Tc': 617.7,  # K
    'Pc': 2.11e6,  # Pa
    'omega': 0.635,
    'MW': 0.2,  # kg/mol
    'viscosity': 0.1  # Pa.s
}

water_props = {
    'Tc': 647.1,  # K
    'Pc': 22.06e6,  # Pa
    'omega': 0.344,
    'MW': 0.018,  # kg/mol
    'viscosity': 0.001  # Pa.s
}

gas_props = {
    'Tc': 190.6,  # K
    'Pc': 4.6e6,  # Pa
    'omega': 0.011,
    'MW': 0.016,  # kg/mol
    'viscosity': 0.00001  # Pa.s
}

elevation_change = 1000  # m

flow_rates_start = flow_rates_at_start(qo_end, qw_end, qg_end, pipe_length, pipe_diameter, pipe_roughness, pressure_end, temperature_end, oil_props, water_props, gas_props, elevation_change)
print(flow_rates_start)
