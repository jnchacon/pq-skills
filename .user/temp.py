import math

def calculate_lc_filter(power_var: float, voltage_v: float, frequency_hz: float, harmonic_order: float) -> dict:
    """
    Calculates the L and C parameters for a first-order LC harmonic filter.
    
    Args:
        power_var: Filter reactive power (Qf) in VAr.
        voltage_v: Filter rated voltage (Uf) in Volts.
        frequency_hz: System rated frequency (fn) in Hz.
        harmonic_order: Tuned frequency (hr) in p.u.
        
    Returns:
        A dictionary with capacitance (F), inductance (H), and verification values.
    """
    
    # Angular frequency (rad/s)
    omega_n = 2 * math.pi * frequency_hz
    
    # Capacitance (C) calculation
    # Formula: C = ((hr^2 - 1) / hr^2) * (Qf / (omega_n * Uf^2))
    c_num = (harmonic_order**2) - 1
    c_den = harmonic_order**2
    c_factor = power_var / (omega_n * (voltage_v**2))
    capacitance = (c_num / c_den) * c_factor
    
    # Inductance (L) calculation
    # Formula: L = (1 / (hr^2 - 1)) * (Uf^2 / (omega_n * Qf))
    l_den = (harmonic_order**2) - 1
    l_factor = (voltage_v**2) / (omega_n * power_var)
    inductance = (1 / l_den) * l_factor
    
    # Verification: omega_r = 1 / sqrt(L * C)
    omega_r_calc = 1 / math.sqrt(inductance * capacitance)
    hr_calc = omega_r_calc / omega_n

    return {
        "capacitance_farads": capacitance,
        "inductance_henrys": inductance,
        "omega_n_rad_s": omega_n,
        "tuned_harmonic_check": hr_calc,
        "status": "success"
    }