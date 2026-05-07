import os
import asyncio
import base64
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted, PermissionDenied, GoogleAPIError
from typing import List, Any, Dict
from pydantic import BaseModel
import traceback

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)

app = FastAPI()

SYSTEM_INSTRUCTION = """You are GameChat, an expert AI gaming assistant. You help users with:
game recommendations, strategy, settings optimization, esports, mechanics,
hardware, troubleshooting, and game comparisons. Be helpful and direct.
Answer all gaming questions fully with appropriate context.
Add disclaimers only when giving hardware or competitive advice.
Refuse ONLY: requests for cheats/hacks/exploits, clearly harmful content,
and questions entirely unrelated to video games.
For off-topic asks, respond: I'm specialized in video games — feel free to ask about games, strategies, or setups.
"""

MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("code.html", "r", encoding="utf-8") as f:
        return f.read()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Build conversation history
    contents = []
    for msg in request.history:
        role = msg.get("role")
        parts = msg.get("parts")
        if role and parts:
            contents.append(
                types.Content(role=role, parts=[types.Part(text=p) for p in parts])
            )

    # Add current user message
    contents.append(
        types.Content(role="user", parts=[types.Part(text=request.message)])
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
        return {"reply": response.text}

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
            return {"reply": response.text}
        except ResourceExhausted:
            return {"reply": "I'm a bit busy right now — please try again in a moment."}
        except PermissionDenied as e:
            return {"reply": f"API error: {str(e)}"}
        except GoogleAPIError as e:
            return {"reply": f"API error: {str(e)}"}
        except Exception as e:
            traceback.print_exc()
            return {"reply": "Something went wrong — please retry."}

    except PermissionDenied as e:
        return {"reply": f"API error: {str(e)}"}
    except GoogleAPIError as e:
        return {"reply": f"API error: {str(e)}"}
    except Exception as e:
        traceback.print_exc()
        return {"reply": "Something went wrong — please retry."}


@app.post("/vision")
async def vision_endpoint(file: UploadFile = File(...), message: str = Form("")):
    prompt = message.strip() if message.strip() else "Analyze this gaming image and provide advice."

    try:
        contents = await file.read()
        image_data = base64.standard_b64encode(contents).decode("utf-8")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Content(parts=[
                    types.Part(text=prompt),
                    types.Part(inline_data=types.Blob(
                        mime_type=file.content_type,
                        data=image_data
                    ))
                ])
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=1000,
            )
        )
        return {"reply": response.text}

    except ResourceExhausted:
        await asyncio.sleep(2)
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Content(parts=[
                        types.Part(text=prompt),
                        types.Part(inline_data=types.Blob(
                            mime_type=file.content_type,
                            data=image_data
                        ))
                    ])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    max_output_tokens=1000,
                )
            )
            return {"reply": response.text}
        except ResourceExhausted:
            return {"reply": "I'm a bit busy right now — please try again in a moment."}
        except PermissionDenied as e:
            return {"reply": f"API error: {str(e)}"}
        except GoogleAPIError as e:
            return {"reply": f"API error: {str(e)}"}
        except Exception as e:
            traceback.print_exc()
            return {"reply": "Something went wrong — please retry."}

    except PermissionDenied as e:
        return {"reply": f"API error: {str(e)}"}
    except GoogleAPIError as e:
        return {"reply": f"API error: {str(e)}"}
    except Exception as e:
        traceback.print_exc()
        return {"reply": "Something went wrong — please retry."}
