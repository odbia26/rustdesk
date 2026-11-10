#!/usr/bin/env python3
import sys
import re
import os

min_ver = sys.argv[1].strip() if len(sys.argv) > 1 else "12.3"
print(f"[set_macos_deployment_target] Setting macOS deployment target to '{min_ver}' across all project files...")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 1. build.py
build_py = os.path.join(base_dir, "build.py")
if os.path.exists(build_py):
    with open(build_py, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r'MACOSX_DEPLOYMENT_TARGET\s*=\s*[0-9]+(?:\.[0-9]+)*', f'MACOSX_DEPLOYMENT_TARGET={min_ver}', c)
    with open(build_py, "w", encoding="utf-8") as f:
        f.write(c)
    print("  -> Updated build.py")

# 2. flutter/macos/Podfile
podfile = os.path.join(base_dir, "flutter", "macos", "Podfile")
if os.path.exists(podfile):
    with open(podfile, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r"platform\s*:osx,\s*'[^']*'", f"platform :osx, '{min_ver}'", c)
    with open(podfile, "w", encoding="utf-8") as f:
        f.write(c)
    print("  -> Updated flutter/macos/Podfile")

# 3. Cargo.toml
cargo_toml = os.path.join(base_dir, "Cargo.toml")
if os.path.exists(cargo_toml):
    with open(cargo_toml, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r'osx_minimum_system_version\s*=\s*"[^"]*"', f'osx_minimum_system_version = "{min_ver}"', c)
    with open(cargo_toml, "w", encoding="utf-8") as f:
        f.write(c)
    print("  -> Updated Cargo.toml")

# 4. flutter/macos/Runner.xcodeproj/project.pbxproj
pbxproj = os.path.join(base_dir, "flutter", "macos", "Runner.xcodeproj", "project.pbxproj")
if os.path.exists(pbxproj):
    with open(pbxproj, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r'MACOSX_DEPLOYMENT_TARGET\s*=\s*[0-9]+(?:\.[0-9]+)*;', f'MACOSX_DEPLOYMENT_TARGET = {min_ver};', c)
    with open(pbxproj, "w", encoding="utf-8") as f:
        f.write(c)
    print("  -> Updated flutter/macos/Runner.xcodeproj/project.pbxproj")

print("[set_macos_deployment_target] Done.")
