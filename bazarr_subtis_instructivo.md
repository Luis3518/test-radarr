# Guía de Instalación: Provider Subtis en Bazarr

## Paso 0: Identificar rutas actuales

Localiza las siguientes carpetas en tu instalación actual de Bazarr:
- `\bazarr\frontend\build\`
- `\bazarr\providers\`

## Paso 1: Clonar el repositorio de Bazarr

Descarga el repositorio de Bazarr. Puedes:
- Clonarlo con Git
- Descargar el ZIP y descomprimirlo

## Paso 2: Agregar entrada para Subtis

Edita el archivo: `\bazarr-master\frontend\src\pages\Settings\Providers\list.ts`

Agrega la siguiente entrada:

```javascript
{
  key: "subtis",
  name: "subtis",
  description: "Encontrá el subtítulo perfecto para cualquier película",
},
```

## Paso 3: Compilar el frontend

Abre una consola en la carpeta `\bazarr-master\frontend` y ejecuta:

```bash
npm run build
```

## Paso 4: Actualizar carpeta build

Copia todo el contenido de `\bazarr-master\frontend\build\` y pégalo en la carpeta build de tu instalación actual de Bazarr:
- Destino: `\bazarr\frontend\build\`

## Paso 5: Instalar el provider

Descarga el archivo `subtis.py` desde: https://github.com/Luis3518/test-radarr/blob/main/bazarr/providers/subtis.py

Luego cópialo a la carpeta providers de tu instalación actual:
- Destino: `\bazarr\providers\`

---

**¡Listo!** El provider Subtis debería estar disponible en Bazarr.