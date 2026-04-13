import math
import argparse
import json

def calculate_lc_filter(power_kvar: float, voltage_kv: float, frequency_hz: float, harmonic_order: float) -> dict:
    """
    Calculates the L and C parameters for a first-order LC harmonic filter.
    
    Args:
        power_kvar: Filter nominal reactive power (Qn) in kVAr.
        voltage_kv: System nominal line voltage (Un) in kV.
        frequency_hz: Nominal system frequency (fn) in Hz.
        harmonic_order: Desired tuning order (hr) in p.u.
        
    Returns:
        A dictionary with capacitance (uF), inductance (mH), and verification values.
    """
    
    # Convert kv and kvar to v and var
    power_var = power_kvar * 1000.0
    voltage_v = voltage_kv * 1000.0
    
    # Angular frequency (rad/s)
    omega_n = 2 * math.pi * frequency_hz
    
    # Capacitance (C) calculation
    # Formula: C = ((hr^2 - 1) / hr^2) * (Qn / (omega_n * Un^2))
    c_num = (harmonic_order**2) - 1
    c_den = harmonic_order**2
    c_factor = power_var / (omega_n * (voltage_v**2))
    capacitance = (c_num / c_den) * c_factor
    
    # Inductance (L) calculation
    # Formula: L = (1 / (hr^2 - 1)) * (Un^2 / (omega_n * Qn))
    l_den = (harmonic_order**2) - 1
    l_factor = (voltage_v**2) / (omega_n * power_var)
    inductance = (1 / l_den) * l_factor
    
    # Verification: omega_r = 1 / sqrt(L * C)
    omega_r_calc = 1 / math.sqrt(inductance * capacitance)
    hr_calc = omega_r_calc / omega_n

    return {
        "capacitance_uf": capacitance * 1e6,
        "inductance_mh": inductance * 1e3,
        "omega_n_rad_s": omega_n,
        "tuned_harmonic_check": hr_calc,
        "status": "success"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate LC filter parameters.")
    parser.add_argument("--power_kvar", type=float, required=True, help="Nominal reactive power (Qn) in kVAr.")
    parser.add_argument("--voltage_kv", type=float, required=True, help="Nominal system voltage (Un) in kV.")
    parser.add_argument("--frequency_hz", type=float, required=True, help="Nominal frequency (fn) in Hz.")
    parser.add_argument("--harmonic_order", type=float, required=True, help="Tuning order (hr) in p.u.")
    
    args = parser.parse_args()
    
    try:
        result = calculate_lc_filter(
            power_kvar=args.power_kvar,
            voltage_kv=args.voltage_kv,
            frequency_hz=args.frequency_hz,
            harmonic_order=args.harmonic_order
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
