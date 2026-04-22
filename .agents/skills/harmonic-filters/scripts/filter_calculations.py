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
        "filter_type": "LC (First Order)",
        "capacitance_uf": capacitance * 1e6,
        "inductance_mh": inductance * 1e3,
        "omega_n_rad_s": omega_n,
        "tuned_harmonic_check": hr_calc,
        "status": "success"
    }


def calculate_hp_filter(power_kvar: float, voltage_kv: float, frequency_hz: float, harmonic_order: float, quality_factor: float) -> dict:
    """
    Calculates the L, C, and Rp parameters for a second-order HP (High Pass) harmonic filter.

    The C and L values use the same formulas as the LC filter. The additional
    output is the damping resistance Rp, which is calculated from the quality
    factor provided by the user.

    IMPORTANT: The quality factor (qfF) is frequency-dependent. The value
    provided must correspond to the tuned frequency (fr = hr * fn). The script
    uses it as given; the agent must inform the user about this dependency.

    Args:
        power_kvar: Filter nominal reactive power (Qn) in kVAr.
        voltage_kv: System nominal line voltage (Un) in kV.
        frequency_hz: Nominal system frequency (fn) in Hz.
        harmonic_order: Desired tuning order (hr) in p.u.
        quality_factor: Filter quality factor at the tuned frequency (qfF @ fr), dimensionless.

    Returns:
        A dictionary with capacitance (uF), inductance (mH), resistance (Ohm), and verification values.
    """

    # Convert kv and kvar to v and var
    power_var = power_kvar * 1000.0
    voltage_v = voltage_kv * 1000.0

    # Angular frequency (rad/s)
    omega_n = 2 * math.pi * frequency_hz

    # Capacitance (C) — same formula as LC
    # Formula: C = ((hr^2 - 1) / hr^2) * (Qf / (omega_n * Uf^2))
    c_num = (harmonic_order**2) - 1
    c_den = harmonic_order**2
    c_factor = power_var / (omega_n * (voltage_v**2))
    capacitance = (c_num / c_den) * c_factor

    # Inductance (L) — same formula as LC
    # Formula: L = (1 / (hr^2 - 1)) * (Uf^2 / (omega_n * Qf))
    l_den = (harmonic_order**2) - 1
    l_factor = (voltage_v**2) / (omega_n * power_var)
    inductance = (1 / l_den) * l_factor

    # Damping resistance (Rp)
    # Formula: Rp = qfF @ fr * (hr * omega_n) * L
    resistance = quality_factor * (harmonic_order * omega_n) * inductance

    # Verification: omega_r = 1 / sqrt(L * C)
    omega_r_calc = 1 / math.sqrt(inductance * capacitance)
    hr_calc = omega_r_calc / omega_n

    return {
        "filter_type": "HP (Second Order)",
        "capacitance_uf": capacitance * 1e6,
        "inductance_mh": inductance * 1e3,
        "resistance_ohm": resistance,
        "quality_factor": quality_factor,
        "omega_n_rad_s": omega_n,
        "tuned_harmonic_check": hr_calc,
        "status": "success"
    }


def calculate_ctype_filter(power_kvar: float, voltage_kv: float, frequency_hz: float, harmonic_order: float, quality_factor: float) -> dict:
    """
    Calculates the C1, C2, L, and Rp parameters for a third-order C-type harmonic filter.

    IMPORTANT: The quality factor (qfF) is frequency-dependent. The value
    provided must correspond to the tuned frequency (fr = hr * fn). Typical
    values range from 0.5 to 5, but this is not a hard limit.

    Args:
        power_kvar: Filter nominal reactive power (Qn) in kVAr.
        voltage_kv: System nominal line voltage (Un) in kV.
        frequency_hz: Nominal system frequency (fn) in Hz.
        harmonic_order: Desired tuning order (hr) in p.u.
        quality_factor: Filter quality factor at the tuned frequency (qfF @ fr), dimensionless.

    Returns:
        A dictionary with C1 (uF), C2 (uF), inductance (mH), resistance (Ohm), and verification values.
    """

    # Convert kv and kvar to v and var
    power_var = power_kvar * 1000.0
    voltage_v = voltage_kv * 1000.0

    # Angular frequency (rad/s)
    omega_n = 2 * math.pi * frequency_hz

    # Main capacitor C2
    # Formula: C2 = Qf / (omega_n * Uf^2)
    c2 = power_var / (omega_n * (voltage_v**2))

    # Auxiliary capacitor C1
    # Formula: C1 = C2 * (hr^2 - 1)
    c1 = c2 * ((harmonic_order**2) - 1)

    # Inductance (L)
    # Formula: L = 1 / (C1 * omega_n^2)
    inductance = 1 / (c1 * (omega_n**2))

    # Damping resistance (Rp)
    # Formula: Rp = qfF @ fr * (hr * omega_n) * L
    resistance = quality_factor * (harmonic_order * omega_n) * inductance

    # Verification: The L-C1 branch resonates at omega_n (fundamental freq)
    # omega_r_c1 = 1 / sqrt(L * C1) should equal omega_n
    omega_r_c1 = 1 / math.sqrt(inductance * c1)
    hr_c1_check = omega_r_c1 / omega_n  # Should be ~1.0 (fundamental)

    return {
        "filter_type": "C-type (Third Order)",
        "capacitance_c1_uf": c1 * 1e6,
        "capacitance_c2_uf": c2 * 1e6,
        "inductance_mh": inductance * 1e3,
        "resistance_ohm": resistance,
        "quality_factor": quality_factor,
        "omega_n_rad_s": omega_n,
        "lc1_resonance_check": hr_c1_check,
        "status": "success"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate harmonic filter parameters (LC, HP, or C-type).")
    parser.add_argument("--filter_type", type=str, choices=["lc", "hp", "ctype"], default="lc",
                        help="Type of filter to calculate: lc (default), hp, or ctype.")
    parser.add_argument("--power_kvar", type=float, required=True, help="Nominal reactive power (Qn) in kVAr.")
    parser.add_argument("--voltage_kv", type=float, required=True, help="Nominal system voltage (Un) in kV.")
    parser.add_argument("--frequency_hz", type=float, required=True, help="Nominal frequency (fn) in Hz.")
    parser.add_argument("--harmonic_order", type=float, required=True, help="Tuning order (hr) in p.u.")
    parser.add_argument("--quality_factor", type=float, default=None,
                        help="Filter quality factor at tuned frequency (qfF @ fr). Required for HP and C-type filters.")

    args = parser.parse_args()

    try:
        if args.filter_type == "lc":
            result = calculate_lc_filter(
                power_kvar=args.power_kvar,
                voltage_kv=args.voltage_kv,
                frequency_hz=args.frequency_hz,
                harmonic_order=args.harmonic_order
            )
        elif args.filter_type in ("hp", "ctype"):
            if args.quality_factor is None:
                raise ValueError(
                    f"--quality_factor is required for '{args.filter_type}' filters. "
                    "Please provide the quality factor at the tuned frequency (qfF @ fr)."
                )
            calc_fn = calculate_hp_filter if args.filter_type == "hp" else calculate_ctype_filter
            result = calc_fn(
                power_kvar=args.power_kvar,
                voltage_kv=args.voltage_kv,
                frequency_hz=args.frequency_hz,
                harmonic_order=args.harmonic_order,
                quality_factor=args.quality_factor
            )

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
