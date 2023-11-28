from handcalcs.decorator import handcalc
import forallpeople as si
import math

@handcalc()
def debit(area: float, n: float, ir=float) -> float:
    """
    calculates the debit of rainwater with the constant ir:5*10-5 from NEN1991-1-1-3 table NB 1
    area is in m^2, and n is the number of overloads per area.

    """
    ir=5*10**-5
    Qhi = (area * ir) / n
    return Qhi


@handcalc()
def waterheight(width_overload: float, Qhi: float) -> float:
    """
    calculates the waterheight above the overload 
    with the debit and overload width in mm.
    """
    Dndi=0.7 * ((Qhi / (width_overload/1000)) ** (2/3))*10**3
    return Dndi

@handcalc()
def water_above_roof(Dndi:float,height_aboveroof: float) -> float:
    dhw = Dndi + height_aboveroof
    return dhw

@handcalc()
def critical_height(height_aboveroof:float,height_of_overload:float) -> float:
    hcrit=height_aboveroof + height_of_overload-30
    return hcrit

@handcalc()
def equivalent_load(dhw:float)-> float:
    equivalentload=dhw*10/1000
    return equivalentload

@handcalc()
def d_flat(dhw:float)-> float:
    d_flat=dhw
    return d_flat

@handcalc()
def d_curved(dhw:float,z:float)-> float:
    d_curved=dhw-0.8*z
    return d_curved

@handcalc()
def d_sloped(dhw:float,al:float)-> float:
    d_sloped=dhw-0.5*al
    return d_sloped

@handcalc()
def flat_roof(dhw: float) -> float:
    d = dhw
    return d

@handcalc()
def curved_roof(dhw: float, z: float) -> float:
    d = dhw - 0.8 * z
    return d

@handcalc()
def sloped_roof_bi_al(dhw: float, al: float, z: float) -> float:
    d = dhw - 0.5 * al
    return d

@handcalc()
def sloped_roof_sm_al(dhw: float, al: float, z: float) -> float:
    z = 0
    x = 1 - ((dhw - 0.8 * z) / al)
    c = 0.5 - 0.3 * x**2 - 0.2 * x**3
    d = dhw - c * al
    return d

@handcalc()
def curved_and_sloped_roof_bi_al(dhw: float, al: float, z: float) -> float:
    d = dhw - 0.8 * z - 0.5 * al
    return d

@handcalc()
def curved_and_sloped_roof_sm_al(dhw: float, al: float, z: float) -> float:
    x = 1 - ((dhw - 0.8 * z) / al)
    c = 0.5 - 0.3 * x**2 - 0.2 * x**3
    d = dhw - 0.8 * z - 0.5 * c * al
    return d

@handcalc()
def critical_stifness(fac: float,hoh: float,l: float,y_rep:float=10)-> float:
    EI_cr=((y_rep * fac * hoh * l**4 )/(math.pi**4))*10**9
    return EI_cr

@handcalc()
def mult_factor(I_y:float,y_m:float,EI_cr:float,E:float=21000)->float:
    n= (E * I_y*10**4)/(y_m * EI_cr)
    return n

@handcalc()
def N_factor(n: float) -> float:
    N= n / (n - 1)
    return N

# Handle the special case where n is equal to 1
def calculate_N_factor(n: float) -> float:
    if n == 1:
        return float('inf')  # or any other value you prefer
    else:
        return N_factor(n)

