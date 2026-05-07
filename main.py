import os
import asyncio
from typing import List, Any, Dict

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.api_core.exceptions import (
    ResourceExhausted,
    PermissionDenied,
    GoogleAPIError,
)
from pydantic import BaseModel
import traceback

# Load environment variables
load_dotenv()

# Get Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Create FastAPI app
app = FastAPI()

# System Prompt
SYSTEM_INSTRUCTION = """
You are GameChat, an expert AI gaming assistant.

You help users with:
- game recommendations
- strategy
- settings optimization
- esports
- mechanics
- hardware
- troubleshooting
- game comparisons

Be helpful and direct.

Answer all gaming questions fully with appropriate context.

Add disclaimers only when giving hardware or competitive advice.

Refuse ONLY:
- cheats
- hacks
- exploits
- harmful content
- questions entirely unrelated to video games

For off-topic questions, respond:
"I'm specialized in video games — feel free to ask about games, strategies, or setups."
"""

# Gemini Model
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"


# =========================
# HOME PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
async def get_index():
    try:
        with open("code.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>GameChat API Running ✅</h1>
        <p>code.html not found.</p>
        """


# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]] = []


# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    contents = []

    # Add history
    for msg in request.history:
        role = msg.get("role")
        parts = msg.get("parts")

        if role and parts:
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=str(p)) for p in parts]
                )
            )

    # Add current user message
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=1000,
            )
        )

        return {
            "reply": response.text
        }

    except ResourceExhausted:
        await asyncio.sleep(2)

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    max_output_tokens=1000,
                )
            )

            return {
                "reply": response.text
            }

        except ResourceExhausted:
            return {
                "reply": "I'm a bit busy right now — please try again in a moment."
            }

        except Exception as e:
            traceback.print_exc()

            return {
                "reply": f"Error: {str(e)}"
            }

    except PermissionDenied:
        return {
            "reply": "Permission denied. Check your Gemini API key."
        }

    except GoogleAPIError as e:
        return {
            "reply": f"Google API Error: {str(e)}"
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "reply": f"Unexpected error: {str(e)}"
        }


# =========================
# IMAGE / VISION ENDPOINT
# =========================
@app.post("/vision")
async def vision_endpoint(
    file: UploadFile = File(...),
    message: str = Form("")
):

    prompt = (
        message.strip()
        if message.strip()
        else "Analyze this gaming image and provide advice."
    )

    try:
        file_bytes = await file.read()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=prompt),
                        types.Part(
                            inline_data=types.Blob(
                                mime_type=file.content_type,
                                data=file_bytes
                            )
                        )
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=1000,
            )
        )

        return {
            "reply": response.text
        }

    except ResourceExhausted:
        await asyncio.sleep(2)

        return {
            "reply": "Server busy. Please try again shortly."
        }

    except PermissionDenied:
        return {
            "reply": "Permission denied. Check your Gemini API key."
        }

    except GoogleAPIError as e:
        return {
            "reply": f"Google API Error: {str(e)}"
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "reply": f"Unexpected error: {str(e)}"
        }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
async def health():
    return {"status": "ok"}


# =========================
# LOCAL RUN
# =========================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
