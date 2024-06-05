import numpy as np
from scipy.optimize import fsolve

# Constants for Peng-Robinson EOS
R = 8.314  # J/(mol*K)

# Component properties: Tc (K), Pc (Pa), omega
components = {
    'methane': {'Tc': 190.56, 'Pc': 4.6e6, 'omega': 0.011},
    'ethane': {'Tc': 305.32, 'Pc': 4.88e6, 'omega': 0.099},
    'propane': {'Tc': 369.83, 'Pc': 4.25e6, 'omega': 0.152},
    'butane': {'Tc': 425.12, 'Pc': 3.8e6, 'omega': 0.2},
    'pentane': {'Tc': 469.7, 'Pc': 3.37e6, 'omega': 0.251},
    'hexane': {'Tc': 507.6, 'Pc': 3.02e6, 'omega': 0.301},
    'heptane': {'Tc': 540.2, 'Pc': 2.74e6, 'omega': 0.35},
    'octane': {'Tc': 568.7, 'Pc': 2.49e6, 'omega': 0.398},
    'nonane': {'Tc': 594.6, 'Pc': 2.29e6, 'omega': 0.445},
    'decane': {'Tc': 617.7, 'Pc': 2.11e6, 'omega': 0.49}
}

# Critical properties and acentric factors
Tc = np.array([components[comp]['Tc'] for comp in components])
Pc = np.array([components[comp]['Pc'] for comp in components])
omega = np.array([components[comp]['omega'] for comp in components])
n_components = len(components)

# Peng-Robinson parameters
kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
a = 0.45724 * R**2 * Tc**2 / Pc
b = 0.07780 * R * Tc / Pc

# Peng-Robinson alpha function
def alpha(T):
    return (1 + kappa * (1 - np.sqrt(T / Tc)))**2

# Peng-Robinson mixing rules
def a_mix(y, alpha):
    return np.sum(np.outer(y, y) * np.sqrt(np.outer(a, a)) * (1 - 0))

def b_mix(y):
    return np.sum(y * b)

# Solve Peng-Robinson EOS for both phases
def PR_EOS(T, P, y):
    alpha_val = alpha(T)
    a_m = a_mix(y, alpha_val)
    b_m = b_mix(y)
    
    # Coefficients of cubic EOS
    A = a_m * P / (R * T)**2
    B = b_m * P / (R * T)
    
    coeffs = [1, -(1 - B), A - 2*B - 3*B**2, -(A*B - B**2 - B**3)]
    Z_roots = np.roots(coeffs)
    Z_roots = Z_roots[np.isreal(Z_roots)].real  # Keep only real roots
    Z = np.max(Z_roots)  # Choosing the largest real root for vapor phase
    
    return Z

# Objective function for Rachford-Rice equation
def rachford_rice(V, z, K):
    return np.sum(z * (K - 1) / (1 + V * (K - 1)))

# Flash calculation function
def flash_calculation(z, T_bottom, P_bottom, T_surface, P_surface, Q_oil_bottom, Q_gas_bottom):
    # Initial guess for vapor fraction
    V_guess = 0.5

    # Initial K-values (Wilson correlation)
    K_bottom = (Pc / P_bottom) * np.exp(5.37 * (1 + omega) * (1 - Tc / T_bottom))

    # Solve for vapor fraction at bottom conditions
    V_bottom = fsolve(rachford_rice, V_guess, args=(z, K_bottom))[0]

    # Calculate liquid and vapor compositions at bottom
    x_bottom = z / (1 + V_bottom * (K_bottom - 1))
    y_bottom = K_bottom * x_bottom

    # Normalize to ensure sum to 1
    x_bottom /= np.sum(x_bottom)
    y_bottom /= np.sum(y_bottom)

    # Calculate molar flow rates at the bottom
    n_total_bottom = (Q_oil_bottom + Q_gas_bottom) / (np.sum(x_bottom * b) + np.sum(y_bottom * b))
    n_liquid_bottom = (1 - V_bottom) * n_total_bottom
    n_vapor_bottom = V_bottom * n_total_bottom

    # Recalculate K-values for the surface conditions
    K_surface = (Pc / P_surface) * np.exp(5.37 * (1 + omega) * (1 - Tc / T_surface))

    # Solve for vapor fraction at surface conditions
    V_surface = fsolve(rachford_rice, V_guess, args=(z, K_surface))[0]

    # Calculate liquid and vapor compositions at surface
    x_surface = z / (1 + V_surface * (K_surface - 1))
    y_surface = K_surface * x_surface

    # Normalize to ensure sum to 1
    x_surface /= np.sum(x_surface)
    y_surface /= np.sum(y_surface)

    # Calculate molar flow rates at the surface
    n_liquid_surface = (1 - V_surface) * n_total_bottom
    n_vapor_surface = V_surface * n_total_bottom

    # Calculate volumetric flow rates at surface conditions
    Z_liquid_surface = PR_EOS(T_surface, P_surface, x_surface)
    Z_vapor_surface = PR_EOS(T_surface, P_surface, y_surface)

    # Molar volumes at surface conditions
    V_liquid_molar_surface = Z_liquid_surface * R * T_surface / P_surface
    V_vapor_molar_surface = Z_vapor_surface * R * T_surface / P_surface

    # Volumetric flow rates
    Q_oil_surface = n_liquid_surface * V_liquid_molar_surface
    Q_gas_surface = n_vapor_surface * V_vapor_molar_surface

    return {
        'Liquid Fraction at Bottom': 1 - V_bottom,
        'Vapor Fraction at Bottom': V_bottom,
        'Liquid Fraction at Surface': 1 - V_surface,
        'Vapor Fraction at Surface': V_surface,
        'Oil Flow Rate at Surface': Q_oil_surface,
        'Gas Flow Rate at Surface': Q_gas_surface
    }
