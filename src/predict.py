import pickle
import os

def predict_news():
    model_path = os.path.join('models', 'fake_news_model.pkl')
    
    if not os.path.exists(model_path):
        print("Error: Model not found. Please run train.py first.")
        return

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    text = input("\nEnter news text to check: ")
    prediction = model.predict([text])[0]
    
    result = "REAL" if prediction == 1 else "FAKE"
    print(f"Result: This news is {result}")

if __name__ == "__main__":
    predict_news()