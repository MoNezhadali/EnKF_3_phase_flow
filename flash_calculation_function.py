import numpy as np
from scipy.optimize import fsolve

# Define constants for Peng-Robinson EOS
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

# Feed composition (mole fraction)
z = np.array([0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05])

# Feed conditions
T = 400.0  # Temperature in K
P = 10e6    # Pressure in Pa

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
    Z = np.max(Z_roots)  # Choosing the largest real root for vapor phase
    
    return Z

# Objective function for Rachford-Rice equation
def rachford_rice(V, z, K):
    return np.sum(z * (K - 1) / (1 + V * (K - 1)))

# Initial guess for vapor fraction
V_guess = 0.5

# Initial K-values (Wilson correlation)
K = (Pc / P) * np.exp(5.37 * (1 + omega) * (1 - Tc / T))

# Solve for vapor fraction
V = fsolve(rachford_rice, V_guess, args=(z, K))[0]

# Calculate liquid and vapor compositions
x = z / (1 + V * (K - 1))
y = K * x

# Normalize to ensure sum to 1
x /= np.sum(x)
y /= np.sum(y)

# Display results
print(f"Liquid Fraction: {1-V:.3f} \n*******")
print(f"Vapor Fraction: {V:.3f} \n*******")
print(f"Liquid Composition: {x} \n*******")
print(f"Vapor Composition: {y} \n*******")
