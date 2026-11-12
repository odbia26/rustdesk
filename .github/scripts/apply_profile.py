#!/usr/bin/env python3
import sys
import re
import os

profile = sys.argv[1].lower().strip() if len(sys.argv) > 1 else "cliente"
print(f"[apply_profile] Applying build profile: '{profile}'")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
config_rs = os.path.join(base_dir, "libs", "hbb_common", "src", "config.rs")
runner_rc = os.path.join(base_dir, "flutter", "windows", "runner", "Runner.rc")
info_plist = os.path.join(base_dir, "flutter", "macos", "Runner", "Info.plist")
desktop_file = os.path.join(base_dir, "res", "rustdesk.desktop")
manifest_xml = os.path.join(base_dir, "flutter", "android", "app", "src", "main", "AndroidManifest.xml")

with open(config_rs, "r", encoding="utf-8") as f:
    config_content = f.read()

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

if profile == "operador":
    # 1. Modo Bidireccional (permite conexiones salientes hacia clientes)
    config_content = re.sub(
        r'map_or\((true|false),\s*\|x\|\s*x\s*==\s*\("incoming"\)\)',
        'map_or(false, |x| x == ("incoming"))',
        config_content
    )
    # 2. Desactivar forzado de PIN para operador
    config_content = config_content.replace(
        'res.entry("unlock-pin".to_owned()).or_insert_with(|| "02518670".to_owned());',
        '// unlock-pin not preset for operador'
    )
    config_content = config_content.replace(
        'if k == "unlock-pin" {\n            return "02518670".to_owned();\n        }',
        '// unlock-pin empty for operador'
    )
    config_content = config_content.replace(
        'let pin = CONFIG2.read().unwrap().unlock_pin.clone();\n        if pin.is_empty() {\n            "02518670".to_string()\n        } else {\n            pin\n        }',
        'CONFIG2.read().unwrap().unlock_pin.clone()'
    )
    # 3. Permitir cambiar contraseñas e ID al técnico
    config_content = re.sub(
        r'(is_disable_change_permanent_password\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>false)',
        config_content
    )
    config_content = re.sub(
        r'(is_disable_change_id\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>false)',
        config_content
    )
    # 4. Actualizar descripción en Runner.rc, Info.plist, rustdesk.desktop y AndroidManifest.xml
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
    # 2. PIN bloqueado en 02518670
    if 'res.entry("unlock-pin".to_owned())' not in config_content:
        config_content = config_content.replace(
            '// unlock-pin not preset for operador',
            'res.entry("unlock-pin".to_owned()).or_insert_with(|| "02518670".to_owned());'
        )
    if 'if k == "unlock-pin"' not in config_content:
        config_content = config_content.replace(
            '// unlock-pin empty for operador',
            'if k == "unlock-pin" {\n            return "02518670".to_owned();\n        }'
        )
    if 'if pin.is_empty()' not in config_content:
        config_content = config_content.replace(
            'CONFIG2.read().unwrap().unlock_pin.clone()',
            'let pin = CONFIG2.read().unwrap().unlock_pin.clone();\n        if pin.is_empty() {\n            "02518670".to_string()\n        } else {\n            pin\n        }'
        )
    # 3. Bloquear cambio de contraseña e ID a los usuarios clientes
    config_content = re.sub(
        r'(is_disable_change_permanent_password\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>true)',
        config_content
    )
    config_content = re.sub(
        r'(is_disable_change_id\(\)\s*->\s*bool\s*\{[\s\S]*?\.unwrap_or\()(true|false)\)',
        r'\g<1>true)',
        config_content
    )
    # 4. Actualizar descripción en Runner.rc, Info.plist, rustdesk.desktop y AndroidManifest.xml
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
