# Instrucciones de Compilación y Personalización - Boersis Remote Desktop

Este documento contiene los datos de configuración incrustados en el binario, las opciones predeterminadas de seguridad y comportamiento, los recursos gráficos instalados y la guía paso a paso para compilar el ejecutable `.exe` en GitHub Actions.

---

## 1. Parámetros Incrustados en el Binario

Los siguientes valores se encuentran programados de forma nativa en el código fuente:

* **Nombre de la Aplicación:** Boersis Remote Desktop
* **Nombre de la Empresa:** Boersis
* **Servidor ID (Rendezvous):** `rd.boersis.net`
* **Servidor Relay:** `rd.boersis.net`
* **Clave Pública del Servidor (`RS_PUB_KEY`):** `6sdyEUFxf0J6TRjUcVhb+3FcKp4w0pxthuicXmSqDXc=`
* **Contraseña Permanente por Defecto:** `Sb8670**`

---

## 2. Opciones de Configuración y Seguridad Predefinidas

El cliente viene pre-configurado de fábrica con las siguientes políticas y ajustes:

1. **Protección de Configuración con PIN de Administrador:**
   * **PIN configurado:** `02518670`
   * Las pestañas de **Seguridad** y **Red** inician bloqueadas. Para ver o modificar cualquier parámetro protegido, se debe hacer clic en *"Desbloquear ajustes de seguridad / red"* e introducir el PIN `02518670`.
   * Los usuarios normales no pueden cambiar la contraseña permanente ni modificar el ID.
2. **Modo Solo Entrante (Cliente de Soporte):**
   * La interfaz muestra únicamente el panel con el **ID y la Contraseña** para que el cliente reciba asistencia técnica remota.
   * La sección de control remoto saliente está oculta y las conexiones hacia el exterior están bloqueadas a nivel de código.
   * El botón de **Ajustes (Configuración)** permanece accesible en el encabezado para que el administrador pueda abrirlo y desbloquear las opciones con el PIN.
3. **Servicio de Windows Automático:**
   * Al instalarse en Windows, se registra como Servicio del Sistema con inicio automático (`start= auto`), garantizando disponibilidad 24/7 incluso sin iniciar sesión de usuario en Windows.
   * La opción de detener el servicio (`hide-stop-service`) está oculta para usuarios no autorizados.
4. **Tema Oscuro Predeterminado:**
   * La interfaz inicia automáticamente en modo oscuro (Dark theme).
5. **Idioma Predeterminado Español:**
   * Todo el cliente inicia en idioma español (`es`).
6. **Ocultar Fondo de Pantalla:**
   * Durante las sesiones remotas entrantes, se quita el fondo de pantalla del escritorio (`allow-remove-wallpaper: Y`) para maximizar la velocidad y ahorrar ancho de banda.
7. **Actualizaciones Desactivadas:**
   * No busca actualizaciones automáticamente ni las descarga (`enable-check-update: N`, `allow-auto-update: N`), manteniendo la versión corporativa homologada.
8. **Sincronización de Portapapeles:**
   * Habilitada entre sesiones (`allow-sync-clipboard-between-sessions: Y`) para facilitar el copiado y pegado de texto.
9. **Método de Verificación: Usar Ambas Contraseñas:**
   * Configurado en `use-both-passwords`. Se puede acceder tanto con la contraseña fija (`Sb8670**`) como con la contraseña temporal de un solo uso.
10. **Sin Impresora RustDesk:**
    * El controlador de impresora remota ha sido desactivado y removido del instalador y de las opciones de configuración.

---

## 3. Imágenes y Logos Instalados (Cubo Boersis)

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

## 4. Pasos Siguientes para Compilar tu Ejecutable

Todos los archivos de código, configuración, logos e iconos ya han sido modificados, verificados y confirmados en el historial de Git local. Para generar el archivo `.exe` con GitHub Actions, sigue estos pasos:

### Paso 1: Subir los cambios a tu repositorio en GitHub

Abre una terminal (PowerShell, Símbolo del Sistema o Git Bash) en la carpeta del proyecto (`c:\Factor-ia\RustDesk`) y ejecuta:

```bash
git push origin master
```

> **Autenticación en GitHub:**
> Si Git te pide usuario y contraseña:
> * **Username:** Tu usuario de GitHub (`odbia26`).
> * **Password:** Un **Personal Access Token (classic)** de GitHub (no tu contraseña de cuenta).
>   * Para crearlo si no lo tienes: Ve a GitHub > **Settings** (arriba a la derecha en tu perfil) > **Developer settings** > **Personal access tokens** > **Tokens (classic)** > **Generate new token**.
>   * Asígnale los permisos `repo` y `workflow`, copia el token generado y pégalo como contraseña en la terminal.

---

### Paso 2: Habilitar Permisos de Escritura en GitHub Actions (Solo la primera vez)

Para que los servidores de GitHub Actions tengan permisos de guardar el ejecutable compilado:

1. Ve a tu repositorio en GitHub: [https://github.com/odbia26/rustdesk](https://github.com/odbia26/rustdesk)
2. Haz clic en la pestaña **Settings** (Configuración del repositorio).
3. En el menú lateral izquierdo, ve a **Actions** > **General**.
4. Desplázate hacia abajo hasta la sección **Workflow permissions**.
5. Selecciona la opción **Read and write permissions**.
6. Haz clic en el botón verde **Save** (Guardar).

---

### Paso 3: Disparar la Compilación y Escoger la Versión

Hemos preparado un flujo dedicado llamado **`Build Windows EXE`** con un selector desplegable para elegir qué variante compilar:

1. En la página de tu repositorio en GitHub, entra a la pestaña **Actions**:
   👉 [https://github.com/odbia26/rustdesk/actions](https://github.com/odbia26/rustdesk/actions)
2. En la barra lateral izquierda, selecciona el flujo de trabajo: **`Build Windows EXE`**.
3. En la parte derecha, haz clic en el botón desplegable **`Run workflow`**.
4. Verás las opciones:
   * **Rama:** Deja seleccionada `master`.
   * **Versión a compilar (desplegable):**
     * **`cliente`** *(Opción predeterminada)*: Genera la versión de soporte para clientes (solo entrante, protegida con el PIN `02518670`, servicio automático de Windows).
     * **`operador`**: Genera la versión completa bidireccional para el técnico (permite conectarse y controlar clientes, panel de control completo, sin bloqueo solo-entrante).
5. Pulsa el botón verde **Run workflow**.

---

### Paso 4: Descargar el Ejecutable Generado (.exe)

1. El proceso de compilación tomará habitualmente entre **15 y 20 minutos** en las máquinas virtuales de GitHub.
2. Podrás ver el progreso en tiempo real dentro de la pestaña **Actions**. Cuando termine satisfactoriamente, aparecerá una marca de verificación verde (✔).
3. Haz clic en el nombre de la ejecución completada (por ejemplo: `Build Windows EXE #1`).
4. En la parte inferior de la página, en la sección **Artifacts**, encontrarás listo para descargar según la versión que escogiste:
   * **`Boersis-Remote-Desktop-cliente-x86_64`** (si compilaste la versión Cliente).
   * **`Boersis-Remote-Desktop-operador-x86_64`** (si compilaste la versión Operador).
5. Al hacer clic, se descargará un archivo comprimido `.zip`. Descomprímelo en tu equipo y obtendrás el instalador y ejecutable final: **Boersis Remote Desktop**.
6. Al ejecutarlo en cualquier máquina, comprobarás que:
   * Muestra el logotipo del **Cubo Boersis** y el icono personalizado.
   * Se conecta automáticamente a tu servidor **`rd.boersis.net`**.
   * Si es la versión **cliente**: opera en modo solo entrante protegido por PIN.
   * Si es la versión **operador**: opera en modo completo con control remoto saliente hacia tus clientes.
