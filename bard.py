# genai_module.py

import google.generativeai as genai

genai.configure(api_key="AIzaSyBtJUMWAn-a6xCCOBqUNe0PgymQtVdypHs")

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_LOW_AND_ABOVE"},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": "BLOCK_LOW_AND_ABOVE"},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
}


def generate_text(prompt):
    def extract_topic(prompt):
        topic = prompt.split(".")[0]
        return topic

    topic = extract_topic(prompt)

    combined_prompt = f"{topic}: {prompt}"

    response = genai.generate_text(
        **defaults,
        prompt=combined_prompt
    )

    return response.result


if __name__ == "__main__":
    user_prompt = input("Enter a prompt: ")
    result = generate_text(user_prompt)
    print(result)
