import streamlit as st
import requests
import json
import re

# Set the page config
st.set_page_config(page_title="Freight Whisperer")

# App Title
st.title("🚢 Freight Whisperer")
st.subheader("Paste a broker message, get structured trade info + price signal")

# Gemini API Key
api_key = "AIzaSyBtvAp7zzsKXDwZKgzB4HyXii4qYTBJGXc"

# Text input area for broker quote
quote = st.text_area(
    "Paste Broker Quote", 
    height=200, 
    value="MV Blue Whale, Supramax 56k DWT, open CJK 25-27 May, 1st leg trip via NoPac to Singapore–Japan range, redelivery Japan, $16,250/d basis dop. Charterers: Bunge."
)

if st.button("Decode Quote") and api_key:
    prompt = f"""Extract the following fields from this broker message, try to be precise and careful:

- Deal Sentiment score (0 to 1 scale, where closer to 1 means very bullish, closer to 0 means very bearish)
- Vessel name
- Vessel type
- DWT (if missing, infer approximate from vessel type)
- Open port
- Laycan (date range if possible, else say 'Not specified')
- Route (origin to destination)
- Cargo (if any)
- Redelivery port
- Daily rate (USD)
- Charterer (if any)
- Market sentiment (bullish, neutral, bearish)
- Confidence level for each field (High, Medium, Low)

Avoid using generic placeholders like 'Prompt Supra' as vessel name.
If fields are missing, try to infer or explain why not extracted.

Message: {quote}

Return result as JSON with keys: deal_sentiment_score, vessel_name, vessel_type, dwt, open_port, laycan, route, cargo, redelivery_port, rate_usd_day, charterer, sentiment, and confidence_scores (dict).
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = { "Content-Type": "application/json" }
    data = {
        "contents": [
            {
                "parts": [
                    { "text": prompt }
                ]
            }
        ]
    }

    with st.spinner("💬 Sending request to Gemini.. \n Remember Deal Sentiment score (0 to 1 scale, where closer to 1 means very bullish, closer to 0 means very bearish)"):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.subheader("Extracted Output")

                # Clean up Markdown/code fences
                result_text_clean = result_text.strip()
                result_text_clean = re.sub(r"^```(?:json)?|```$", "", result_text_clean, flags=re.MULTILINE).strip()

                try:
                    parsed = json.loads(result_text_clean)
                    st.json(parsed)
                except json.JSONDecodeError:
                    st.error("⚠️ Model output is not valid JSON.")
                    st.text(result_text_clean)
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
