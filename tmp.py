from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, PRMIX, FlashVL
from thermo.interaction_parameters import IPDB
constants, properties = ChemicalConstantsPackage.from_IDs(['methane', 'ethane', 'nitrogen'])
kijs = IPDB.get_ip_asymmetric_matrix('ChemSep PR', constants.CASs, 'kij')
print(kijs)
# [[0.0, -0.0059, 0.0289], [-0.0059, 0.0, 0.0533], [0.0289, 0.0533, 0.0]]
eos_kwargs = {'Pcs': constants.Pcs, 'Tcs': constants.Tcs, 'omegas': constants.omegas, 'kijs': kijs}
gas = CEOSGas(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
liquid = CEOSLiquid(PRMIX, eos_kwargs=eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases)
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)
# zs = [0.965, 0.018, 0.017]
PT = flasher.flash(T=110.0, P=1e5, zs=zs)
PT.VF, PT.gas.zs, PT.liquid0.zs
# (0.10365, [0.881788, 2.6758e-05, 0.11818], [0.97462, 0.02007, 0.005298])
flasher.flash(P=1e5, VF=1, zs=zs).T
# 133.6
flasher.flash(T=133, VF=0, zs=zs).P
# 518367.4
flasher.flash(P=PT.P, H=PT.H(), zs=zs).T
# 110.0
flasher.flash(P=PT.P, S=PT.S(), zs=zs).T
# 110.0
flasher.flash(T=PT.T, H=PT.H(), zs=zs).T
# 110.0
flasher.flash(T=PT.T, S=PT.S(), zs=zs).T
# 110.0