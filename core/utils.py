import os
import requests
import logging

logger = logging.getLogger(__name__)

def translate_message(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates a chat message using the Gemini API.
    Returns the translated string or falls back to the original text on failure.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is missing.")
        return text

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }

    # The prompt explicitly sets the Persona and instructions
    system_prompt = (
        f"You are a professional translator. "
        f"Translate the following user message from {source_lang} to {target_lang}. "
        f"Maintain the tone and any slang used. Only return the translated text without extra conversational filler."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt + "\n\nMessage to translate: " + text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3 # Lower temperature for more accurate translation
        }
    }

    try:
        print(f"DEBUG: Sending to Gemini -> Text: '{text}', Source: '{source_lang}', Target: '{target_lang}'")
        # Include a timeout (e.g., 5-10 seconds) to prevent the request from hanging
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        
        print(f'Gemini Status: {response.status_code}')
        if response.status_code != 200:
            print(f'Gemini Error: {response.text}')

        response.raise_for_status() # Raise exception for 4xx or 5xx HTTP errors
        
        response_data = response.json()
        translated_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
        return translated_text

    except requests.exceptions.Timeout:
        logger.warning(f"Translation API timeout for text: {text[:20]}...")
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"Translation API request error: {str(e)}")
        return text
    except (KeyError, ValueError, IndexError) as e:
        logger.error(f"Translation API parse error: {str(e)}")
        return text
