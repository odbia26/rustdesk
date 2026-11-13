#!/usr/bin/env python3
import sys
import re
import os

profile = sys.argv[1].lower().strip() if len(sys.argv) > 1 else "cliente"
print(f"[apply_profile] Applying build profile: '{profile}'")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
config_rs = os.path.join(base_dir, "libs", "hbb_common", "src", "config.rs")
common_rs = os.path.join(base_dir, "src", "common.rs")
runner_rc = os.path.join(base_dir, "flutter", "windows", "runner", "Runner.rc")
info_plist = os.path.join(base_dir, "flutter", "macos", "Runner", "Info.plist")
desktop_file = os.path.join(base_dir, "res", "rustdesk.desktop")
manifest_xml = os.path.join(base_dir, "flutter", "android", "app", "src", "main", "AndroidManifest.xml")

with open(config_rs, "r", encoding="utf-8") as f:
    config_content = f.read()

common_content = ""
if os.path.exists(common_rs):
    with open(common_rs, "r", encoding="utf-8") as f:
        common_content = f.read()

runner_content = ""
if os.path.exists(runner_rc):
    with open(runner_rc, "r", encoding="utf-8") as f:
        runner_content = f.read()

plist_content = ""
if os.path.exists(info_plist):
    with open(info_plist, "r", encoding="utf-8") as f:
        plist_content = f.read()

desktop_content = ""
if os.path.exists(desktop_file):
    with open(desktop_file, "r", encoding="utf-8") as f:
        desktop_content = f.read()

manifest_content = ""
if os.path.exists(manifest_xml):
    with open(manifest_xml, "r", encoding="utf-8") as f:
        manifest_content = f.read()

# PIN por defecto activo en AMBOS perfiles (02518670)
if '// unlock-pin not preset for operador' in config_content:
    config_content = config_content.replace(
        '// unlock-pin not preset for operador',
        'res.entry("unlock-pin".to_owned()).or_insert_with(|| "02518670".to_owned());'
    )
if '// unlock-pin empty for operador' in config_content:
    config_content = config_content.replace(
        '// unlock-pin empty for operador',
        'if k == "unlock-pin" {\n            return "02518670".to_owned();\n        }'
    )
if 'let pin = CONFIG2.read().unwrap().unlock_pin.clone();\n        if pin.is_empty()' not in config_content:
    config_content = config_content.replace(
        'CONFIG2.read().unwrap().unlock_pin.clone()',
        'let pin = CONFIG2.read().unwrap().unlock_pin.clone();\n        if pin.is_empty() {\n            "02518670".to_string()\n        } else {\n            pin\n        }'
    )

if profile == "operador":
    # 1. Modo Bidireccional (permite conexiones salientes hacia clientes)
    config_content = re.sub(
        r'map_or\((true|false),\s*\|x\|\s*x\s*==\s*\("incoming"\)\)',
        'map_or(false, |x| x == ("incoming"))',
        config_content
    )
    # 2. Permitir cambiar contraseñas permanentes (is_disable_change_permanent_password = false)
    config_content = re.sub(
        r'(is_disable_change_permanent_password\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>false)',
        config_content
    )
    # 3. Mantener BLOQUEADO el cambio de ID (is_disable_change_id = true)
    config_content = re.sub(
        r'(is_disable_change_id\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>true)',
        config_content
    )
    # 4. Ajustar res.entry de disable-change-permanent-password a 'N'
    config_content = config_content.replace(
        'res.entry("disable-change-permanent-password".to_owned()).or_insert_with(|| "Y".to_owned());',
        'res.entry("disable-change-permanent-password".to_owned()).or_insert_with(|| "N".to_owned());'
    )
    # 5. Ajustar get_option en config.rs para que disable-change-permanent-password no retorne 'Y'
    get_opt_cliente = (
        'if k == "disable-change-permanent-password" || k == "disable-change-id" {\n'
        '            return "Y".to_owned();\n'
        '        }'
    )
    get_opt_operador = (
        'if k == "disable-change-id" {\n'
        '            return "Y".to_owned();\n'
        '        }\n'
        '        if k == "disable-change-permanent-password" {\n'
        '            return "N".to_owned();\n'
        '        }'
    )
    if get_opt_cliente in config_content:
        config_content = config_content.replace(get_opt_cliente, get_opt_operador)

    # 6. Ajustar get_builtin_option en src/common.rs para que el botón sea visible en Flutter
    if common_content:
        common_content = common_content.replace(
            '"disable-change-permanent-password" => "Y".to_owned(),',
            '"disable-change-permanent-password" => "N".to_owned(),'
        )

    # 7. Actualizar descripción en Runner.rc, Info.plist, rustdesk.desktop y AndroidManifest.xml
    if runner_content:
        runner_content = runner_content.replace(
            'VALUE "FileDescription", "Boersis Remote Desktop" "\\0"',
            'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"'
        )
        runner_content = runner_content.replace(
            'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"',
            'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"'
        )
    if plist_content:
        plist_content = plist_content.replace(
            "<string>Boersis Remote Desktop</string>",
            "<string>Boersis Remote Desktop - Operador</string>"
        )
    if desktop_content:
        desktop_content = desktop_content.replace(
            "Name=Boersis Remote Desktop",
            "Name=Boersis Remote Desktop - Operador"
        )
    if manifest_content:
        manifest_content = manifest_content.replace(
            'android:label="Boersis Remote Desktop"',
            'android:label="Boersis Remote Desktop - Operador"'
        )

elif profile == "cliente":
    # 1. Modo Solo Entrante (Soporte)
    config_content = re.sub(
        r'map_or\((true|false),\s*\|x\|\s*x\s*==\s*\("incoming"\)\)',
        'map_or(true, |x| x == ("incoming"))',
        config_content
    )
    # 2. Bloquear cambio de contraseña permanente (is_disable_change_permanent_password = true)
    config_content = re.sub(
        r'(is_disable_change_permanent_password\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>true)',
        config_content
    )
    # 3. Bloquear cambio de ID (is_disable_change_id = true)
    config_content = re.sub(
        r'(is_disable_change_id\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>true)',
        config_content
    )
    # 4. Ajustar res.entry de disable-change-permanent-password a 'Y'
    config_content = config_content.replace(
        'res.entry("disable-change-permanent-password".to_owned()).or_insert_with(|| "N".to_owned());',
        'res.entry("disable-change-permanent-password".to_owned()).or_insert_with(|| "Y".to_owned());'
    )
    # 5. Ajustar get_option en config.rs
    get_opt_cliente = (
        'if k == "disable-change-permanent-password" || k == "disable-change-id" {\n'
        '            return "Y".to_owned();\n'
        '        }'
    )
    get_opt_operador = (
        'if k == "disable-change-id" {\n'
        '            return "Y".to_owned();\n'
        '        }\n'
        '        if k == "disable-change-permanent-password" {\n'
        '            return "N".to_owned();\n'
        '        }'
    )
    if get_opt_operador in config_content:
        config_content = config_content.replace(get_opt_operador, get_opt_cliente)

    # 6. Ajustar get_builtin_option en src/common.rs
    if common_content:
        common_content = common_content.replace(
            '"disable-change-permanent-password" => "N".to_owned(),',
            '"disable-change-permanent-password" => "Y".to_owned(),'
        )

    # 7. Actualizar descripción en Runner.rc, Info.plist, rustdesk.desktop y AndroidManifest.xml
    if runner_content:
        runner_content = runner_content.replace(
            'VALUE "FileDescription", "Boersis Remote Desktop" "\\0"',
            'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"'
        )
        runner_content = runner_content.replace(
            'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"',
            'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"'
        )
    if plist_content:
        plist_content = plist_content.replace(
            "<string>Boersis Remote Desktop - Operador</string>",
            "<string>Boersis Remote Desktop</string>"
        )
    if desktop_content:
        desktop_content = desktop_content.replace(
            "Name=Boersis Remote Desktop - Operador",
            "Name=Boersis Remote Desktop"
        )
    if manifest_content:
        manifest_content = manifest_content.replace(
            'android:label="Boersis Remote Desktop - Operador"',
            'android:label="Boersis Remote Desktop"'
        )

with open(config_rs, "w", encoding="utf-8") as f:
    f.write(config_content)

if common_content and os.path.exists(common_rs):
    with open(common_rs, "w", encoding="utf-8") as f:
        f.write(common_content)

if runner_content and os.path.exists(runner_rc):
    with open(runner_rc, "w", encoding="utf-8") as f:
        f.write(runner_content)

if plist_content and os.path.exists(info_plist):
    with open(info_plist, "w", encoding="utf-8") as f:
        f.write(plist_content)

if desktop_content and os.path.exists(desktop_file):
    with open(desktop_file, "w", encoding="utf-8") as f:
        f.write(desktop_content)

if manifest_content and os.path.exists(manifest_xml):
    with open(manifest_xml, "w", encoding="utf-8") as f:
        f.write(manifest_content)

print(f"[apply_profile] Successfully configured profile '{profile}'.")
