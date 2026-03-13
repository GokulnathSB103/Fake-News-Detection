# Fake News Detection System

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your data to `data/news_data.csv`.
3. Train the model: `python src/train.py`
4. Run the web interface: `streamlit run src/app.py`

## Project Architecture


The system uses a **TF-IDF** approach for feature extraction and **Logistic Regression** for classification.