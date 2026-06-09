# pip install cx_freeze
import cx_Freeze

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/icone.ico",
        target_name="SpaceDefender.exe"
    )
]

cx_Freeze.setup(
    name="Space Defender",
    options={
        "build_exe": {
            "packages": ["pygame", "pyttsx3", "comtypes", "win32api", "win32con"],
            "include_files": ["bases", "recursos"],
        }
    },
    executables=executaveis
)

# python setup.py build
