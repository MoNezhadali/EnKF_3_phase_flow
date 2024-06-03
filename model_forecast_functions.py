from math import exp
from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL, PropertyCorrelationsPackage
from thermo.phases import GibbsExcessLiquid, IdealGas
import numpy as np

def get_initial_and_boundary_conditions():
    # Initial and Boundary Conditions
    # Initial Conditions
    bottom_hole_pressure = 134.5 * 10**5 # Pa
    bottom_hole_temperature = 100 + 273 # K
    bottom_hole_flow_rate_oil = 0.05 # m3/s
    bottom_hole_flow_rate_water = 0.05 # m3/s
    bottom_hole_flow_rate_gas = 0.05 # m3/s

    # Boundary Conditions
    surface_pressure = 5 * 10**5 # Pa
    surface_temperature = 30 + 273 # K
    surface_flow_rate_oil = 0.05 # m3/s
    surface_flow_rate_water = 0.05 # m3/s
    surface_flow_rate_gas = 0.05 # m3/s

    # Expansion Coefficients
    compressibility_coefficient = 4.6 * 10**-10 # compressibility coefficient of water reference(???)
    thermal_expansion_coefficient = 2.07 * 10**-4 # thermal expansion coefficient of water Reference(???)

    all_initial_and_boundary_conditions = {}
    all_initial_and_boundary_conditions["bottom_hole_pressure"] = bottom_hole_pressure
    all_initial_and_boundary_conditions["bottom_hole_temperature"] = bottom_hole_temperature
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"] = bottom_hole_flow_rate_oil
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"] = bottom_hole_flow_rate_water
    all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"] = bottom_hole_flow_rate_gas
    all_initial_and_boundary_conditions["surface_pressure"] = surface_pressure
    all_initial_and_boundary_conditions["surface_temperature"] = surface_temperature
    all_initial_and_boundary_conditions["surface_flow_rate_oil"] = surface_flow_rate_oil
    all_initial_and_boundary_conditions["surface_flow_rate_water"] = surface_flow_rate_water
    all_initial_and_boundary_conditions["surface_flow_rate_gas"] = surface_flow_rate_gas
    all_initial_and_boundary_conditions["compressibility_coefficient"] = compressibility_coefficient
    all_initial_and_boundary_conditions["thermal_expansion_coefficient"] = thermal_expansion_coefficient


    # Define the mixture components and their mole fractions in each phase
    components = ['methane', 'ethane', 'propane']  # Example components

    # Initial conditions
    # T1 = 300  # Initial temperature in K
    # P1 = 101325  # Initial pressure in Pa

    # OIl phase composition and volume percentage
    oil_mole_fractions = [0.5, 0.3, 0.2]  # Example liquid molar composition
    oil_volume_ratio = 0.40  # Liquid phase volume percentage

    # Gas phase composition and volume percentage
    gas_mole_fractions = [0.7, 0.2, 0.1]  # Example gas molar composition
    gas_volume_ratio = 0.60  # Gas phase volume percentage

    # Final conditions
    # T2 = 350  # Final temperature in K
    # P2 = 202650  # Final pressure in Pa

    all_initial_and_boundary_conditions["components"] = components
    all_initial_and_boundary_conditions["oil_mole_fractions"] = oil_mole_fractions
    all_initial_and_boundary_conditions["oil_volume_ratio"] = oil_volume_ratio
    all_initial_and_boundary_conditions["gas_mole_fractions"] = gas_mole_fractions
    all_initial_and_boundary_conditions["gas_volume_ratio"] = gas_volume_ratio

    return all_initial_and_boundary_conditions

def get_surface_flow_rate_oil_and_gas(bottom_hole_pressure, surface_pressure, bottom_hole_temperature, surface_temperature, bottom_hole_flow_rate_oil, bottom_hole_flow_rate_gas):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()

    components = all_initial_and_boundary_conditions["components"]
    oil_mole_fractions = all_initial_and_boundary_conditions["oil_mole_fractions"]
    # oil_volume_ratio = all_initial_and_boundary_conditions["oil_volume_ratio"]
    gas_mole_fractions = all_initial_and_boundary_conditions["gas_mole_fractions"]
    # gas_volume_ratio = all_initial_and_boundary_conditions["gas_volume_ratio"]
    T1 = bottom_hole_temperature  # Initial temperature in K
    P1 = bottom_hole_pressure  # Initial pressure in Pa

    T2 = surface_temperature  # Final temperature in K
    P2 = surface_pressure  # Final pressure in Pa

    # Get the necessary constants and properties
    constants = ChemicalConstantsPackage.from_IDs(components)[0]
    eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas)
    properties_oil = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=None)
    # properties_oil = CEOSLiquid(PRMIX, constants, HeatCapacityGases=None)
    properties_gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=None)
    properties_correlations = PropertyCorrelationsPackage(constants=constants)
    # Create a FlashVL object for vapor-liquid equilibrium calculations
    flash = FlashVL(constants, properties_correlations, gas = properties_gas, liquid = properties_oil)

    V_oil_initial = bottom_hole_flow_rate_oil
    V_gas_initial = bottom_hole_flow_rate_gas
    print(P1)
    oil_initial = flash.flash(T=T1, P=P1, zs=oil_mole_fractions)
    for phase in oil_initial.phases:
        print(phase.phase)
        if phase.phase == 'l':
            V_oil_molar = phase.V()

    P1 = 101325  # Initial pressure in Pa
    gas_initial = flash.flash(T=T1, P=P1, zs=gas_mole_fractions)

    # Find the liquid and gas phases
    for phase in gas_initial.phases:
        if phase.phase == 'g':
            V_gas_molar = phase.V()

    V_gas_molar = gas_initial.gas0.V()

    # Calculate initial molar volumes
    # V_oil_molar = properties_oil.molar_volume(T=T1, P=P1, zs=oil_mole_fractions)
    # V_gas_molar = properties_gas.molar_volume(T=T1, P=P1, zs=gas_mole_fractions)

    # Calculate total moles in each phase
    # V_total_initial = 1.0  # Total initial volume (arbitrary reference)
    n_oil_initial = V_oil_initial / V_oil_molar
    n_gas_initial = V_gas_initial / V_gas_molar

    # Calculate overall moles and composition
    overall_moles = n_oil_initial + n_gas_initial
    zs_overall = [(n_oil_initial * x + n_gas_initial * y) / overall_moles
                for x, y in zip(oil_mole_fractions, gas_mole_fractions)]

    # Perform the flash calculation at final conditions
    result_final = flash.flash(T=T2, P=P2, zs=zs_overall)

    # Extract new phase volumes
    V_oil_final = result_final.liquid0.V()
    V_gas_final = result_final.gas0.V()

    return V_oil_final, V_gas_final


def test_get_surface_flow_rate_oil_and_gas():
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    bottom_hole_pressure = all_initial_and_boundary_conditions["bottom_hole_pressure"]
    surface_pressure = all_initial_and_boundary_conditions["surface_pressure"]
    bottom_hole_temperature = all_initial_and_boundary_conditions["bottom_hole_temperature"]
    surface_temperature = all_initial_and_boundary_conditions["surface_temperature"]
    bottom_hole_flow_rate_oil = all_initial_and_boundary_conditions["bottom_hole_flow_rate_oil"]
    bottom_hole_flow_rate_gas = all_initial_and_boundary_conditions["bottom_hole_flow_rate_gas"]
    oil_rate, gas_rate = get_surface_flow_rate_oil_and_gas(bottom_hole_pressure = bottom_hole_pressure,
                                                           surface_pressure = surface_pressure,
                                                           bottom_hole_temperature = bottom_hole_temperature,
                                                           surface_temperature = surface_temperature,
                                                           bottom_hole_flow_rate_oil = bottom_hole_flow_rate_oil,
                                                           bottom_hole_flow_rate_gas = bottom_hole_flow_rate_gas)
    print("get_surface_flow_rate_oil_and_gas PASSED: \n",
          "oil_rate: ", oil_rate, "\n",
          "gas_rate: ", gas_rate, "\n")

components = ['methane', 'ethane', 'propane']  # Example components
constants = ChemicalConstantsPackage.from_IDs(components)[0]
eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas)
test_get_surface_flow_rate_oil_and_gas()



def get_surface_flow_rate_water(bottom_hole_pressure, surface_pressure, bottom_hole_temperature, surface_temperature, bottom_hole_flow_rate_water):
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    compressibility_coefficient = all_initial_and_boundary_conditions["compressibility_coefficient"]
    thermal_expansion_coefficient = all_initial_and_boundary_conditions["thermal_expansion_coefficient"]
    # compressibility_coefficient = 4.6 * 10**-10 # compressibility coefficient of water reference(???)
    # thermal_expansion_coefficient = 2.07 * 10**-4 # thermal expansion coefficient of water Reference(???)
    bottom_hole_flow_rate_water_const_tmp = bottom_hole_flow_rate_water * exp(compressibility_coefficient * (bottom_hole_pressure - surface_pressure))
    surface_flow_rate_water = bottom_hole_flow_rate_water_const_tmp * exp(thermal_expansion_coefficient * (surface_temperature - bottom_hole_temperature))
    return surface_flow_rate_water

# Test get_surface_flow_rage_water
def test_get_surface_flow_rate_water():
    all_initial_and_boundary_conditions = get_initial_and_boundary_conditions()
    bottom_hole_pressure = all_initial_and_boundary_conditions["bottom_hole_pressure"]
    surface_pressure = all_initial_and_boundary_conditions["surface_pressure"]
    bottom_hole_temperature = all_initial_and_boundary_conditions["bottom_hole_temperature"]
    surface_temperature = all_initial_and_boundary_conditions["surface_temperature"]
    bottom_hole_flow_rate_water = all_initial_and_boundary_conditions["bottom_hole_flow_rate_water"]

    tmp = get_surface_flow_rate_water(bottom_hole_pressure = bottom_hole_pressure,
                                  surface_pressure = surface_pressure,
                                  bottom_hole_temperature = bottom_hole_temperature,
                                  surface_temperature = surface_temperature,
                                  bottom_hole_flow_rate_water = bottom_hole_flow_rate_water)
    assert abs(tmp - 0.04972476036029373) < 1e-5
    print("get_surface_flow_rate_water PASSED: ", tmp)

test_get_surface_flow_rate_water()


def model_forecast(bottom_hole_pressure, bottom_hole_temperature, surface_pressure, surface_temperature, bottom_hole_flow_rate_oil, bottom_hole_flow_rate_water, bottom_hole_flow_rate_gas):
    # surface_flow_rate_water = get_surface_flow_rage_water(bottom_hole_pressure, surface_pressure, bottom_hole_temperature, surface_temperature, bottom_hole_flow_rate_water)
    pass
    # return surface_flow_rate_oil, surface_flow_rate_water, surface_flow_rate_gas