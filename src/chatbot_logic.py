def get_chatbot_response(user_input):
    """
    Core logic for the Truth-Seeker AI Chatbot.
    Matches user keywords to educational explanations about the project.
    """
    user_input = user_input.lower()
    
    # 1. Detection Methodology
    if "how" in user_input and "detect" in user_input:
        return ("Our system uses **TF-IDF (Term Frequency-Inverse Document Frequency)**. "
                "It calculates how unique or sensationalist certain words are. Fake news often "
                "uses 'clickbait' language that our Logistic Regression model is trained to flag.")
    
    # 2. Deepfake / Audio Analysis
    elif "deepfake" in user_input or "voice" in user_input or "audio" in user_input:
        return ("To detect audio deepfakes, we look at the **Vocal Spectrogram**. "
                "Human voices have 'Organic Jitter' (tiny variations in pitch). AI-generated "
                "voices are mathematically perfect, which actually makes them look 'robotic' "
                "under frequency analysis.")

    # 3. Image Analysis
    elif "image" in user_input or "photo" in user_input:
        return ("Our image scanner looks for **Artifacts**. AI generators often struggle with "
                "pixel consistency in complex areas like eyes, fingers, and background text "
                "symmetry. We scan for these 'digital fingerprints'.")

    # 4. General Help
    else:
        return ("I am your project assistant. You can ask me:\n"
                "- 'How does the text detection work?'\n"
                "- 'How can you tell if a voice is AI?'\n"
                "- 'What do you look for in fake images?'")