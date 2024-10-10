import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictions, setPredictions] = useState(null);

  // Manejar el archivo seleccionado
  const onFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Subir el archivo y obtener predicciones
  const onFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/uploadfile/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setPredictions(response.data.predictions);
    } catch (error) {
      console.error("Error uploading the file:", error);
    }
  };

  // Descargar los resultados procesados
  const downloadResults = async () => {
    try {
      const response = await axios.post("http://localhost:8000/download-results/");
      const link = document.createElement("a");
      link.href = `http://localhost:8000/${response.data.file_url}`;
      link.download = "result.csv";
      link.click();
    } catch (error) {
      console.error("Error downloading the file:", error);
    }
  };

  return (
    <div className="App">
      <h1>Cargar archivo para predicciones</h1>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Subir Archivo y Obtener Predicciones</button>

      {predictions && (
        <div>
          <h2>Resultados de las predicciones:</h2>
          <pre>{JSON.stringify(predictions, null, 2)}</pre>
        </div>
      )}

      <button onClick={downloadResults}>Descargar Resultados</button>
    </div>
  );
}

export default App;


