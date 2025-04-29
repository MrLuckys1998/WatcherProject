# WatchersProject

Sistema modular y extensible para ejecutar scripts de monitoreo ("watchers") de manera periódica y automatizada.

## 🧠 Descripción

Este proyecto permite definir múltiples scripts de "watchers", cada uno con su propia lógica de análisis o monitoreo, y ejecutarlos periódicamente sin intervención manual. Los watchers se generan desde plantillas, se configuran con archivos `.json`, y se ejecutan automáticamente mediante un orquestador multihilo.

## 🗂️ Estructura del proyecto

```
WatchersProject/
├── generated/                  # Watchers generados listos para ejecutarse
├── templates/                  # Plantillas (.j2) y ejemplos (.json) para generar watchers
├── logs/                       # Archivos de log de ejecución
├── systemd/                    # Servicios systemd para ejecutar watcher_orchestrator y watcher_web
├── generator_core.py          # Lógica para generar código desde plantillas
├── interactive_generator.py   # Interfaz para generación interactiva
├── watcher_orchestrator.py    # Orquestador que carga y ejecuta watchers periódicamente
├── watcher_web.py             # (opcional) Interfaz web para administración
├── logger.py                  # Módulo de logging centralizado
├── utils.py                   # Utilidades compartidas
└── generar_docs_pruebas.sh    # Script para generar documentación/pruebas
```

## 🚀 Cómo ejecutar

1. **Clonar el proyecto** y posicionarse en el directorio raíz.

2. **Instalar dependencias necesarias (si aplica):**
   ```bash
   pip install jinja2
   ```

3. **Generar un watcher desde plantilla:**
   ```bash
   python interactive_generator.py
   ```

4. **Ejecutar el orquestador:**
   ```bash
   python watcher_orchestrator.py
   ```

   Esto cargará y ejecutará automáticamente todos los scripts `.py` dentro de `generated/`.

## 🔄 Cómo funciona

- Cada watcher debe definir al menos una función `run()` y opcionalmente `interval_seconds`.
- El orquestador escanea el directorio `generated/` cada 5 segundos para detectar nuevos watchers.
- Cada watcher se ejecuta en su propio hilo.
- Los errores se registran en `logs/app.log`.

## 🧩 Agregar nuevos watchers

1. Crear un archivo de configuración `.example.json` dentro de `templates/`.
2. Crear una plantilla `.py.j2` correspondiente con lógica parametrizable.
3. Ejecutar el generador interactivo para crear el watcher.
4. El watcher aparecerá en `generated/` y será automáticamente detectado por el orquestador.

## 🛠️ Servicios systemd

Para ejecutar los watchers como servicios persistentes en sistemas Linux:

```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable Watcher-Orquestador.service
sudo systemctl start Watcher-Orquestador.service
```

## 📄 Logs

Los registros se almacenan en `logs/app.log`, incluyendo:
- Inicio y fin de cada watcher
- Errores o excepciones en tiempo de ejecución

## ✍️ Autor y Créditos

Proyecto desarrollado por el equipo de ELK Monitoring para facilitar la automatización de tareas de monitoreo basadas en plantillas dinámicas.

---
