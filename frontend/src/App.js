import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [inputText, setInputText] = useState("");
  const [textPrediction, setTextPrediction] = useState(null);
  const [retrainMessage, setRetrainMessage] = useState("");
  const [serverResponse, setServerResponse] = useState(null);
  const [trainingFile, setTrainingFile] = useState(null); // Nuevo estado para el archivo de entrenamiento

  // Manejar el archivo seleccionado para predicciones
  const onFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Manejar el archivo seleccionado para reentrenamiento
  const onTrainingFileChange = (event) => {
    setTrainingFile(event.target.files[0]);
  };

  const onFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setPredictions(response.data.predictions);
      setServerResponse(response.data);
    } catch (error) {
      console.error("Error uploading the file:", error);
    }
  };

  // Clasificar texto
  const classifyText = async () => {
    try {
      const jsonData = [
        {
          "Textos_espanol": inputText,
          "sdg": 1
        }
      ];

      const response = await axios.post("http://localhost:8000/predict/", jsonData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setTextPrediction(response.data.prediction);
      setServerResponse(response.data);
    } catch (error) {
      console.error("Error classifying the text:", error);
    }
  };

  // Nueva función para reentrenar el modelo con un archivo de datos de entrenamiento
  const uploadTrainingFile = async () => {
    const formData = new FormData();
    formData.append("file", trainingFile);

    try {
      const response = await axios.post("http://localhost:8000/retrain-model/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setRetrainMessage(response.data.message);
      setServerResponse(response.data);
    } catch (error) {
      console.error("Error uploading the training file:", error);
    }
  };

  // Nueva función para enviar el JSON como archivo .json
  const enviarJsonComoArchivo = async () => {
    const jsonData = [
      {
        "Textos_espanol": inputText,
        "sdg": 1
      }
    ];

    try {
      const jsonString = JSON.stringify(jsonData);
      const blob = new Blob([jsonString], { type: 'application/json' });

      const formData = new FormData();
      formData.append("file", blob, "data.json");

      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setPredictions(response.data.predictions);
      setServerResponse(response.data);
    } catch (error) {
      console.error("Error al enviar el archivo .json:", error);
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

      <hr />

      <h1>Clasificación de Texto</h1>
      <input 
        type="text" 
        value={inputText} 
        onChange={(e) => setInputText(e.target.value)} 
        placeholder="Escribe un texto aquí" 
      />
      <button onClick={enviarJsonComoArchivo}>Clasificar texto</button>

      {textPrediction && (
        <div>
          <h2>Resultado de la clasificación:</h2>
          <p>{textPrediction}</p>
        </div>
      )}

      <hr />

      <h1>Reentrenar el Modelo</h1>
      <input type="file" onChange={onTrainingFileChange} />
      <button onClick={uploadTrainingFile}>Subir Archivo de Entrenamiento y Reentrenar</button>

      {retrainMessage && (
        <div>
          <h2>Mensaje del reentrenamiento:</h2>
          <p>{retrainMessage}</p>
        </div>
      )}

      <hr />

      {serverResponse && (
        <div>
          <h2>Respuesta del Servidor:</h2>
          {serverResponse.map((item, index) => (
            <div key={index} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
              <p><strong>Texto en Español:</strong> {item.Textos_espanol}</p>
              <p><strong>SDG:</strong> {item.sdg}</p>
              <p><strong>Probabilidad:</strong> {item.probabilidad.toFixed(2)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
