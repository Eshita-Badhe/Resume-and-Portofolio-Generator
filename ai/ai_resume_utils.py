import openai
from dotenv import load_dotenv
import os
openai.api_key = ''
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_resume_content(form_data):
    prompt = f"Generate a professional resume summary, experience bullet points, and role-based skills for: {form_data.get('name', 'a software developer')}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful resume assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    text = response['choices'][0]['message']['content']
    return {
        "summary": "Auto-generated summary...",
        "experience": "- Bullet 1\n- Bullet 2",
        "skills": "Python, Flask, SQL"
    }
