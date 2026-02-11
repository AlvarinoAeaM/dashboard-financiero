"""
Script para crear un video demo automatizado del Dashboard
Requiere: selenium, pillow
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

class DashboardVideoCreator:
    """Crea capturas de pantalla para video demo"""
    
    def __init__(self, url="http://localhost:8501"):
        self.url = url
        self.screenshots = []
        
        # Configurar Chrome en modo headless
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")  # Des comentar para headless
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def esperar_carga(self, segundos=3):
        """Espera a que la página cargue"""
        time.sleep(segundos)
    
    def tomar_screenshot(self, nombre):
        """Toma una captura de pantalla"""
        print(f"📸 Capturando: {nombre}")
        
        screenshot = self.driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(screenshot))
        
        filename = f"screenshots/{nombre}.png"
        img.save(filename)
        self.screenshots.append(filename)
        
        return filename
    
    def crear_screenshots_demo(self):
        """Crea todas las capturas para el demo"""
        
        print("🎬 Iniciando captura de screenshots para demo...")
        print(f"🌐 Navegando a: {self.url}")
        
        try:
            # 1. Cargar página principal
            self.driver.get(self.url)
            self.esperar_carga(5)
            self.tomar_screenshot("01_dashboard_principal")
            
            # 2. Scroll para mostrar KPIs
            self.driver.execute_script("window.scrollTo(0, 200)")
            self.esperar_carga(1)
            self.tomar_screenshot("02_kpis_principales")
            
            # 3. Scroll a gráficos de crecimiento
            self.driver.execute_script("window.scrollTo(0, 800)")
            self.esperar_carga(1)
            self.tomar_screenshot("03_analisis_crecimiento")
            
            # 4. Scroll a análisis por segmento
            self.driver.execute_script("window.scrollTo(0, 1400)")
            self.esperar_carga(1)
            self.tomar_screenshot("04_analisis_segmento")
            
            # 5. Scroll a tendencias temporales
            self.driver.execute_script("window.scrollTo(0, 2000)")
            self.esperar_carga(1)
            self.tomar_screenshot("05_tendencias_temporales")
            
            # 6. Scroll a top asesores
            self.driver.execute_script("window.scrollTo(0, 2800)")
            self.esperar_carga(1)
            self.tomar_screenshot("06_top_asesores")
            
            # 7. Scroll a tabla de datos
            self.driver.execute_script("window.scrollTo(0, 3600)")
            self.esperar_carga(1)
            self.tomar_screenshot("07_tabla_datos")
            
            # 8. Mostrar sidebar con filtros
            try:
                # Buscar y hacer click en el botón del sidebar
                sidebar_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSidebar']"))
                )
                self.driver.execute_script("window.scrollTo(0, 0)")
                self.esperar_carga(1)
                self.tomar_screenshot("08_filtros_sidebar")
            except Exception as e:
                print(f"⚠️ No se pudo capturar sidebar: {e}")
            
            # 9. Volver al inicio
            self.driver.execute_script("window.scrollTo(0, 0)")
            self.esperar_carga(1)
            self.tomar_screenshot("09_vista_completa")
            
            print(f"\n✅ Se capturaron {len(self.screenshots)} screenshots")
            print("📁 Ubicación: ./screenshots/")
            
        except Exception as e:
            print(f"❌ Error durante la captura: {str(e)}")
        
        finally:
            self.driver.quit()
    
    def crear_gif(self, output_file="demo.gif", duration=2000):
        """Crea un GIF animado con las screenshots"""
        print(f"\n🎞️ Creando GIF animado...")
        
        try:
            images = [Image.open(img) for img in self.screenshots]
            
            # Guardar como GIF
            images[0].save(
                output_file,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0
            )
            
            print(f"✅ GIF creado: {output_file}")
            
        except Exception as e:
            print(f"❌ Error al crear GIF: {str(e)}")

def main():
    """Función principal"""
    print("=" * 60)
    print("📹 GENERADOR DE SCREENSHOTS PARA VIDEO DEMO")
    print("=" * 60)
    print()
    print("⚠️ IMPORTANTE:")
    print("1. Asegúrate de tener el dashboard corriendo en localhost:8501")
    print("2. Ejecuta: streamlit run Dashboard.py")
    print("3. Luego ejecuta este script")
    print()
    input("Presiona ENTER cuando el dashboard esté listo...")
    
    # Crear directorio de screenshots si no existe
    import os
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        print("✅ Directorio 'screenshots' creado")
    
    # Crear screenshots
    creator = DashboardVideoCreator()
    creator.crear_screenshots_demo()
    
    # Crear GIF (opcional)
    crear_gif = input("\n¿Crear GIF animado? (s/n): ").lower()
    if crear_gif == 's':
        creator.crear_gif()
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print()
    print("📝 Próximos pasos:")
    print("  1. Revisa las screenshots en ./screenshots/")
    print("  2. Usa OBS Studio o Loom para grabar el video")
    print("  3. Edita el video con las screenshots como referencia")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
