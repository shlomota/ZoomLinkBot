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
        print(f"Sending image to GPT-4o-Mini: {image_url}")
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please extract the Zoom meeting ID, passcode and full join link from this image."},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
                response_format=ZoomInfo,
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            print(f"Error during GPT-4o-Mini completion: {str(e)}")
            raise

