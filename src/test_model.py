import pandas as pd
import pickle

with open('models/fake_news_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Test with one obvious fake and one obvious real
test_sentences = [
    "The president signed a law today regarding school funding.", # Real
    "Aliens landed in New York and are giving away free gold to everyone." # Fake
]

predictions = model.predict(test_sentences)
for text, pred in zip(test_sentences, predictions):
    print(f"Text: {text[:30]}... | Prediction: {'REAL' if pred == 1 else 'FAKE'}")