# path: services/ai_service.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_health_remarks(glucose, haemoglobin, cholesterol):
    prompt = (
        f"A patient has the following blood test results: Glucose: {glucose} mg/dL, Haemoglobin: {haemoglobin} g/dL, Cholesterol: {cholesterol} mg/dL. "
        f"Within 2 sentences, summarize possible health risks based on these values. Be very concise and factual. Do not give a diagnosis."
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                #instruction layer
                "role": "system", #set model's personna and guardrails
                "content": "You are a medical assistant that summarizes blood test results clearly and factually. Never diagnose. Always recommend consulting a doctor."
            },
            {
                #data layer
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=200
    )
    return response.choices[0].message.content