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

## Configuración inicial básica

### Radarr
1. Importar películas desde el directorio `downloads`
2. Usar "Library Import" seleccionando la carpeta para importar el contenido

### Bazarr
1. **Conectar a Radarr:** Configurar la conexión con el servidor Radarr
2. **Agregar provider:** Yify Subtitles funciona bien como proveedor
3. **Crear perfil de subtítulos:**
   - Para test inicial: varios idiomas
   - Para desarrollo de subtítulos: usar solo español (buscar películas sin subtítulos)
4. **Cambiar perfil de subtítulos:** Desde el apartado películas usando "Mass Edit"

### Prowlarr
1. **Configurar como indexer:** Agregar BitSearch como indexer de prueba
2. **Integración con Radarr:**
   - Configurar la integración desde Prowlarr hacia Radarr
   - Configurar el indexer Prowlarr desde Radarr
