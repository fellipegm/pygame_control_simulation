from cx_Freeze import setup, Executable

base = None    

executables = [Executable("cart.py", base=base)]

packages = ["idna", "pygame", "numpy", "helpers", "control"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Control cart V1.0 -- Fellipe Garcia Marques",
    options = options,
    version = "1.0",
    description = 'Control systems simulator with python',
    executables = executables
)