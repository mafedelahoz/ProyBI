import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from Classes import ToDataFrame, ProcessText, Tokenization, Lemmatization, StopWordDeletion, SpecialCharacterFilter, FinalText, Predictions

# Modify this function to accept the file path as an argument
def create_pipeline(file_path_external):
    to_dataframe_transformer = ToDataFrame(file_path=file_path_external)

    loaded_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    loaded_model = joblib.load('model.pkl')

    # Create your pipeline as before, using the file path provided
    pipeline = Pipeline([
        ("crear_dataframe", to_dataframe_transformer),
        ("procesamiento_texto", ProcessText(column="Textos_espanol")),
        ("tokenizacion", Tokenization(column='procesado')),
        ("lematizacion", Lemmatization(column='procesado')),
        ("eliminar_stopwords", StopWordDeletion(column='procesado')),
        ("eliminacion_no_alfabetico", SpecialCharacterFilter(column='lemmas_sin_stopwords')),
        ("texto_final", FinalText(column='lemmas_limpios')),
        ("classifier", Predictions(model=loaded_model, vectorizer=loaded_vectorizer))
    ])

    return pipeline
