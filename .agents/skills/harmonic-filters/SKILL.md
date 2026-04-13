---
name: harmonic-filters
description: Calculation of LC Harmonic Filters (First Order). Use this skill whenever the user mentions designing LC harmonic filters to obtain precise and deterministic results for L and C values.
---

# harmonic-filters

This skill allows for the precise and deterministic calculation of inductance ($L$) and capacitance ($C$) values for tuned harmonic filters. It delegates the underlying calculations to a Python script attached to the skill to avoid mathematical LLM hallucinations.

-# Instructions

--# Step 1: Collect Parameters
Verify that you have all four essential parameters from the user's request. If any are missing, DO NOT assume or invent values. Instead, politely start a step-by-step interview process with the user to collect the missing data:

- `power_kvar`: Filter nominal reactive power (Qn) in kiloVolt-Amperes reactive (kVAr)
- `voltage_kv`: System nominal line voltage (Un) in kiloVolt (kV)
- `frequency_hz`: Nominal system frequency (fn) in Hertz (Hz)
- `harmonic_order`: Desired tuning order (hr) in per unit (p.u.)

--# Step 2: Expert Harmonic Verification
Evaluate the `harmonic_order` provided by the user before executing any command.
If the user requests tuning to a pure integer harmonic (e.g., 5.0, 7.0, 11.0):

1. Pause the workflow and do not execute the script yet.
2. Politely warn them that tuning exactly to a pure harmonic can be dangerous due to possible parallel resonance with the grid.
3. Give them a practical example. For example: "If you want to tune to the 5th harmonic, you can design a filter at 4.8 p.u."
4. Wait for them to respond with their final decision on the `harmonic_order` before proceeding.

--# Step 3: Execute Calculation
Once all 4 parameters are collected and validated, use the terminal command tool (`run_command`) to run the calculation script:

```bash
python .agents/skills/harmonic-filters/scripts/filter_calculations.py --power_kvar [value] --voltage_kv [value] --frequency_hz [value] --harmonic_order [value]
```

--# Step 4: Present Results
The script returns a JSON response containing the exact analytical values. Do not calculate or alter the values yourself.
Read the template found in `assets/report-template.md` and securely use it as a strict guide to fill in the data and present the final results to the user.

**STRICT CONSTRAINT:** This is an engineering skill. You MUST provide the output in TEXT-ONLY format using the Markdown template. DO NOT use image generation tools, dashboards, or any visual tools to represent the data. Do not invent any new formatting or visual layouts.

--# Troubleshooting
If the terminal command fails or the Python script returns a JSON with `"status": "error"`, DO NOT attempt to do the math yourself. Present the error message to the user and ask them to verify if the parameters make physical/electrical sense.
