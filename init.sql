-- init.sql
-- Conexión a la base de datos principal, asumiendo que ya fue creada por Docker Compose
\c geodatabase

-- Habilita la extensión h3-pg (Si ya está instalada en el contenedor, se activa aquí)
CREATE EXTENSION IF NOT EXISTS h3;

-- Muestra la versión para confirmación
SELECT h3_pg_version();