# 1. Imagen Base: PostgreSQL 15
FROM postgis/postgis:15-3.4

# 2. Instalación de Dependencias de Compilación y Herramientas GDAL/OGR
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        postgresql-server-dev-15 \
        gdal-bin \
        libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. COMPILACIÓN E INSTALACIÓN DE H3-PG
WORKDIR /tmp
RUN git clone --branch v4.1.1 https://github.com/zachasme/h3-pg.git && \
    cd h3-pg && \
    make && \
    make install

# 4. Inicialización de la Base de Datos
COPY init.sql /docker-entrypoint-initdb.d/