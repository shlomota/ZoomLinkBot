# llm.py
from openai import OpenAI
from pydantic import BaseModel
import os

# Define a structured output model for Zoom information
class ZoomInfo(BaseModel):
    meeting_id: str
    passcode: str
    join_url: str

class ChatGPT:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def extract_zoom_info(self, image_url):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please extract the Zoom meeting ID and passcode from this image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return completion.choices[0]['message']['content']

    def parse_zoom_info(self, zoom_info_text):
        try:
            return ZoomInfo.parse_raw(zoom_info_text)
        except Exception as e:
            raise ValueError(f"Error parsing Zoom info: {str(e)}")
