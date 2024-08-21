from cx_Freeze import setup, Executable
import sys
import os

build_exe_options = {
    "packages": ["os", "sqlite3", "datetime", "pandas", "PyQt5"],
    "include_files": [("database/database.sqlite", "database/database.sqlite"),
                      ("imagenes", "imagenes"),
                      ("app.manifest", "app.manifest"),]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="IntegradorNFX2",
    version="1.1",
    description="Integrador NFX2 con base de datos sqlite3",
    options={"build_exe": build_exe_options},
    executables=[Executable("integradorNFX1.py", base=base, icon="imagenes/iconoNFX1.ico")]
)






