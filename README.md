# 🛰️ Desafío Práctico - Desarrollador de Datos Geoespaciales  
**Candidata:** Geof. Andrea Rodríguez  
**Empresa:** Garruchos Agropecuaria  
**Fecha:** Octubre 2025  

---

## 📘 Introducción  
Este proyecto corresponde al desafío práctico para la posición de **Desarrollador/a de Datos Geoespaciales**, cuyo objetivo es:  
1. Construir una infraestructura reproducible basada en Docker y PostGIS.  
2. Ingerir y analizar datos geoespaciales (KML, GeoParquet, GeoPackage).  
3. Evaluar correlaciones espaciales de rendimiento de soja y generar clusters, hotspots y análisis de baja productividad.  

---

## ⚙️ Requisitos  
- Docker Desktop ≥ 4.0  
- Python ≥ 3.10  
- Conda (opcional pero recomendado)  
- QGIS / DBeaver para visualización  
- Archivo `requirements.txt` incluido en el repositorio  

---

## 🧩 Estructura del proyecto

Resolucion-PruebaTecnica/
	
	|- dockerfile
	|- docker-compose.yml
	|- init.sql
	|
	├── data/
	|  	|- la_magdalena_L4.kml
	|  	|- veris_data.gpkg
	|  	|- soy_performance_2019_2021_2023.parquet
	|
	├── notebooks/
	|  	|- PruebaTécnica_RodriguezAndrea
	| 
	├── outputs/
	|  	|- clusters_rendimiento.gpkg
	|  	|- Analisis_Hotspot_Rendimiento_2021.gpkg
	|  	|- analisis_zonas.csv
	|
	|- requirements.txt
	|- Informe_Tecnico_AndreaRodriguez.pdf

---

## 🐳 Configuración y Ejecución con Docker (Parte 1)

1. **Clonar el proyecto:**
   ```bash
   git clone https://github.com/andrearodriguez/Resolucion-PruebaTecnica.git
   cd Resolucion-PruebaTecnica
   ```

2. **Construir y levantar el contenedor**
	```bash
	docker compose up -d --build 
	```
 
Esto construirá la imagen de Docker, compilará la extensión H3, y levantará el servicio PostGIS/H3 en el puerto 5432.

3. **Verificar el contenedor activo** 
	```bash
	docker ps
	```
 
4. **Carga de Datos (KML, GPKG)** 

Archivo kml:
	```bash
	docker exec postgis_h3_container ogr2ogr -f "PostgreSQL" "PG:host=localhost user=usergeo password=5659 dbname=geodatabase" /app/data/la_magdalena_L4.kml -nln kml_layer -overwrite
	```
	
Archivo gpkg:
	```bash
	docker exec postgis_h3_container ogr2ogr -f "PostgreSQL" "PG:host=localhost user=usergeo password=5659 dbname=geodatabase" /app/data/veris_data.gpkg -nln geopackage_layer -overwrite 
	```
	
5. **Carga del GeoParquet mediante Python (fuera del contenedor)** 

	```bash
	conda create -n geoenv python=3.11
	conda activate geoenv
	conda install --file requirements.txt
	python cargar_geoparquet.py
	```
Al finalizar, los tres archivos estarán cargados en las tablas kml_layer, geopackage_layer, y performance_parquet_layer.

-----------

## 🧠 Análisis de Datos (Parte 2)

1. Abrir la notebook
	notebooks/PruebaTécnica_RodriguezAndrea.ipynb

2. Ejecutar las celdas secuencialmente en Jupyter o Google Colab.

3. Los resultados (correlaciones, clusters, hotspots) se guardan en la carpeta outputs.

------------

## 🗺️ Visualización en QGIS

Se incluye el archivo `Prueba-RodriguezAndrea.qgz`, que contiene las capas cargadas desde la base PostGIS (Lote L4, Veris, Rendimiento, Clusters y Hotspots).  
![Mapa QGIS - Lote L4 La Magdalena](outputs/mapa_qgis.png)

----------

## 🌿 Bonus - Índice Espectral Sentinel-2
En el informe técnico se incluye un planteo sobre el uso de índices espectrales (NDVI) derivados de Sentinel-2 para anticipar zonas de alto o bajo rendimiento, utilizando Google Earth Engine.

-------------

👩‍💻 Autora

Andrea Rodríguez

Geofísica y Científica de Datos

📧 arodriguez8@hotmail.com

📅 Octubre 2025

