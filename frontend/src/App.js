import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [inputText, setInputText] = useState("");
  const [textPrediction, setTextPrediction] = useState(null);
  const [retrainMessage, setRetrainMessage] = useState("");

  // Manejar el archivo seleccionado
  const onFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const onFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Cambia la URL a la que apunta la solicitud
      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setPredictions(response.data.predictions);
    } catch (error) {
      console.error("Error uploading the file:", error);
    }
};
  // Clasificar texto
  const classifyText = async () => {
    try {
      const response = await axios.post("http://localhost:8000/classify-text/", {
        text: inputText
      });
      setTextPrediction(response.data.prediction);
    } catch (error) {
      console.error("Error classifying the text:", error);
    }
  };

  // Reentrenar el modelo
  const retrainModel = async () => {
    try {
      const response = await axios.post("http://localhost:8000/retrain-model/");
      setRetrainMessage(response.data.message);
    } catch (error) {
      console.error("Error re-training the model:", error);
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
      <button onClick={classifyText}>Clasificar Texto</button>

      {textPrediction && (
        <div>
          <h2>Resultado de la clasificación:</h2>
          <p>{textPrediction}</p>
        </div>
      )}

      <hr />

      <h1>Reentrenar el Modelo</h1>
      <button onClick={retrainModel}>Reentrenar Modelo</button>

      {retrainMessage && (
        <div>
          <h2>Mensaje del reentrenamiento:</h2>
          <p>{retrainMessage}</p>
        </div>
      )}
    </div>
  );
}

export default App;
