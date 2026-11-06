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

## 2. Rutas para colocar tus Imágenes y Logos

Cuando dispongas de tus recursos gráficos, reemplaza los archivos correspondientes en las siguientes rutas relativas dentro de este proyecto:

| Archivo / Ruta relativa | Formato / Tamaño | Descripción y Ubicación en la App |
| :--- | :--- | :--- |
| `flutter/windows/runner/resources/app_icon.ico` | `.ico` (Multitamaño 16x16 a 256x256) | **Icono principal** del ejecutable `.exe` y de la barra de título de la ventana de Windows. |
| `res/icon.ico` | `.ico` (Multitamaño) | Icono secundario del instalador y empaquetador portátil de Windows. |
| `res/icon.png` | `.png` (256x256 recomendado) | Imagen del icono en alta resolución. |
| `res/logo.svg` | `.svg` (Vectorial) | Logotipo principal de la marca utilizado en la aplicación. |
| `flutter/assets/icon.svg` | `.svg` (Vectorial) | Icono que se muestra dentro de la interfaz de usuario de Flutter. |
| `res/tray-icon.ico` | `.ico` (16x16 / 32x32) | Icono que aparece en la bandeja del sistema (junto al reloj de Windows). |

> **Nota:** Al sustituir los archivos, asegúrate de mantener exactamente los mismos nombres y extensiones.

---

## 3. Pasos Siguientes para Compilar tu `.exe`

### Paso 1: Subir los cambios a tu repositorio en GitHub

1. Abre una terminal (PowerShell o Git Bash) en la raíz de esta carpeta (`c:\Factor-ia\RustDesk`).
2. Si reemplazaste iconos o hiciste ajustes adicionales, confírmalos:
   ```bash
   git add .
   git commit -m "feat: actualizar logos de Boersis"
   ```
3. Sube la rama `master` a tu repositorio remoto:
   ```bash
   git push origin master
   ```
   *(Si el sistema solicita autenticación, ingresa tu usuario de GitHub y un Personal Access Token con permisos `repo` y `workflow`).*

---

### Paso 2: Habilitar Permisos de Actions en GitHub

Para que los servidores de compilación de GitHub puedan empaquetar los artefactos:

1. Ve a tu repositorio en GitHub: [https://github.com/odbia26/rustdesk](https://github.com/odbia26/rustdesk)
2. Haz clic en la pestaña **Settings** (Configuración del repositorio).
3. En el menú de la izquierda, entra a **Actions** > **General**.
4. Desplázate hacia abajo hasta la sección **Workflow permissions**.
5. Selecciona la opción **Read and write permissions**.
6. Haz clic en **Save** (Guardar).

---

### Paso 3: Disparar la Compilación de Windows

Hemos creado un flujo optimizado llamado **Build Windows EXE** que compila únicamente el cliente para Windows (evita compilar macOS, Linux o Android, ahorrando tiempo):

1. En la página de tu repositorio en GitHub, ve a la pestaña **Actions**.
2. En el panel izquierdo, selecciona el flujo: **`Build Windows EXE`**.
3. Haz clic en el botón desplegable de la derecha: **`Run workflow`**.
4. Comprueba que esté seleccionada la rama **`master`** y pulsa el botón verde **Run workflow**.

---

### Paso 4: Descargar el Ejecutable Generado

1. La compilación tomará habitualmente entre **15 y 20 minutos**.
2. Verás la ejecución en curso en la pestaña **Actions**. Cuando termine correctamente, mostrará un círculo verde con check.
3. Haz clic en el nombre de la ejecución completada.
4. En la parte inferior de la página (sección **Artifacts**), encontrarás listo para descargar el archivo:
   * **`windows-flutter-x86_64-exe`**
5. Al descomprimir el archivo `.zip` descargado, obtendrás tu ejecutable final `.exe` de **Boersis Remote Desktop**.
