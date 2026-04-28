---
name: harmonic-filters
description: Calculation of Harmonic Filters (LC, HP, and C-type). Use this skill whenever the user mentions designing harmonic filters (LC first-order, HP high-pass second-order, or C-type third-order) to obtain precise and deterministic results for filter component values.
---

# harmonic-filters

This skill allows for the precise and deterministic calculation of component values for three types of harmonic filters:

- **LC (First Order)**: Calculates inductance (L) and capacitance (C).
- **HP — High Pass (Second Order)**: Calculates L, C, and damping resistance (Rp).
- **C-type (Third Order)**: Calculates two capacitors (C1, C2), inductance (L), and damping resistance (Rp).

It delegates the underlying calculations to a Python script attached to the skill to avoid mathematical LLM hallucinations.

## Instructions

### Step 1: Identify Filter Type

Determine which filter type the user wants to design. The user may explicitly say LC, HP, or C-type, or you may need to ask. If unclear, present the three options and let them choose.

### Step 2: Collect Parameters

Verify that you have all essential parameters from the user's request. If any are missing, DO NOT assume or invent values. Instead, politely start a step-by-step interview process with the user to collect the missing data.

**Parameters required for ALL filter types:**

- `power_kvar`: Filter nominal reactive power (Qn) in kiloVolt-Amperes reactive (kVAr)
- `voltage_kv`: System nominal line voltage (Un) in kiloVolt (kV)
- `frequency_hz`: Nominal system frequency (fn) in Hertz (Hz)
- `harmonic_order`: Desired tuning order (hr) in per unit (p.u.)

**STRICT RULE — Unit Normalization:**
The script expects `power_kvar` in **kVAr** and `voltage_kv` in **kV**. Users often express power in MVAr or voltage in V. You MUST normalize before executing:

| User says | Conversion | Example |
| --- | --- | --- |
| X **MVAr** | Multiply by 1,000 → kVAr | 10 MVAr → `--power_kvar 10000` |
| X **VAr** | Divide by 1,000 → kVAr | 5000000 VAr → `--power_kvar 5000` |
| X **V** | Divide by 1,000 → kV | 30000 V → `--voltage_kv 30` |

After converting, **echo the normalized values back to the user** before executing the script. For example: _"I'll calculate with Qn = 10,000 kVAr and Un = 30 kV."_ This gives the user a chance to catch conversion errors.

**Additional parameter required for HP and C-type filters ONLY:**

- `quality_factor`: Filter quality factor at the tuned frequency (qf @ fr), dimensionless.

**STRICT RULE:** The quality factor is frequency-dependent. It must be evaluated at the tuned frequency (fr = hr × fn). When collecting this parameter, always inform the user: _"The quality factor (qf) depends on the frequency. Please provide the value corresponding to the tuned frequency (fr = hr × fn Hz)."_ Typical values range from 0.5 to 5, but this is not a hard limit.

### Step 3: Expert Verification

Before executing any command, evaluate the parameters provided by the user as a domain expert would:

**3a. Harmonic Order check:**
If the user requests tuning to a pure integer harmonic (e.g., 5.0, 7.0, 11.0):

1. Pause the workflow and do not execute the script yet.
2. Politely warn them that tuning exactly to a pure harmonic can be dangerous due to possible parallel resonance with the grid.
3. Give them a practical example. For example: "If you want to tune to the 5th harmonic, you can design a filter at 4.8 p.u."
4. Wait for them to respond with their final decision on the `harmonic_order` before proceeding.

**3b. Quality Factor check (HP and C-type only):**
If the user provides a `quality_factor` outside the typical range of 0.5 to 5:

1. Do not reject the value, but politely warn the user that typical quality factors for damped filters are in the 0.5–5 range.
2. Explain that values outside this range may result in poor damping performance or excessive losses.
3. Suggest a typical starting point (e.g., 2.0) if the user is unsure.
4. Let the user confirm or adjust the value before proceeding.

### Step 4: Execute Calculation

Once all parameters are collected and validated, use the terminal command tool (`run_command`) to run the calculation script.

**For LC filters:**

```bash
python .agents/skills/harmonic-filters/scripts/filter_calculations.py --filter_type lc --power_kvar [value] --voltage_kv [value] --frequency_hz [value] --harmonic_order [value]
```

**For HP filters:**

```bash
python .agents/skills/harmonic-filters/scripts/filter_calculations.py --filter_type hp --power_kvar [value] --voltage_kv [value] --frequency_hz [value] --harmonic_order [value] --quality_factor [value]
```

**For C-type filters:**

```bash
python .agents/skills/harmonic-filters/scripts/filter_calculations.py --filter_type ctype --power_kvar [value] --voltage_kv [value] --frequency_hz [value] --harmonic_order [value] --quality_factor [value]
```

### Step 5: Sanity Check (Post-Calculation)

Before presenting the results, check the `sanity_check` field in the script's JSON output. The script automatically validates two physical quantities that do NOT self-cancel with unit errors:

1. **Rated current** ($I = Q_n / (\sqrt{3} \cdot U_n)$): Must be between 1 A and 5000 A for typical MV/HV filter banks. A current of 0.19 A at 30 kV is a red flag.
2. **Capacitance magnitude**: At voltages > 1 kV, filter capacitors below 0.1 μF are extremely unusual.

**If `sanity_check_passed` is `false`:**
1. DO NOT present the results to the user.
2. Read the `warnings` array in the JSON for specific guidance.
3. The most common cause is passing MVAr directly as kVAr (e.g., `--power_kvar 10` instead of `--power_kvar 10000` for a 10 MVAr filter).
4. Review your unit conversions from Step 2 and re-run the script.

> **Future note:** Inverse calculations (given C, L, R → derive Qn, hr, qf) can provide an even stronger cross-check. This is planned but not yet implemented.

### Step 6: Present Results

The script returns a JSON response containing the exact analytical values. Do not calculate or alter the values yourself.

Read the appropriate template from the `assets/` folder based on the filter type:

- **LC** → `assets/report-template-lc.md`
- **HP** → `assets/report-template-hp.md`
- **C-type** → `assets/report-template-ctype.md`

Use the template as a strict guide to fill in the data and present the final results to the user.

**STRICT CONSTRAINT:** This is an engineering skill. You MUST provide the output in TEXT-ONLY format using the Markdown template. DO NOT use image generation tools, dashboards, or any visual tools to represent the data. Do not invent any new formatting or visual layouts.

## Troubleshooting

If the terminal command fails or the Python script returns a JSON with `"status": "error"`, DO NOT attempt to do the math yourself. Present the error message to the user and ask them to verify if the parameters make physical/electrical sense.

A common error for HP and C-type filters is forgetting the `--quality_factor` argument. Verify you included it in the command.
