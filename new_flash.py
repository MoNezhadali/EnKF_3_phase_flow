from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB
from thermo.mixture import Mixture

def flash_calculation(T_input, P_input, T_output, P_output, Q_oil_input, Q_gas_input):
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
    composition_molar_fractions = [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]

    constants, properties = ChemicalConstantsPackage.from_IDs(components)
    kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')

    eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
    gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)
    PT_output = flasher.flash(T=T_output, P=P_output, zs=composition_molar_fractions)
    PT = flasher.flash(T=T_input, P=P_input, zs=composition_molar_fractions)

    gasDensity = PT.phases[0].rho_mass()
    liquidDensity = PT.phases[1].rho_mass()
    print("\n **********")
    print(gasDensity)
    print("\n**********")
    print(liquidDensity)


    rho_oil_top = Mixture(components, zs=composition_molar_fractions, T=T_output, P=P_output).rhol
    rho_gas_top = Mixture(components, zs=composition_molar_fractions, T=T_output, P=P_output).rhog

    density = Mixture(components, zs=composition_molar_fractions, T=T_output, P=P_output).rholm
    rho_oil_bottom = Mixture(components, zs=composition_molar_fractions, T=T_input, P=P_input).rhol
    rho_gas_bottom = Mixture(components, zs=composition_molar_fractions, T=T_input, P=P_input).rhog

    total_mass_flow_rate_top = (Q_oil_input * rho_oil_top) + (Q_gas_input * rho_gas_top)
    rho_average_bottom = (PT.LF * rho_oil_bottom) + (PT.VF * rho_gas_bottom)
    total_volume_flow_rate_bottom = total_mass_flow_rate_top / rho_average_bottom

    Q_oil_output = total_volume_flow_rate_bottom * PT.LF
    Q_gas_output = total_volume_flow_rate_bottom * PT.VF


    return Q_oil_output, Q_gas_output


values = flash_calculation(P_input=5e6, T_input=400, P_output=1e6, T_output=300, Q_oil_input=0.05, Q_gas_input=0.01)
print(values)