import importlib
import subprocess

required_libraries = [
    "speechrecognition",
    "pyttsx3",
    "webbrowser",
    "datetime",
    "os",
    "random",
    "config",
    "google.generativeai"
]
def check_and_install_libraries(required_libraries):
    missing_libraries = []
    for library in required_libraries:
        try:
            importlib.import_module(library)
        except ImportError:
            missing_libraries.append(library)

    if missing_libraries:
        print(f"The following libraries are required but not installed: {', '.join(missing_libraries)}")
        try:
            subprocess.run(["pip", "install"] + missing_libraries, check=True)
            print("Successfully installed missing libraries.")
            return True
        except subprocess.CalledProcessError:
            print("Error installing libraries using pip. Please install them manually.")
            return False
    else:
        return True

check_and_install_libraries(required_libraries)