from dotenv import load_dotenv
import google.generativeai as genai

from .models import Biomarker
import os
import json
load_dotenv()

API = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=API)

config = genai.GenerationConfig(
    response_mime_type="application/json",
    response_schema={
  "type": "object",
  "properties": {
    "response": {
      "type": "object",
      "properties": {
        "diseases": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "description": {
                "type": "string"
              },
              "next_steps": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "preventive_steps": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "long_term_complications": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            },
            "required": [
              "name",
              "description",
              "next_steps",
              "preventive_steps",
              "long_term_complications"
            ]
          }
        }
      },
      "required": [
        "diseases"
      ]
    }
  },
  "required": [
    "response"
  ]
}
)


model = genai.GenerativeModel("gemini-1.5-flash", generation_config=config)
chat_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_response(data):
    PROMPT = "You are women health counsellor You will be given some symptoms faced by the user. Your job is to tell what could be the possible disease which cause these symptoms, preventive measures, what are the next steps a person should take when diagnosed with the disease and long term disease complications. SYMPTOMS : "

    r = model.generate_content(PROMPT + data)
    data = json.loads(r._result.candidates.pb[0].content.parts[0].text)
    return data['response']['diseases']

    
def chat_with_gemini(input, history):
    chat_session = chat_model.start_chat(history=history)
    response = chat_session.send_message(input)
    data = response._result.candidates.pb[0].content.parts[0].text
    return data


