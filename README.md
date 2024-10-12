
# Proyecto: Despliegue de la API y Frontend

Este documento contiene las instrucciones para desplegar la API usando FastAPI y el frontend en React. Se detallan los pasos para configurar un entorno virtual para la API, instalar las dependencias necesarias, y ejecutar tanto el backend como el frontend.

## 1. Despliegue de la API (Backend)

### Requisitos previos

- Python 3.x instalado en tu sistema.
- `pip` instalado para gestionar las dependencias de Python.

### Pasos para configurar y ejecutar la API

1. **Clonar el repositorio** (si no lo has hecho ya):
   ```bash
   git clone <url-del-repositorio>
   cd <directorio-del-proyecto>
   ```

2. **Crear un entorno virtual (venv)**:

   En el directorio raíz del proyecto, ejecuta:

   ```bash
   python -m venv venv
   ```

   Esto creará un entorno virtual llamado `venv`.

3. **Activar el entorno virtual**:

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```

   - En macOS y Linux:
     ```bash
     source venv/bin/activate
     ```

   Una vez activado, verás el nombre del entorno virtual en tu terminal.

4. **Instalar las dependencias**:

   Asegúrate de que el archivo `requirements.txt` está en la raíz del proyecto. Luego, ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todas las dependencias necesarias para ejecutar la API.

5. **Ejecutar la API con Uvicorn**:

   Para ejecutar la API con recarga automática (`--reload`) y asegurarte de que se toma el archivo `app.py` como el módulo principal, usa:

   ```bash
   uvicorn app:app --reload
   ```

   - `app:app` se refiere al módulo `app.py` (el primer `app`) y a la instancia de la aplicación FastAPI (el segundo `app`).
   - La opción `--reload` permite que la API se recargue automáticamente cada vez que detecta cambios en el código.

6. **Acceder a la API**:

   Por defecto, la API estará disponible en `http://127.0.0.1:8000`. Puedes verificar que está funcionando accediendo a `http://127.0.0.1:8000/docs` para ver la documentación interactiva generada por Swagger.

---

## 2. Despliegue del Frontend (React)

### Requisitos previos

- Node.js y npm instalados en tu sistema. Puedes verificar la instalación ejecutando:
   ```bash
   node -v
   npm -v
   ```

### Pasos para configurar y ejecutar el frontend

1. **Navegar a la carpeta del frontend**:

   Asegúrate de estar en la raíz del proyecto y navega a la carpeta del frontend:

   ```bash
   cd frontend
   ```

2. **Instalar las dependencias**:

   Ejecuta el siguiente comando para instalar todas las dependencias necesarias para el proyecto React:

   ```bash
   npm install
   ```

3. **Ejecutar el frontend**:

   Una vez instaladas las dependencias, inicia el servidor de desarrollo de React con el siguiente comando:

   ```bash
   npm start
   ```

   Esto abrirá automáticamente el navegador y cargará el frontend en `http://localhost:3000`.

### Notas adicionales

- Asegúrate de que la API (backend) esté ejecutándose en `http://localhost:8000` para que el frontend pueda comunicarse correctamente con ella.
- Si estás trabajando en un entorno donde el backend y el frontend están en dominios o puertos diferentes, asegúrate de que la API tenga configurado el CORS correctamente para permitir las solicitudes desde el frontend.

---

## 3. Consideraciones finales

- Recuerda desactivar el entorno virtual cuando hayas terminado con el desarrollo del backend ejecutando:
  - En Windows: `venv\Scripts\deactivate`
  - En macOS y Linux: `deactivate`

- Si encuentras algún problema durante el despliegue o la ejecución, revisa que todas las dependencias se hayan instalado correctamente y que no haya errores en la configuración de los archivos de la API o del frontend.

¡Gracias por usar nuestro proyecto! Para cualquier consulta o problema, por favor, contacta al equipo de desarrollo.
