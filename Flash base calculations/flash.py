from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB
from thermo.mixture import Mixture
from initial_and_boundary_conditions import get_initial_and_boundary_conditions

def flash_calculation(T_input, P_input, T_output, P_output, Q_oil_input, Q_gas_input):
    tmp = get_initial_and_boundary_conditions()
    components = tmp["components"]
    gas_composition = tmp["bottom_hole_gas_composition"]
    liquid_composition = tmp["bottom_hole_oil_composition"]
    gas_molar_density = tmp["bottom_hole_gas_molar_density"]
    liquid_molar_density = tmp["bottom_hole_oil_molar_density"]

    gas_fraction = Q_gas_input * gas_molar_density / (Q_gas_input * gas_molar_density + Q_oil_input * liquid_molar_density)
    liquid_fraction = 1 - gas_fraction


    total_composition = [None]*len(gas_composition)
    for i in range(len(gas_composition)):
        total_composition[i] = gas_composition[i] * gas_fraction + liquid_composition[i] * liquid_fraction

    constants, properties = ChemicalConstantsPackage.from_IDs(components)
    kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')
    eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
    gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)

    input_flash = flasher.flash(T=T_input, P=P_input, zs=total_composition)

    inputGasDensity = input_flash.phases[0].rho()
    inputGasFraction = input_flash.VF
    inputGasComposition = input_flash.phases[0].zs_calc
    inputLiquidDensity = input_flash.phases[1].rho()
    inputLiquidComposition = input_flash.phases[1].zs_calc
    inputLiquidFraction = input_flash.LF

    output_flash = flasher.flash(T=T_output, P=P_output, zs=total_composition)

    outputGasDensity = output_flash.phases[0].rho()
    outputGasFraction = output_flash.VF
    outputGasComposition = output_flash.phases[0].zs_calc
    outputLiquidDensity = output_flash.phases[1].rho()
    outputLiquidComposition = output_flash.phases[1].zs_calc
    outputLiquidFraction = output_flash.LF

    Q_mole_liquid = (Q_oil_input * inputLiquidDensity) 
    Q_mole_gas = (Q_gas_input * inputGasDensity) 
    total_mole_flow_rate = Q_mole_liquid + Q_mole_gas

    Q_mole_gas_output = total_mole_flow_rate * outputGasFraction
    Q_mole_liquid_output = total_mole_flow_rate * outputLiquidFraction

    Q_volume_gas_output = Q_mole_gas_output / outputGasDensity
    Q_volume_liquid_output = Q_mole_liquid_output / outputLiquidDensity

    return Q_volume_liquid_output, Q_volume_gas_output

def main():
    tmp = get_initial_and_boundary_conditions()

    bottom_hole_pressure = tmp["bottom_hole_pressure"]
    surface_pressure = tmp["surface_pressure"]
    bottom_hole_temperature = tmp["bottom_hole_temperature"]
    surface_temperature = tmp["surface_temperature"]
    bottom_hole_flow_rate_oil = tmp["bottom_hole_flow_rate_oil"]
    bottom_hole_flow_rate_gas = tmp["bottom_hole_flow_rate_gas"]

    print("bottom_hole_flow_rate_oil: ", bottom_hole_flow_rate_oil)
    print("bottom_hole_flow_rate_gas: ", bottom_hole_flow_rate_gas)

    surface_flow_rate_oil, surface_flow_rate_gas = flash_calculation(P_input = bottom_hole_pressure,
                                                                    T_input = bottom_hole_temperature,
                                                                    P_output=surface_pressure,
                                                                    T_output=surface_temperature,
                                                                    Q_oil_input=bottom_hole_flow_rate_oil,
                                                                    Q_gas_input=bottom_hole_flow_rate_gas)
    print("surface_flow_rate_oil: ", surface_flow_rate_oil)
    print("surface_flow_rate_gas: ", surface_flow_rate_gas)


if __name__ == "__main__":
    main()