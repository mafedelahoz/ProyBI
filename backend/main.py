from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from model import cargar_datos, preprocesar_datos, predecir

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Guardar el archivo en el servidor
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Procesar el archivo cargado
    try:
        # Cargar los datos
        data = cargar_datos(file_location)

        # Preprocesar los datos
        data_preprocesado = preprocesar_datos(data)

        # Hacer la predicción
        data_final = predecir(data_preprocesado)

        # Guardar el resultado en un archivo Excel (opcional)
        result_file_location = f"{UPLOAD_DIR}/df_predicciones_{file.filename}"
        data_final.to_excel(result_file_location, index=False)

        # Convertir a JSON y retornar al usuario
        return JSONResponse(content={"predictions": data_final.to_dict(orient='records')})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Ruta para descargar el archivo con los resultados (opcional)
@app.post("/download-results/")
async def download_results():
    result_path = f"{UPLOAD_DIR}/result.xlsx"  # Cambiar si es necesario
    return {"file_url": result_path}
