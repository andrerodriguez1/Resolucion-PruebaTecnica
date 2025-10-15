import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from shapely import wkb 
import os

# --- 1. CONFIGURACIÓN DE CONEXIÓN ---
PG_HOST = 'localhost'
PG_PORT = 5432           
PG_USER = 'usergeo'
PG_PASS = '5659'
PG_DB = 'geodatabase'

# 2. Crear la cadena de conexión
conn_string = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'
engine = create_engine(conn_string)

# 3. Definir la ruta del archivo Parquet
geop_path = './data/soy_performance_2019_2021_2023.parquet'
TABLA_DESTINO = 'performance_parquet_layer'
# NOMBRE CORREGIDO: La columna de geometría es 'geom'
GEOM_COL_NAME = 'geom'

if not os.path.exists(geop_path):
    print(f"Error: Archivo no encontrado en {os.path.abspath(geop_path)}")
    exit()

print(f"Leyendo archivo Parquet: {geop_path}")

# El primer intento con gpd.read_file() falló, así que vamos directo al respaldo con pandas.
try:
    # 4. Leer el Parquet como un DataFrame simple (requiere pyarrow, que ya instalaste)
    df = pd.read_parquet(geop_path)
    
    print(f"Éxito: Leído como Pandas DataFrame con {len(df)} filas.")
    
    # 5. Convertir la columna 'geom' (que asumimos está en formato WKT) a geometría
    if GEOM_COL_NAME in df.columns:
        # Renombrar la columna 'geom' a 'geometry' para que GeoPandas la reconozca
        # y convertir el texto WKT a objetos Shapely.
        df['geometry'] = df[GEOM_COL_NAME].apply(wkb.loads)
        
        # Crear el GeoDataFrame (CRS 4326 es el estándar, ajusta si es necesario)
        gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
        
        # Opcional: Eliminar la columna de geometría original para evitar duplicados en PostGIS
        gdf = gdf.drop(columns=[GEOM_COL_NAME]) 
        
        print(f"Éxito: Conectado a la columna '{GEOM_COL_NAME}' y convertido a GeoDataFrame.")
    else:
        # Si la columna 'geom' no existe, hay un problema con el archivo.
        print(f"\nFATAL: La columna espacial esperada ('{GEOM_COL_NAME}') no se encontró en el archivo Parquet.")
        exit()

except Exception as e:
    print(f"\nFATAL: Error irrecuperable al procesar o conectar.")
    print(f"Detalle del error: {e}")
    exit()


# 6. Cargar el GeoDataFrame a PostGIS
print(f"Iniciando conexión y carga a la tabla '{TABLA_DESTINO}'...")

gdf.to_postgis(
    name=TABLA_DESTINO,
    con=engine,
    if_exists='replace',
    index=False # No es necesario crear un índice en PostGIS para la clave primaria de Pandas
)

print(f"\n🎉 ¡Carga COMPLETADA! La tabla '{TABLA_DESTINO}' está en tu base de datos PostGIS.")