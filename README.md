# Radarr + Prowlarr + Bazarr Docker Setup

## ¿Qué es esto?
- **Radarr**: Aplicación para gestionar y descargar películas automáticamente
- **Prowlarr**: Gestor de indexers/trackers que se sincroniza con Radarr
- **Bazarr**: Gestor de subtítulos que se integra con Radarr para descargar subtítulos automáticamente

## Estructura del proyecto
- `radarr/data/` - Datos y configuración de Radarr
- `prowlarr/data/` - Datos y configuración de Prowlarr
- `bazarr/data/` - Datos y configuración de Bazarr
- `movies/` - Carpeta donde se guardan las películas descargadas
- `downloads/` - Carpeta para descargas del cliente
- `docker-compose.yml` - Configuración de los contenedores

## Requisitos
- Docker y Docker Compose instalados

## Cómo ejecutar

1. **Inicia los contenedores:**
   ```bash
   docker-compose up -d
   ```

2. **Accede a las aplicaciones:**
   - Radarr: `http://localhost:7878`
   - Prowlarr: `http://localhost:9696`
   - Bazarr: `http://localhost:6767`

3. **Ver logs (opcional):**
   ```bash
   docker-compose logs -f radarr
   docker-compose logs -f prowlarr
   docker-compose logs -f bazarr
   ```

4. **Detener los contenedores:**
   ```bash
   docker-compose down
   ```

## Configuración entre servicios
Para que los servicios se comuniquen entre sí dentro de Docker, usa los nombres de los contenedores en lugar de `localhost`:
- **Radarr Server:** `http://radarr:7878`
- **Prowlarr Server:** `http://prowlarr:9696`
- **Bazarr Server:** `http://bazarr:6767`

Por ejemplo, al configurar Prowlarr en Radarr, usa `http://radarr:7878` como URL del servidor.

## Notas
- El contenedor se reinicia automáticamente si se detiene inesperadamente
- Los datos persisten en las carpetas del proyecto
- Cambia la zona horaria en el archivo docker-compose.yml si es necesario (actual: UTC)

--
configure prowlarr como indexer, agregue solo BitSearch.
Luego configuro desde prowlarr la integracion con radarr y desde radarr el indexer prowlarr.

importas las peliculas desde el directorio "download"
Desde "library import" seleccionando la carpeta te permite importarlo.

yifi subtitles me funcionó