import requests
import json
import time # Added for exponential backoff sleep
# NOTE: You MUST replace 'home.models' with the correct path to your models file.
# If your app is named 'quiz_app', the path might be 'quiz_app.models'.
# If your models are in a sub-app named 'home', this path is likely correct.


# --- Configuration ---
# NOTE: Replace with your actual Gemini API key loaded from Django settings/environment variables.
# It is highly recommended to load this from Django settings (e.g., from django.conf import settings)
API_KEY = "" 
MODEL_NAME = "gemini-2.5-flash-preview-09-2025" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# Define the structured output schema for the LLM
QUESTION_SCHEMA = {
    "type": "ARRAY",
    "description": "An array of multiple-choice questions.",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question_text": {"type": "STRING", "description": "The text of the question."},
            "options": {
                "type": "OBJECT",
                "description": "The four options (A, B, C, D) for the question.",
                "properties": {
                    "A": {"type": "STRING"},
                    "B": {"type": "STRING"},
                    "C": {"type": "STRING"},
                    "D": {"type": "STRING"}
                }
            },
            "correct_option": {
                "type": "STRING",
                "description": "The letter (A, B, C, or D) corresponding to the correct answer.",
                "enum": ["A", "B", "C", "D"]
            }
        },
        "required": ["question_text", "options", "correct_option"]
    }
}

def generate_and_save_questions(category_id, topic_prompt, num_questions=5):
    from home.models import Category, Question, Option 
    """
    Generates structured quiz questions using the Gemini API and saves them to the database.

    :param category_id: The ID of the Category object to link questions to.
    :param topic_prompt: The user-provided prompt (e.g., "History of World War II").
    :param num_questions: The number of questions to generate.
    :return: A tuple (success_count, error_message)
    """
    
    # 1. Look up the Category object
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return (0, f"Error: Category with ID {category_id} not found.")
        
    # 2. Construct the System Instruction and User Query
    system_prompt = (
        f"You are a helpful quiz generator. Your task is to generate {num_questions} "
        f"high-quality multiple-choice questions (MCQs) on the topic: '{topic_prompt}'. "
        "Each question must have exactly four options (A, B, C, D) and specify the single correct option."
    )
    user_query = f"Generate {num_questions} unique, challenging multiple-choice questions about {topic_prompt}."

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": QUESTION_SCHEMA
        }
    }
    
    # 3. Make the API Call (with simple retry logic for stability)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            )
            response.raise_for_status()
            break  # Success
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                # Simple exponential backoff: 2^attempt seconds
                time.sleep(2 ** attempt) 
                continue
            return (0, f"API Error after {max_retries} retries: {e}")
        except Exception as e:
            return (0, f"An unexpected error occurred during the API call: {e}")

    # 4. Process the Response
    try:
        result = response.json()
        json_text = result['candidates'][0]['content']['parts'][0]['text']
        generated_questions = json.loads(json_text)
    except (KeyError, json.JSONDecodeError, IndexError) as e:
        # Handle cases where the response is not clean structured JSON
        return (0, f"Failed to parse model response structure. Raw error: {e}")

    # 5. Save Questions and Options to Django Database
    successful_saves = 0
    
    try:
        for q_data in generated_questions:
            # Create the Question object
            question = Question.objects.create(
                category=category,
                question_text=q_data['question_text']
            )
            
            # Create the Option objects
            for key, text in q_data['options'].items():
                Option.objects.create(
                    question=question,
                    option_text=text,
                    # Determine if this option is the correct one based on the model's response
                    is_correct=(key == q_data['correct_option'])
                )

            successful_saves += 1
            
    except Exception as e:
        # Catch any database saving errors
        return (successful_saves, f"Database saving failed after {successful_saves} questions: {e}")
        
    return (successful_saves, None)


# --- Example Usage (Remove for final Django integration) ---
if __name__ == '__main__':
    print("--- Running Test Generation (Requires a running Django environment to import models) ---")
    print("Please integrate this file into your Django app and use the outlined view function.")