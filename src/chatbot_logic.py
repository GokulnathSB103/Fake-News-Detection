def get_chatbot_response(user_input):
    user_input = user_input.lower()
    
    # 1. Criteria for AUDIO & LIVE VOICE
    if "audio" in user_input or "voice" in user_input or "live" in user_input:
        return ("### 🎙️ Audio & Live Voice Analysis Criteria:\n"
                "We analyze the **Spectral Density** of the sound. \n"
                "- **Human Criteria:** Look for 'Organic Jitter' and natural breathing pauses. Human vocal cords have slight imperfections.\n"
                "- **AI/Fake Criteria:** Synthetic voices often have 'Robotic Flatness'—the frequencies are too consistent and lack the emotional micro-variations found in real human speech.")

    # 2. Criteria for VIDEO
    elif "video" in user_input or "deepfake" in user_input:
        return ("### 🎥 Video Analysis Criteria:\n"
                "The system focuses on **Temporal Consistency** (frame-by-frame logic).\n"
                "- **Human Criteria:** Natural eye blinking (approx. every 2-10 seconds) and fluid skin-tone changes during movement.\n"
                "- **Fake Criteria:** We look for 'Boundary Blurring' around the chin and hair, and 'Lip-Sync Lag' where the mouth movement doesn't perfectly match the audio frequencies.")

    # 3. Criteria for IMAGES
    elif "image" in user_input or "photo" in user_input:
        return ("### 🖼️ Image Analysis Criteria:\n"
                "We scan for **Metadata and Pixel Artifacts**.\n"
                "- **Human Criteria:** Consistent lighting and shadow directions across all objects in the frame.\n"
                "- **Fake Criteria:** AI often leaves 'Digital Fingerprints' like warped background text, nonsensical shadows, or anatomical errors (like extra fingers or mismatched earrings).")

    # 4. Criteria for TEXT (News Content)
    elif "news" in user_input or "text" in user_input or "real or fake" in user_input:
        return ("### 📰 Text Content Analysis Criteria:\n"
                "We use a **TF-IDF + Logistic Regression** model.\n"
                "- **Real Criteria:** Balanced vocabulary, citations of specific sources, and objective tone.\n"
                "- **Fake Criteria:** High usage of 'Stop Words' (and, the, but) in unusual patterns, extreme emotional bias (anger/fear), and repetitive sensationalist phrases.")

    # Default Response
    else:
        return ("I can explain how we verify truth! Ask me about:\n"
                "- 'How do you analyze **live voices**?'\n"
                "- 'What are the criteria for **video**?'\n"
                "- 'How do you detect **fake images**?'")