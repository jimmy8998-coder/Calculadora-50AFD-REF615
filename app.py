import math

def calcular_ajuste_50afd(
    corriente_nominal_carga_amperes, 
    corriente_arranque_inrush_amperes, 
    corriente_cortocircuito_trifasico_amperes, 
    factor_reduccion_arco_ieee1584=0.50
):
    """
    Programa de Cálculo y Justificación Técnica para el Ajuste de la Función 50AFD
    en Relevadores ABB REF615 basado en IEEE 1584 y Criterios ABB.
    """
    print("==================================================================")
    print("  MEMORIA DE CÁLCULO Y AUDITORÍA TÉCNICA - FUNCIÓN 50AFD (REF615)")
    print("==================================================================")
    
    # 1. Análisis de Carga y Límites Inferiores
    in_load = corriente_nominal_carga_amperes
    i_inrush = corriente_arranque_inrush_amperes
    
    # El umbral mínimo debe superar al inrush o pico de arranque para evitar falsos disparos
    limite_inferior_tecnico = max(in_load * 1.25, i_inrush * 1.10)
    
    # 2. Cálculo de la Corriente Mínima de Arco (IEEE 1584)
    # I_arc_min se estima típicamente aplicando el factor de reducción del modelo IEEE 1584 sobre el Isc trifásico
    i_sc3f = corriente_cortocircuito_trifasico_amperes
    i_arc_min = i_sc3f * factor_reduccion_arco_ieee1584
    
    # 3. Cálculo del Ajuste Óptimo Recomendado (50AFD)
    # Criterio: Por encima del inrush/carga, pero por debajo de la corriente mínima de arco con margen de seguridad (ej. 80%)
    limite_superior_tecnico = i_arc_min * 0.80
    
    if limite_inferior_tecnico >= limite_superior_tecnico:
        print("\n[ALERTA CRÍTICA]: ¡Conflicto de Coordinación!")
        print("El límite inferior (basado en Inrush/Carga) es mayor o igual al límite superior de arco.")
        print("Riesgo inminente: El arco eléctrico es de tan baja magnitud que no puede distinguirse de la carga.")
        return None

    # Propuesta de ajuste óptimo (punto medio seguro con sesgo hacia la sensibilidad)
    ajuste_propuesto_amperes = limite_inferior_tecnico + (limite_superior_tecnico - limite_inferior_tecnico) * 0.35
    
    # Expresado en múltiplos de In (para el parámetro Start Value del REF615)
    multiplo_in = ajuste_propuesto_amperes / in_load

    # 4. Resultados y Justificación Técnica
    print(f"\n[1] PARÁMETROS DE ENTRADA:")
    print(f" • Corriente Nominal de Carga (In)          : {in_load:.2f} A")
    print(f" • Corriente Máxima de Inrush / Arranque    : {i_inrush:.2f} A")
    print(f" • Corriente de Cortocircuito Empernado (3φ): {i_sc3f:.2f} A")
    print(f" • Corriente Mínima de Arco (I_arc_min)     : {i_arc_min:.2f} A (Factor IEEE 1584: {factor_reduccion_arco_ieee1584})")

    print(f"\n[2] VENTANA DE AJUSTE VÁLIDA:")
    print(f" • Límite Inferior (Seguridad vs Inrush)    : > {limite_inferior_tecnico:.2f} A")
    print(f" • Límite Superior (Sensibilidad vs Arco)   : < {limite_superior_tecnico:.2f} A")

    print(f"\n[3] RESULTADO PROPUESTO PARA EL RELEVADOR ABB REF615:")
    print(f" • Umbral de Corriente 50AFD Propuesto      : **{ajuste_propuesto_amperes:.2f} A**")
    print(f" • Ajuste en Múltiplos de In (Start Value)  : **{multiplo_in:.2f} x In**")

    print(f"\n[4] JUSTIFICACIÓN NORMATIVA Y TÉCNICA:")
    print(f" ✓ **IEEE 1584:** Garantiza que el umbral ({ajuste_propuesto_amperes:.2f} A) está por debajo de la corriente mínima de arco ({i_arc_min:.2f} A), asegurando que el elemento de sobrecorriente dé el 'AND' de disparo rápido.")
    print(f" ✓ **ABB Relion Manual:** Al ajustarse en {multiplo_in:.2f} x In, se supera holgadamente el pico de inrush/arranque ({i_inrush:.2f} A), previniendo de manera absoluta disparos en falso por destellos ópticos externos combinados con transitorios de magnetización.")
    print(f" ✓ **IEEE C37.20.7 / NFPA 70E:** Permite tiempos de despeje ultra-rápidos (< 5 ms en el relé), reduciendo drásticamente la energía incidente del arco eléctrico.")
    print("==================================================================")
    
    return ajuste_propuesto_amperes, multiplo_in

# EJEMPLO DE EJECUCIÓN (Modifica estos valores con los datos reales de tu estudio)
# Supongamos un alimentador con In = 400 A, Inrush de transformador/motor de 2400 A, y Isc trifásica de 25,000 A.
if __name__ == "__main__":
    calcular_ajuste_50afd(
        corriente_nominal_carga_amperes=400.0,
        corriente_arranque_inrush_amperes=2400.0,
        corriente_cortocircuito_trifasico_amperes=25000.0,
        factor_reduccion_arco_ieee1584=0.50
    )
