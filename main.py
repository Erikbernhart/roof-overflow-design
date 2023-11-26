from handcalcs.decorator import handcalc
import forallpeople as si

@handcalc()
def debit(area: float, n: float, ir=float) -> float:
    """
    calculates the debit of rainwater with the constant ir:5*10-5 from NEN1991-1-1-3 table NB 1
    area is in m^2, and n is the number of overloads per area.

    """
    ir=5*10**-5
    Qhi = (area * ir) / n
    return round(Qhi,3)


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

from typing import Optional

def calculate_ligger_properties(roof_type: str, dhw: float, al: Optional[float] = 0, z: float = 0) -> float:
    if roof_type == "flat roof":
        # Flat roof logic
        d = dhw
    elif roof_type == "curved":
        # Curved logic
        d = dhw - 0.8 * z
    elif roof_type == "sloped":
        # Sloped logic
        if dhw > al:
            d = dhw - 0.5 * al
        else:
            z = 0
            x = 1 - ((dhw - 0.8 * z) / al)
            c = 0.5 - 0.3 * x**2 - 0.2 * x**3
            d = d_hw - c * al
    elif roof_type == "curved and sloped":
        # Curved and sloped logic
        if dhw > al:
            d = dhw - 0.8 * z - 0.5 * al
        else:
            x = 1 - ((dhw - 0.8 * z) / al)
            c = 0.5 - 0.3 * x**2 - 0.2 * x**3
            d = dhw - 0.8 * z - 0.5 * c * al
    else:
        raise ValueError("Invalid roof_type value")

    return d



