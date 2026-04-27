# 📁 Folder Lister

**Folder Lister** es una aplicación de escritorio desarrollada en Python diseñada para la gestión, organización, análisis y documentación de archivos de video. Está especialmente pensada para procesar grabaciones (como cámaras de seguridad o CCTV), permitiendo clasificar videos, realizar capturas de pantalla precisas con anotaciones y exportar la información estructurada para la creación ágil de reportes.

---

## ✨ Características Principales

* **Gestión y Ordenamiento Intuitivo:** Carga directorios completos de videos (formato `.mkv`) y permite reordenar la lista manualmente utilizando una interfaz de *Drag & Drop* (arrastrar y soltar).
* **Reproductor de Video Integrado:** Visualiza los videos directamente dentro de la aplicación gracias a su motor de renderizado basado en OpenCV.
* **Captura de Evidencia y Anotaciones:** Extrae *frames* específicos de los videos, guárdalos como imágenes `.png` y añade observaciones detalladas (con un límite visual de diseño de 219 caracteres).
* **Exportación y Generación de Casos:** Copia, enumera y traslada archivos a rutas de destino configurables (mediante `config.json`). Incluye automatización para generar "Casos Base", integrándose directamente con Microsoft PowerPoint para armar presentaciones con las evidencias.
* **Interfaz Moderna (UI):** Diseño limpio y profesional en modo oscuro, con botones estilizados y barras de desplazamiento personalizadas, superando las limitaciones visuales tradicionales de Tkinter.

---

## 🏗️ Arquitectura del Proyecto

El código fuente sigue los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**, asegurando escalabilidad, mantenibilidad y una clara separación de responsabilidades:

* 📂 `src/domains/`: Contiene el modelo de negocio central (`VideoInfo`) utilizando `dataclasses` para gestionar los metadatos de los videos.
* 📂 `src/repository/`: Maneja la persistencia en memoria y el estado de la lista de videos (`VideoRepository`).
* 📂 `src/service/`: Concentra la lógica de negocio, como el procesamiento de directorios, estrategias de ordenamiento y gestión de casos (`VideoService`, `CasoService`).
* 📂 `src/infrastructure/`: Gestiona las interacciones con sistemas externos, como la comunicación directa con la API de Windows para PowerPoint (`PowerPointClient`).
* 📂 `src/ui/`: Componentes visuales desarrollados en Tkinter, divididos lógicamente entre la ventana principal (`interfaz.py`), el reproductor (`reproductor.py`) y el sistema de estilos (`styles.py`).
* 📂 `src/factory/` y `src/validators/`: Implementación de patrones de diseño (como `VideoFactory` para la creación de objetos a partir de nombres de archivos) y validaciones estrictas de rutas para evitar errores de procesamiento.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** `tkinter` (Librería estándar)
* **Procesamiento de Video:** `OpenCV` (`cv2`) y `Pillow` (`PIL`) para la manipulación y renderizado de imágenes.
* **Integración de Reportes:** `pywin32` (`win32com.client`) para el control automatizado de Microsoft PowerPoint.

---

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/folder-lister.git](https://github.com/tu-usuario/folder-lister.git)
   cd folder-lister


2. **Crear un entorno virtual (Recomendado):**
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instalar las dependencias:**
   ```bash
    pip install -r requirements.txt

4. **Configuración:** Verifica y edita el archivo config.json en el directorio principal para establecer las rutas de origen y destino predeterminadas de tus proyectos.

5. **Ejecutar la aplicación**
   ```bash
   python main.py

## 💡 Flujo de Trabajo Básico

1. Abre la aplicación y selecciona el directorio que contiene los videos a analizar.

2. Utiliza la lista principal para revisar el orden de los archivos; arrastra y suelta si necesitas corregir la cronología.

3. Haz doble clic en cualquier video para abrir el Reproductor Integrado.

4. Navega hasta el momento exacto, toma una captura de pantalla y añade tu observación.

5. Cierra el reproductor y utiliza la opción **"Crear caso base"** para exportar los archivos y generar el reporte de PowerPoint automáticamente.
