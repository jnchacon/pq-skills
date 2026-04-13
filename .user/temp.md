Cálculo de Filtros de Armónicos LC (Primer Orden)

Esta Skill permite calcular de manera precisa y determinística los valores de inductancia ($L$) y capacitancia ($C$) para filtros de armónicos sintonizados. Utiliza las fórmulas de diseño para filtros de primer orden donde la sintonía se define por la relación entre la reactancia inductiva y capacitiva a la frecuencia nominal.

Parámetros

{
  "type": "object",
  "properties": {
    "power_var": {
      "type": "number",
      "description": "Potencia reactiva del filtro (Qf) en Volt-Amperios reactivos (VAr)."
    },
    "voltage_v": {
      "type": "number",
      "description": "Tensión nominal de línea del sistema (Uf) en Voltios (V)."
    },
    "frequency_hz": {
      "type": "number",
      "description": "Frecuencia nominal del sistema (fn) en Hercios (Hz)."
    },
    "harmonic_order": {
      "type": "number",
      "description": "Orden de sintonía deseado (hr) en por unidad (p.u.). Ejemplo: 4.7 para protección de bancos de capacitores."
    }
  },
  "required": ["power_var", "voltage_v", "frequency_hz", "harmonic_order"]
}


Script

filter_calculations.py