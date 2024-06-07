from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB

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
composition_molar_fractions = [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15]

constants, properties = ChemicalConstantsPackage.from_IDs(components)
kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')

eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)
PT = flasher.flash(T=400.0, P=2e6, zs=composition_molar_fractions)

print(PT.phase)
print("\n *******")
print(PT.VF)
print("\n *******")
print(PT.LF)
print("\n *******")
print(PT.LF + PT.VF)
