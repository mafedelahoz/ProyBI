import spacy
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix, accuracy_score, recall_score, precision_score, f1_score
from sklearn import tree
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import  OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import pandas as pd

import spacy

class ToDataFrame(BaseEstimator, TransformerMixin):
    def __init__(self, file_path=None, data_dict=None):
        """
        Initializes the class with an optional file path or data dictionary.
        """
        self.file_path = file_path  # Store the file path in the class instance
        self.data_dict = data_dict  # Store the data dictionary in the class instance

    def fit(self, X=None, y=None):
        """
        Fit method is not required to do anything here.
        """
        return self

    def transform(self, X=None, y=None):
        """
        Reads the file from the given file path or uses the provided data dictionary
        and transforms it into a DataFrame.
        """
        # If X is already a DataFrame, return it as is
        if isinstance(X, pd.DataFrame):
            return X

        # If data_dict is provided, create DataFrame from it
        if self.data_dict is not None:
            return pd.DataFrame([self.data_dict])  # Wrap the dict in a list

        # Check if file_path is set
        if not self.file_path:
            raise ValueError("No file path or data dictionary provided for ToDataFrame transformer.")
        
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
        X = self.vectorizer.transform(Z['texto_preprocesado']).toarray()
        predictions = self.model.predict(X)
        
        # Ensure to pass Z to predict_proba
        probabilidad = self.model.predict_proba(X).max(axis=1)

        
        # Create a copy of the DataFrame to avoid modifying the original one
        Z_copy = Z.copy()
        
        # Add predictions to the DataFrame
        Z_copy['sdg'] = predictions
        print("Predicciones añadidas")
        Z_copy['probabilidad'] = probabilidad
        Z_copy.drop(columns=['texto_preprocesado', 'procesado', 'tokens', 'lemmas', 'lemmas_sin_stopwords', 'lemmas_limpios'], inplace=True)
        
        return Z_copy

class Retrain(BaseEstimator, TransformerMixin):
    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    def fit(self, Z, y=None):
        # This transformer does not need to learn anything
        return self

    def retrain(self, Z):
        # Ensure predictions is a 1D array and matches the number of rows in X
        X = self.vectorizer.fit_transform(Z['texto_preprocesado']).toarray()
        Y = Z["sdg"]

        x_train, x_validation, y_train, y_validation = train_test_split(X, Y, test_size=0.3, random_state=10)
        self.model.fit(x_train, y_train)
        
        # analíticas del modelo
        y_pred = self.model.predict(x_validation)
        accuracy = accuracy_score(y_validation, y_pred)
        joblib.dump(self.model, 'model.pkl')
        
        return accuracy

