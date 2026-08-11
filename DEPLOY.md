# Despliegue: Fichas Técnicas con Formulario

## Arquitectura
- **Formulario HTML** → GitHub Pages
- **PDFs (140 archivos, 843 MB)** → GitHub Releases
- **Leads** → Google Sheets via Apps Script webhook

---

## Paso 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repo: `fichas-tecnicas`
3. Visibilidad: **Public** (necesario para GitHub Pages gratis)
4. Click "Create repository"

## Paso 2: Subir el formulario HTML

Abre una terminal en `C:\Users\atenc\Claude\fichas-tecnicas` y ejecuta:

```bash
git init
git add index.html
git commit -m "Add lead capture form for fichas tecnicas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/fichas-tecnicas.git
git push -u origin main
```

## Paso 3: Activar GitHub Pages

1. Ve a tu repo → Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Click Save
5. Espera ~1 minuto, tu form estará en: `https://TU_USUARIO.github.io/fichas-tecnicas/`

## Paso 4: Subir PDFs como Release

Desde la misma terminal, ejecuta:

```bash
gh release create v1 --title "Fichas Técnicas v1" --notes "140 fichas técnicas en PDF" pdfs/*.pdf
```

> Si no tienes `gh` instalado: https://cli.github.com/
> Si son muchos archivos para un solo comando, usa el script `subir-releases.ps1`

Las URLs de cada PDF serán:
```
https://github.com/TU_USUARIO/fichas-tecnicas/releases/download/v1/nutripro-bio.pdf
https://github.com/TU_USUARIO/fichas-tecnicas/releases/download/v1/progranic-cinnacar.pdf
... etc
```

## Paso 5: Configurar Google Sheets webhook

1. Crea una Google Sheet nueva (o usa una existente)
2. Ve a Extensions → Apps Script
3. Pega el contenido de `google-apps-script.js`
4. Ejecuta la función `setup()` una vez
5. Deploy → New deployment → Web app
   - Execute as: **Me**
   - Who has access: **Anyone**
6. Copia la URL del deployment

## Paso 6: Actualizar las URLs en index.html

Edita `index.html` y reemplaza:

1. `YOUR_GOOGLE_APPS_SCRIPT_URL_HERE` → la URL del paso 5
2. `https://github.com/USUARIO/fichas-tecnicas/releases/download/v1` → tu URL real con tu usuario de GitHub

Haz commit y push:
```bash
git add index.html
git commit -m "Configure webhook and PDF URLs"
git push
```

## Paso 7: Conectar en Wix

En cada página dinámica de producto, el botón "Descargar Ficha Técnica" debe enlazar a:

```
https://TU_USUARIO.github.io/fichas-tecnicas/?p={slug-del-producto}
```

Donde `{slug-del-producto}` es el slug de la URL del producto en Wix.
Por ejemplo, si la página del producto es `/productos/nutripro-bio`, el enlace sería:

```
https://TU_USUARIO.github.io/fichas-tecnicas/?p=nutripro-bio
```

### En Wix con páginas dinámicas:
En el editor de Wix, en el botón de descarga, usa un enlace dinámico:
```
https://TU_USUARIO.github.io/fichas-tecnicas/?p={slug}
```

Donde `{slug}` viene del campo dinámico de la URL del producto.

---

## Actualizar fichas en el futuro

Para reemplazar o agregar PDFs:

```bash
# Eliminar release viejo
gh release delete v1 --yes

# Crear nuevo release con archivos actualizados
gh release create v1 --title "Fichas Técnicas v1" --notes "Fichas actualizadas" pdfs/*.pdf
```

---

## Referencia: Mapping de archivos

Ver `mapping.csv` para la tabla completa de:
- slug → archivo original → URL de descarga
