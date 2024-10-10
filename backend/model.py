import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import spacy
import joblib

import spacy

class ToDataFrame(BaseEstimator, TransformerMixin):
    def __init__(self, file_path=None):
        """
        Initializes the class with an optional file path.
        """
        self.file_path = file_path  # Store the file path in the class instance

    def fit(self, X=None, y=None):
        """
        Fit method is not required to do anything here.
        """
        return self

    def transform(self, X=None, y=None):
        """
        Reads the file from the given file path and transforms it into a DataFrame.
        If the file_path is already a DataFrame, return it directly.
        """
        # If X is already a DataFrame, return it as is
        if isinstance(self.file_path, pd.DataFrame):
            return self.file_path

        # Check if file_path is set
        if not self.file_path:
            raise ValueError("No file path provided for ToDataFrame transformer.")
        
        # Try reading the input data from the file path
        try:
            if self.file_path.endswith(".csv"):
                dataframe = pd.read_csv(self.file_path)
                print("Data read as CSV")
                return dataframe
            elif self.file_path.endswith(".xlsx"):
                dataframe = pd.read_excel(self.file_path)
                print("Data read as Excel")
                return dataframe
            elif self.file_path.endswith(".json"):
                dataframe = pd.read_json(self.file_path)
                print("Data read as JSON")
                return dataframe
            else:
                raise ValueError("Unsupported file format. Please provide a CSV, Excel, or JSON file.")
        except Exception as e:
            raise ValueError(f"Failed to read file: {e}")


class ProcessText(BaseEstimator, TransformerMixin):
    
    nlp = spacy.load("es_core_news_md")
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        if Z is None or not isinstance(Z, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        if self.column not in Z.columns:
            raise ValueError(f"Column '{self.column}' not found in DataFrame.")
        
        print("procesando")
        ZCopy = Z.copy()
        ZCopy['procesado'] = Z[self.column].apply(lambda x: self.nlp(x))
        return ZCopy

class Tokenization(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        print("tokenizando")
        Z['tokens'] = Z[self.column].apply(lambda doc: [token.text for token in doc])
        return Z

class Lemmatization(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        print("lematizando")
        Z['lemmas'] = Z[self.column].apply(lambda doc: [token.lemma_ for token in doc])
        return Z

class StopWordDeletion(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        print("stopwords")
        Z['lemmas_sin_stopwords'] = Z[self.column].apply(lambda doc: [token.lemma_ for token in doc if not token.is_stop])
        return Z

class SpecialCharacterFilter(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        print("lemmas limpios")
        Z['lemmas_limpios'] = Z[self.column].apply(lambda lemmas: [lemma for lemma in lemmas if lemma.isalpha()])
        return Z

class FinalText(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column
    
    def fit(self, Z, y=None):
        return self
    
    def transform(self, Z):
        print("texto final")
        Z['texto_preprocesado'] = Z[self.column].apply(lambda lemmas: ' '.join(lemmas))
        return Z


class Predictions(BaseEstimator, TransformerMixin):
    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    def fit(self, Z, y=None):
        # This transformer does not need to learn anything
        return self

    def predict(self, Z):
        # Ensure predictions is a 1D array and matches the number of rows in X
        X = self.vectorizer.fit_transform(Z['texto_preprocesado']).toarray()
        predictions = self.model.predict(X)
        
        # Ensure to pass Z to predict_proba
        probabilidad = self.model.predict_proba(X)
        
        # Create a copy of the DataFrame to avoid modifying the original one
        Z_copy = Z.copy()
        
        # Add predictions to the DataFrame
        Z_copy['sdg'] = predictions
        Z_copy.drop(columns=['texto_preprocesado', 'procesado', 'tokens', 'lemmas', 'lemmas_sin_stopwords', 'lemmas_limpios'], inplace=True)
        
        return Z_copy, probabilidad

# Cargar el modelo de lenguaje de SpaCy
nlp = spacy.load("es_core_news_md")

# Cargar el vectorizador y modelo de clasificación
count = joblib.load("../tfidf_vectorizer.pkl")  
best_NB = joblib.load("../pipeline_model.pkl")   

def cargar_datos(filepath):
    """Función para cargar los datos desde un archivo Excel"""
    data = pd.read_excel(filepath)
    return data

def preprocesar_datos(data):
    """Función para preprocesar los datos usando SpaCy"""
    data_copy = data.copy()
    
    # SpaCy procesamiento
    data_copy['procesado'] = data_copy['Textos_espanol'].apply(lambda x: nlp(x))
    
    # Eliminación de caracteres especiales y stopwords
    data_copy['lemmas_limpios'] = data_copy['procesado'].apply(lambda doc: [token.lemma_ for token in doc if not token.is_stop and token.is_alpha])
    
    # Texto preprocesado final
    data_copy['texto_preprocesado'] = data_copy['lemmas_limpios'].apply(lambda lemmas: ' '.join(lemmas))
    
    return data_copy

def predecir(data_copy):
    """Función para hacer la predicción usando el mejor modelo entrenado"""
    X_pred = count.transform(data_copy['texto_preprocesado'])
    y_pred = best_NB.predict(X_pred)
    data_copy['spg'] = y_pred
    return data_copy[['Textos_espanol', 'spg']]


