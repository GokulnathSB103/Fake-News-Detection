import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

def train_model():
    # 1. Load Data
    data_path = os.path.join('data', 'news_data.csv')
    if not os.path.exists(data_path):
        print("Error: data/news_data.csv not found!")
        return

    df = pd.read_csv(data_path)
    
    # 2. Split Data (Text and Label)
    X = df['text']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Create Pipeline: TF-IDF + Logistic Regression (UPDATED)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
        ('model', LogisticRegression())
    ])

    # 4. Train
    print("Training started...")
    pipeline.fit(X_train, y_train)
    
    # 5. Evaluate
    predictions = pipeline.predict(X_test)
    print(f"Model Training Complete. Accuracy: {accuracy_score(y_test, predictions):.2%}")

    # 6. Save Model
    os.makedirs('models', exist_ok=True)
    with open('models/fake_news_model.pkl', 'wb') as f:
        pickle.dump(pipeline, f)
    print("Model saved to models/fake_news_model.pkl")

if __name__ == "__main__":
    train_model()