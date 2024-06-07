from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB
from thermo.mixture import Mixture

def flash_calculation(T_bottom, P_bottom, T_surface, P_surface, Q_oil_top, Q_gas_top):
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
    print(properties)
    kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')

    eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
    gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
    flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)
    PT_surface = flasher.flash(T=T_surface, P=P_surface, zs=composition_molar_fractions)
    PT = flasher.flash(T=T_bottom, P=P_bottom, zs=composition_molar_fractions)


    rho_oil_top = Mixture(components, zs=composition_molar_fractions, T=T_surface, P=P_surface).rhol
    rho_gas_top = Mixture(components, zs=composition_molar_fractions, T=T_surface, P=P_surface).rhog
    rho_oil_bottom = Mixture(components, zs=composition_molar_fractions, T=T_bottom, P=P_bottom).rhol
    rho_gas_bottom = Mixture(components, zs=composition_molar_fractions, T=T_bottom, P=P_bottom).rhog

    total_mass_flow_rate_top = (Q_oil_top * rho_oil_top) + (Q_gas_top * rho_gas_top)
    rho_average_bottom = (PT.LF * rho_oil_bottom) + (PT.VF * rho_gas_bottom)
    total_volume_flow_rate_bottom = total_mass_flow_rate_top / rho_average_bottom

    Q_oil_bottom = total_volume_flow_rate_bottom * PT.LF
    Q_oil_gas = total_volume_flow_rate_bottom * PT.VF


    return Q_oil_bottom, Q_oil_gas


values = flash_calculation(P_bottom=5e6, T_bottom=400, P_surface=1e6, T_surface=300, Q_oil_top=0.05, Q_gas_top=0.01)
print(values)