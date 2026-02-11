"""
Script de prueba para verificar que el Dashboard funciona correctamente
Ejecutar antes de hacer deploy
"""

import sys
import os

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print(" Verificando archivos necesarios...")
    
    archivos_requeridos = [
        'Dashboard.py',
        'requirements.txt',
        'README.md',
        'AUMs_Clientes.xlsx',
        '.streamlit/config.toml'
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   {archivo}")
        else:
            print(f"   {archivo} - NO ENCONTRADO")
            faltantes.append(archivo)
    
    if faltantes:
        print(f"\n  Faltan {len(faltantes)} archivo(s)")
        return False
    else:
        print("\n Todos los archivos necesarios están presentes")
        return True

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n Verificando dependencias...")
    
    dependencias = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'openpyxl': 'openpyxl'
    }
    
    faltantes = []
    for nombre, paquete in dependencias.items():
        try:
            __import__(paquete)
            print(f"   {nombre}")
        except ImportError:
            print(f"   {nombre} - NO INSTALADO")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n  Instala las dependencias faltantes:")
        print(f"   pip install {' '.join(faltantes)}")
        return False
    else:
        print("\n Todas las dependencias están instaladas")
        return True

def verificar_datos():
    """Verifica que el archivo Excel pueda ser leído"""
    print("\n Verificando archivo de datos...")
    
    try:
        import pandas as pd
        
        archivo = 'AUMs_Clientes.xlsx'
        if not os.path.exists(archivo):
            print(f"   Archivo {archivo} no encontrado")
            return False
        
        # Intentar leer una hoja
        df_test = pd.read_excel(archivo, sheet_name='Base 2017', nrows=5)
        print(f"   Archivo Excel legible")
        print(f"   Columnas encontradas: {len(df_test.columns)}")
        print(f"   Tamaño del archivo: {os.path.getsize(archivo) / (1024*1024):.2f} MB")
        return True
        
    except Exception as e:
        print(f"   Error al leer Excel: {str(e)}")
        return False

def verificar_python_version():
    """Verifica la versión de Python"""
    print("\n Verificando versión de Python...")
    
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   Versión compatible")
        return True
    else:
        print("    Se recomienda Python 3.8 o superior")
        return False

def verificar_estructura_datos():
    """Verifica la estructura del DataFrame"""
    print("\n Verificando estructura de datos...")
    
    try:
        import pandas as pd
        
        columnas_esperadas = [
            'Año', 'Numero de Mes', 'Segmento Mesa', 'Doc. Identificación',
            'Asesor Comercial', 'Mesa', 'Numero  Identificación', 
            'Nombre Cliente', 'Segmento Largo', 'AUM Fin de Mes', 
            'No.Clientes', 'Segmento Cliente'
        ]
        
        df_test = pd.read_excel('AUMs_Clientes.xlsx', sheet_name='Base 2017', nrows=10)
        
        columnas_faltantes = [col for col in columnas_esperadas if col not in df_test.columns]
        
        if columnas_faltantes:
            print(f"   Columnas faltantes: {columnas_faltantes}")
            print(f"   Columnas encontradas: {list(df_test.columns)}")
            return False
        else:
            print(f"   Estructura de datos correcta")
            print(f"   Primeras filas: {len(df_test)} registros de prueba")
            return True
            
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

def crear_screenshots_dir():
    """Crea directorio para screenshots si no existe"""
    print("\n Verificando directorio de screenshots...")
    
    if not os.path.exists('screenshots'):
        try:
            os.makedirs('screenshots')
            print("   Directorio 'screenshots' creado")
        except Exception as e:
            print(f"  ⚠️  No se pudo crear directorio: {str(e)}")
            return False
    else:
        print("   Directorio 'screenshots' ya existe")
    
    return True

def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 60)
    print(" VERIFICACIÓN DE DASHBOARD FINANCIERO")
    print("=" * 60)
    
    checks = [
        verificar_python_version(),
        verificar_archivos(),
        verificar_dependencias(),
        verificar_datos(),
        verificar_estructura_datos(),
        crear_screenshots_dir()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print(" ¡TODAS LAS VERIFICACIONES PASARON!")
        print("\n Puedes ejecutar el dashboard con:")
        print("   streamlit run Dashboard.py")
        print("\n Para deploy, sigue las instrucciones en INSTRUCCIONES.md")
    else:
        print("  ALGUNAS VERIFICACIONES FALLARON")
        print("\n Por favor corrige los errores antes de continuar")
        print(" Consulta el README.md para más información")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
