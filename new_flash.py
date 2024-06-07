from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB

components = [
'methane','ethane','propane','butane','pentane','hexane','heptane','octane','nonane','decane',
]

constants, properties = ChemicalConstantsPackage.from_IDs(components)
kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')

eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)
zs = [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]
PT = flasher.flash(T=300.0, P=1e5, zs=zs)

print("\n *******")
print(PT.phase)
print("\n *******")
print("\n *******")
