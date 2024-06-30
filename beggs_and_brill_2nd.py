import math
import fluidproperties_original as pvt
import random
import matplotlib.pyplot as plt

"""
This code results with the pressure loss gradient in psi/ft 
"""

def beggs_and_brill(P,T,liquid_rate, WC, GOR, gas_grav, oil_grav, wtr_grav, diameter, angle, roughness, Psep,Tsep):
    #P              Pressure, psia
    #T              Temperature, °F
    #liquid_rate    Oil flowrate, stb/D
    #WC             Water Cut, %
    #GOR            Producing gas-oil ratio, scf/stb
    #gas_grav       Gas specific gravity
    #oil_grav       Oil gravity, API
    #wtr_grav       Water specific gravity
    #diameter       Inner diameter of pipe, in.
    #angle          angle of pipe inclination in degrees
    #roughness      Roughness of the pipe or tubing
    #Psep           Separator pressure, psia
    #Tsep           Separator temperature, °F    
    
    angle_pi = angle * math.pi / 180                       #angle_pi is converted angle in terms of pi
    area = math.pi / 4 * (diameter / 12)**2  #X-sectional area of pipe, ft^2
    gas_rate=liquid_rate*GOR                            #Gas rate, SCF/D 
    liquid_rate1=liquid_rate* 0.000065                  #Unit conversion to ft^3/s from stb/D
    
    #Velocity under zero slippage
    oil_rate=liquid_rate*(1-WC)
    water_rate=liquid_rate*WC
    wor=water_rate/oil_rate
    # usl = liquid_rate1 / area                            #Liquid superficial velocity, ft/s
    # usg = gas_rate / area /86400                         #Gas superficial velocity, ft/s

    ###################################################################

    #Importing the properties of fluids
    Z = pvt.zfactor(P,T,gas_grav)                                           #Gas compressibility factor
    TDS = pvt.salinity(wtr_grav)                                            #Water salinity, wt% total dissolved solids
    Pb = pvt.bubble_point2(T, Tsep, Psep, gas_grav, oil_grav, GOR)          #Bubble point pressure, psia
    Rso = pvt.sol_gor(T, P, Tsep, Psep, Pb, gas_grav, oil_grav)             #Solution gas-oil ratio, scf/stb
    Rsw = pvt.sol_gwr(P, T, TDS)                                            #Solution gas_water ratio, scf/stb
    Bo = pvt.oil_fvf(T, P, Tsep, Psep, Pb, Rso, gas_grav, oil_grav)                           #Oil formation volume factor, rb/stb
    Bw = pvt.water_fvf(P, T, TDS)                                           #Water formation volume factor, rb/stb
    Bg = pvt.gas_fvf(P, T, gas_grav)                                        #Gas formation volume factor, ft_/scf
    muo = pvt.oil_visc(T, P, Pb, Rso, gas_grav, oil_grav)                   #Oil viscosity, cp
    muw = pvt.wtr_visc(P, T, TDS)                                           #Water viscosity, cp
    mug = pvt.gvisc(P, T, Z, gas_grav)                                        #Gas viscosity, cp
    rhoo = pvt.oil_dens(P, T, Tsep, Psep, Pb, Bo, Rso, gas_grav, oil_grav)  #Oil density, lb/ft
    rhow = 62.368 * wtr_grav / Bw                                      #Water density, lb/ft^3
    rhog = 2.699 * gas_grav * P / (T + 460) / Z                         #Gas density, lb/ft^3
    sigo = pvt.oil_tens(P, T, oil_grav)                                     #Gas-oil interfacial tension, dynes/cm
    sigw = pvt.wtr_tens(P, T)                                               #Gas-water interfacial tension, dynes/cm

    ###################################################################

     #Volume fraction weighted liquid properties
    rhol = (Bw * wor * rhow + Bo * rhoo) / (Bw * wor + Bo)  
    #rhol     Liquid density, lb/ft                                                  
    mul = (Bw * wor * rhow) / (Bw * wor * rhow + Bo * rhoo) * muw + (Bo * rhoo) / (Bw * wor * rhow + Bo * rhoo) * muo              
    #mul      Liquid viscosity, cp
    sigl = (Bw * wor * rhow) / (Bw * wor * rhow + Bo * rhoo) * sigw + (Bo * rhoo) / (Bw * wor * rhow + Bo * rhoo) * sigo           
    #sigl     Gas-liquid interfacial tension, dynes/cm

    ###################################################################

    #Calculate bottomhole fluid velocity in ft_/s
    qo = Bo * oil_rate / 15387                                          #Oil flowrate
    qw = Bw * wor * oil_rate / 15387                                    #Water flowrate
    ql = qo + qw                                                        #Liquid flowrate
    if ((GOR - Rso - Rsw*wor) <= 0):                           #If gas flowrate is negative, set to zero
        qg = 0
    else:
        qg = Bg * (GOR - Rso - Rsw * wor) * oil_rate / 86400
    
    usl = ql / area                                                      #Liquid superficial velocity
    usg = qg / area
    um = usl + usg                                       #Mixture superficial velocity, ft/s

    ###################################################################

    #um       mixture velocity
    #diameter pipe inside diameter
    NFr = um**2/32.174/(diameter/12)  
    CL = ql/ (ql+ qg)
    CG = 1- CL
    NLV = 1.938 * usl * (rhol / sigl) ** 0.25 
    """
      usl is no slip liquid velocity, 
      ρL, liquid density, 
      g, gravitational constant and 
      σ,  is surface tension
    """
    #The transition lines for correlation    
    L1 = 316*CL**0.302
    L2 = 0.0009252*CL**(-2.4684)
    L3 = 0.1*CL**(-1.4516)
    L4 = 0.5*CL**(-6.738) 
                             
    """"
    EL0 = a*CL**b / Frm**c
    """


#For uphill&downhill flow flow
#β    the inclination correction factor coefficient
#B    the liquid hold-up inclination correction factor
#EL0  the horizontal hold-up 
#CL   the non slip holdup
#EL   final hold-up after inclination and slip correlation

def Flow_type(NFr, CL, L1, L2, L3, L4):
    """Function to Determine the Flow regime by the Method of Beggs and Brill"""
    #The function returns a number indicating the flow flow_type
    #   Segregated flow
    #   Transition flow
    #   Intermittent flow
    #   Distributed flow    
    #NFr        Froude Number
    #CL       Input liquid fraction
    #L1,2,3,4   Dimensionless constants

    #flow_type 1 - Segregated flow
    if (((CL < 0.01) and (NFr < L1)) or ((CL >= 0.01) and (NFr < L2))):
        flow_type = "Segregated Flow"
    
        
    #flow_type 2 - Transition flow
    if ((CL >= 0.01) and (L2 < NFr) and (NFr <= L3)):
        flow_type = "Transition Flow"
    
        
    #flow_type 3 - Intermittent flow
    if ((((0.01 <= CL) and (CL < 0.4)) and ((L3 < NFr) and (NFr < L1))) or ((CL >= 0.4) and (L3 < NFr) and (NFr <= L4))):
        flow_type = "Intermittent Flow"
    
        
    #flow_type 4 - Distributed flow
    if (((CL < 0.4) and (NFr >= L1)) or ((CL >= 0.4) and (NFr > L4))):
        flow_type = "Distributed Flow"
    
    
    return flow_type