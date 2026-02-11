"""
Generador de datos de ejemplo para el Dashboard
Útil para demos sin acceso al archivo real
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generar_datos_demo(num_clientes=1000, num_asesores=50):
    """
    Genera datos de ejemplo para el dashboard
    
    Args:
        num_clientes: Número de clientes únicos
        num_asesores: Número de asesores únicos
    """
    
    print("🔄 Generando datos de ejemplo...")
    
    # Listas de datos ficticios
    nombres = [
        "GARCIA RODRIGUEZ", "MARTINEZ LOPEZ", "RODRIGUEZ GARCIA",
        "LOPEZ MARTINEZ", "GONZALEZ PEREZ", "PEREZ GONZALEZ",
        "SANCHEZ RODRIGUEZ", "RAMIREZ LOPEZ", "TORRES GARCIA",
        "FLORES MARTINEZ", "RIVERA LOPEZ", "GOMEZ PEREZ"
    ]
    
    primeros_nombres = ["JUAN", "MARIA", "CARLOS", "ANA", "LUIS", "LAURA", 
                        "PEDRO", "SOFIA", "DIEGO", "VALENTINA", "MIGUEL", "CAMILA"]
    
    segmentos_mesa = [
        "1. BANCA PRIVADA",
        "2. BANCA PREFERENTE",
        "3. INVERSIONISTAS PLATA",
        "4. INVERSIONISTAS ORO",
        "5. BANCA EMPRESARIAL"
    ]
    
    mesas = [
        "BANCA PRIVADA",
        "BANCA PREFERENTE", 
        "INVERSIONISTAS PLATA",
        "INVERSIONISTAS ORO",
        "BANCA EMPRESARIAL"
    ]
    
    segmentos_largo = [
        "INVERSIONISTA DIAMANTE",
        "INVERSIONISTA PLATINO",
        "INVERSIONISTA ORO",
        "INVERSIONISTA PLATA",
        "INVERSIONISTA BRONCE"
    ]
    
    # Generar clientes únicos
    clientes = []
    for i in range(num_clientes):
        nombre = f"{random.choice(primeros_nombres)} {random.choice(nombres)}"
        clientes.append({
            'id': f"{100000 + i}",
            'nombre': nombre
        })
    
    # Generar asesores únicos
    asesores = []
    for i in range(num_asesores):
        nombre = f"{random.choice(primeros_nombres)} {random.choice(nombres)}"
        asesores.append({
            'doc_id': f"{19000000 + i}",
            'nombre': nombre
        })
    
    # Generar registros para cada año y mes
    años = [2017, 2018, 2019, 2020, 2021, 2022]
    meses = list(range(1, 13))
    
    todos_los_datos = []
    
    for año in años:
        print(f"  Generando datos para {año}...")
        
        datos_año = []
        
        for mes in meses:
            # Seleccionar un subconjunto aleatorio de clientes para este mes
            clientes_mes = random.sample(clientes, k=int(num_clientes * 0.7))
            
            for cliente in clientes_mes:
                # Asignar asesor aleatorio
                asesor = random.choice(asesores)
                
                # Seleccionar segmento
                segmento_idx = random.randint(0, len(segmentos_mesa) - 1)
                
                # Generar AUM con cierta correlación al segmento
                if segmento_idx == 0:  # Banca Privada
                    aum_base = random.uniform(50_000_000, 500_000_000)
                elif segmento_idx == 1:  # Banca Preferente
                    aum_base = random.uniform(20_000_000, 100_000_000)
                elif segmento_idx == 2:  # Inversionistas Plata
                    aum_base = random.uniform(10_000_000, 50_000_000)
                elif segmento_idx == 3:  # Inversionistas Oro
                    aum_base = random.uniform(5_000_000, 30_000_000)
                else:  # Banca Empresarial
                    aum_base = random.uniform(30_000_000, 200_000_000)
                
                # Agregar tendencia de crecimiento
                factor_crecimiento = 1 + ((año - 2017) * 0.05) + (mes * 0.001)
                aum = aum_base * factor_crecimiento
                
                # Agregar algo de ruido
                aum = aum * random.uniform(0.9, 1.1)
                
                registro = {
                    'Año': año,
                    'Numero de Mes': mes,
                    'Segmento Mesa': segmentos_mesa[segmento_idx],
                    'Doc. Identificación': asesor['doc_id'],
                    'Asesor Comercial': asesor['nombre'],
                    'Mesa': mesas[segmento_idx],
                    'Numero  Identificación': cliente['id'],
                    'Nombre Cliente': cliente['nombre'],
                    'Segmento Largo': segmentos_largo[segmento_idx],
                    'AUM Fin de Mes': round(aum, 2),
                    'No.Clientes': 1 if random.random() > 0.5 else 0,
                    'Segmento Cliente': 'Basico',
                    'AUM Fin de Mes ': round(aum * random.uniform(0.1, 0.3), 2)
                }
                
                datos_año.append(registro)
        
        todos_los_datos.extend(datos_año)
    
    # Crear DataFrame
    df = pd.DataFrame(todos_los_datos)
    
    print(f"\n Datos generados:")
    print(f"   Total de registros: {len(df):,}")
    print(f"   Clientes únicos: {df['Numero  Identificación'].nunique():,}")
    print(f"   Asesores únicos: {df['Asesor Comercial'].nunique():,}")
    print(f"   AUM Total: ${df['AUM Fin de Mes'].sum()/1e9:.2f}B")
    
    return df

def guardar_excel(df, nombre_archivo='AUMs_Clientes_DEMO.xlsx'):
    """Guarda el DataFrame en formato Excel con múltiples hojas"""
    
    print(f"\n Guardando datos en {nombre_archivo}...")
    
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        for año in [2017, 2018, 2019, 2020, 2021, 2022]:
            df_año = df[df['Año'] == año]
            df_año.to_excel(writer, sheet_name=f'Base {año}', index=False)
            print(f"   Hoja 'Base {año}' creada ({len(df_año):,} registros)")
    
    print(f"\n Archivo guardado exitosamente!")
    print(f"   Ubicación: {nombre_archivo}")
    
    return nombre_archivo

def main():
    """Función principal"""
    print("=" * 60)
    print("  GENERADOR DE DATOS DEMO - DASHBOARD FINANCIERO")
    print("=" * 60)
    print()
    
    # Configuración
    num_clientes = 1000  # Ajusta según necesites
    num_asesores = 50
    
    print(f"  Configuración:")
    print(f"  Clientes: {num_clientes}")
    print(f"  Asesores: {num_asesores}")
    print(f"  Período: 2017-2022")
    print(f"  Meses: 12 por año")
    print()
    
    # Generar datos
    df = generar_datos_demo(num_clientes, num_asesores)
    
    # Guardar
    archivo = guardar_excel(df)
    
    print("\n" + "=" * 60)
    print(" PROCESO COMPLETADO")
    print()
    print(" Próximos pasos:")
    print("  1. Renombrar el archivo a 'AUMs_Clientes.xlsx' si lo deseas")
    print("  2. Ejecutar: streamlit run Dashboard.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
