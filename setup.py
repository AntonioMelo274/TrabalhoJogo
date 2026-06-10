import cx_Freeze

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/icone.ico",
        target_name="JogoFantasma.exe"
    )
]

cx_Freeze.setup(
    name="Jogo Fantasma",
    options={
        "build_exe": {
            "packages": ["pygame", "pyttsx3", "comtypes", "win32api", "win32con"],
            "include_files": ["bases", "recursos"],
        }
    },
    executables=executaveis
)
