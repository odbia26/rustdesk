#!/usr/bin/env python3
import sys
import re
import os

profile = sys.argv[1].lower().strip() if len(sys.argv) > 1 else "cliente"
print(f"[apply_profile] Applying build profile: '{profile}'")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
config_rs = os.path.join(base_dir, "libs", "hbb_common", "src", "config.rs")
runner_rc = os.path.join(base_dir, "flutter", "windows", "runner", "Runner.rc")

with open(config_rs, "r", encoding="utf-8") as f:
    config_content = f.read()

with open(runner_rc, "r", encoding="utf-8") as f:
    runner_content = f.read()

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
    # 4. Actualizar descripción en Runner.rc
    runner_content = runner_content.replace(
        'VALUE "FileDescription", "Boersis Remote Desktop" "\\0"',
        'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"'
    )
    runner_content = runner_content.replace(
        'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"',
        'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"'
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
    # 4. Actualizar descripción en Runner.rc
    runner_content = runner_content.replace(
        'VALUE "FileDescription", "Boersis Remote Desktop" "\\0"',
        'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"'
    )
    runner_content = runner_content.replace(
        'VALUE "FileDescription", "Boersis Remote Desktop - Operador" "\\0"',
        'VALUE "FileDescription", "Boersis Remote Desktop - Soporte" "\\0"'
    )

with open(config_rs, "w", encoding="utf-8") as f:
    f.write(config_content)

with open(runner_rc, "w", encoding="utf-8") as f:
    f.write(runner_content)

print(f"[apply_profile] Successfully configured profile '{profile}'.")
