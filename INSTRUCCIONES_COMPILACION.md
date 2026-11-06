# Instrucciones de Compilación y Personalización - Boersis Remote Desktop

Este documento contiene los datos de configuración ya incrustados en el proyecto, las rutas exactas para sustituir tus logotipos/iconos y la guía paso a paso para compilar el ejecutable `.exe` en GitHub Actions.

---

## 1. Parámetros Incrustados en el Binario

Los siguientes valores ya se encuentran programados de forma nativa en el código fuente:

* **Nombre de la Aplicación:** Boersis Remote Desktop
* **Nombre de la Empresa:** Boersis
* **Servidor ID (Rendezvous):** `rd.boersis.net`
* **Servidor Relay:** `rd.boersis.net`
* **Clave Pública del Servidor (`RS_PUB_KEY`):** `6sdyEUFxf0J6TRjUcVhb+3FcKp4w0pxthuicXmSqDXc=`
* **Contraseña Permanente por Defecto:** `Sb8670**`

---

## 2. Imágenes y Logos Instalados (Cubo Boersis)

Todos los recursos gráficos del Cubo Boersis ya fueron procesados, convertidos y colocados en sus respectivas carpetas:

| Archivo / Ruta relativa | Formato / Tamaño | Estado | Descripción y Ubicación en la App |
| :--- | :--- | :--- | :--- |
| `flutter/windows/runner/resources/app_icon.ico` | `.ico` (Multitamaño 16x16 a 256x256) | ✅ Instalado | **Icono principal** del ejecutable `.exe` y de la ventana de Windows. |
| `res/icon.ico` | `.ico` (Multitamaño 16x16 a 256x256) | ✅ Instalado | Icono secundario del instalador y ejecutable portátil. |
| `res/tray-icon.ico` | `.ico` (16x16 y 32x32) | ✅ Instalado | Icono de la bandeja del sistema (junto al reloj de Windows). |
| `res/icon.png` | `.png` (256x256) | ✅ Instalado | Imagen en mapa de bits de alta resolución con transparencia. |
| `res/logo.svg` | `.svg` (Vectorial 2048x2048) | ✅ Instalado | Logotipo vectorial de la marca. |
| `flutter/assets/icon.svg` | `.svg` (Vectorial 2048x2048) | ✅ Instalado | Icono dentro de la interfaz gráfica Flutter. |
| `res/32x32.png`, `res/64x64.png`, `res/128x128.png`, `res/128x128@2x.png`, `res/mac-icon.png` | `.png` (Varios tamaños) | ✅ Instalado | Iconos auxiliares para empaquetado. |

---

## 3. Todo Listo para Subir a GitHub y Compilar

Todos los archivos de código, configuración y recursos gráficos ya han sido modificados, verificados y confirmados en el historial de Git local.

### Paso 1: Subir los cambios a tu repositorio en GitHub

Abre una terminal (PowerShell o Git Bash) en la raíz de esta carpeta (`c:\Factor-ia\RustDesk`) y ejecuta:

```bash
git push origin master
```

> **Nota:** Si Git te solicita credenciales:
> * **Username:** Tu usuario de GitHub (`odbia26`).
> * **Password:** Un **Personal Access Token** de GitHub (creado en *GitHub > Settings > Developer Settings > Personal access tokens* con permisos `repo` y `workflow`).

---

### Paso 2: Habilitar Permisos de Actions en GitHub

Para que GitHub Actions pueda compilar y almacenar los archivos ejecutables:

1. Ve a tu repositorio en GitHub: [https://github.com/odbia26/rustdesk](https://github.com/odbia26/rustdesk)
2. Haz clic en la pestaña **Settings** (Configuración del repositorio).
3. En el menú lateral izquierdo, haz clic en **Actions** > **General**.
4. Desplázate hacia abajo hasta la sección **Workflow permissions**.
5. Selecciona la opción **Read and write permissions**.
6. Haz clic en el botón **Save** (Guardar).

---

### Paso 3: Disparar la Compilación de Windows

Hemos creado un flujo dedicado y optimizado llamado **`Build Windows EXE`** que compila únicamente la versión de Windows (ahorrando tiempo y evitando fallos con macOS o Android):

1. En la página de tu repositorio en GitHub, haz clic en la pestaña **Actions**.
2. En la lista de flujos del panel izquierdo, selecciona: **`Build Windows EXE`**.
3. Haz clic en el botón desplegable de la derecha: **`Run workflow`**.
4. Asegúrate de que esté seleccionada la rama **`master`** y pulsa el botón verde **Run workflow**.

---

### Paso 4: Descargar el Ejecutable Generado

1. La compilación tardará habitualmente entre **15 y 20 minutos** en los servidores de GitHub.
2. Verás la ejecución en curso en la pestaña **Actions**. Cuando termine con éxito, aparecerá un icono verde de verificación (✔).
3. Haz clic en el nombre de la ejecución completada.
4. En la parte inferior de la página, en la sección **Artifacts**, encontrarás listo para descargar:
   * **`windows-flutter-x86_64-exe`**
5. Al descomprimir el archivo `.zip` que descargas, obtendrás tu instalador y ejecutable final listo para usar: **Boersis Remote Desktop**. Al abrirlo, se conectará de inmediato a tu servidor `rd.boersis.net` con tu logotipo y la contraseña permanente predeterminada.

