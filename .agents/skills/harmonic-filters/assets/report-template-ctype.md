# 📝 C-type Harmonic Filter Design Report

**Input Parameters:**

* **Power (Qn):** `[Insert]` kVAr
* **Voltage (Un):** `[Insert]` kV
* **Frequency (fn):** `[Insert]` Hz
* **Tuning Order (hr):** `[Insert]` p.u.
* **Quality Factor (qf @ fr):** `[Insert]`

**Calculated Parameters:**

| Parameter | Value | Unit |
| --- | --- | --- |
| Main Capacitor (C2) | `[Insert]` | μF |
| Auxiliary Capacitor (C1) | `[Insert]` | μF |
| Inductance (L) | `[Insert]` | mH |
| Damping Resistance (Rp) | `[Insert]` | Ω |

**Verification Details:**

* **L-C1 Resonance Check:** `[Insert]` (should be ≈ 1.0, confirming resonance at fundamental frequency)
* **Calculation Status:** ✅ Success

_Note: Values are calculated analytically to ensure precision. The quality factor is evaluated at the tuned frequency (fr = hr × fn). In the C-type topology, the L-C1 branch is tuned to the fundamental frequency, and C2 is the main series capacitor._
