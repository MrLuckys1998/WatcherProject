# Importación de módulos necesarios
import os
# Importación de módulos necesarios
import time
# Importación de módulos necesarios
import threading
# Importación de módulos necesarios
import importlib.util
# Importación de módulos necesarios
import traceback
# Importación de módulos necesarios
from logger import logger  # Importación del logger central

WATCHER_DIR = "generated"
CHECK_INTERVAL = 5  # cada 5 segundos escanea por nuevos watchers

executing_watchers = {}

# Definición de una función: run_periodically
def run_periodically(path, interval, module_name):
# Definición de una función: task
    def task():
        while True:
            try:
                logger.info(f"[RUNNING] {module_name}")
                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.run()
            except Exception as e:
                logger.error(f"[ERROR] {module_name}: {e}\n{traceback.format_exc()}")
            time.sleep(interval)
    return threading.Thread(target=task, daemon=True)

# Definición de una función: load_watcher
def load_watcher(path):
    filename = os.path.basename(path)
    module_name = os.path.splitext(filename)[0]

    if module_name in executing_watchers:
        return

    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        interval = getattr(module, "interval_seconds", 300)
        t = run_periodically(path, interval, module_name)
        t.start()
        executing_watchers[module_name] = t
        logger.info(f"[STARTED] {filename} cada {interval}s")
    except Exception as e:
        logger.error(f"[FAILED] {filename} no se pudo iniciar: {e}")

# Definición de una función: main
def main():
    os.makedirs(WATCHER_DIR, exist_ok=True)
    logger.info("=== Orquestador iniciado ===")

    while True:
        for file in os.listdir(WATCHER_DIR):
            if file.endswith(".py"):
                path = os.path.join(WATCHER_DIR, file)
                load_watcher(path)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()