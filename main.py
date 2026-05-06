import os
import asyncio
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, PermissionDenied, GoogleAPIError
from typing import List, Optional, Any, Dict
from pydantic import BaseModel
import traceback

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=api_key)

app = FastAPI()

SYSTEM_INSTRUCTION = """You are GameChat, an expert AI gaming assistant. You help users with:
game recommendations, strategy, settings optimization, esports, mechanics,
hardware, troubleshooting, and game comparisons. Be helpful and direct.
Answer all gaming questions fully with appropriate context.
Add disclaimers only when giving hardware or competitive advice.
Refuse ONLY: requests for cheats/hacks/exploits, clearly harmful content,
and questions entirely unrelated to video games.
For off-topic asks, respond: "I'm specialized in video games — feel free to ask about games, strategies, or setups."
"""

model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=SYSTEM_INSTRUCTION)

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("c:/Games/stitch_gamebot_ai_chat_ui/code.html", "r", encoding="utf-8") as f:
        return f.read()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    formatted_history = []
    for msg in request.history:
        formatted_history.append({
            "role": msg.get("role"),
            "parts": msg.get("parts")
        })
    
    chat_session = model.start_chat(history=formatted_history)
    
    try:
        response = chat_session.send_message(request.message)
        return {"reply": response.text}
    except ResourceExhausted:
        await asyncio.sleep(2)
        try:
            response = chat_session.send_message(request.message)
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
    try:
        contents = await file.read()
        image_parts = [
            {
                "mime_type": file.content_type,
                "data": contents
            }
        ]
        
        vision_prompt = """You are GameChat, an expert AI gaming assistant.
Analyze this image and the user's message.
If the image is not related to video games (like food, selfie, etc.), respond EXACTLY with:
"This image doesn't appear to be related to video games. Try uploading a gameplay screenshot, settings page, or in-game setup."
Otherwise, answer the user's message helpfully and directly based on the gaming image.

User's message: """ + (message if message.strip() else "What's in this image?")
        
        try:
            response = model.generate_content([vision_prompt, image_parts[0]])
            return {"reply": response.text}
        except ResourceExhausted:
            await asyncio.sleep(2)
            try:
                response = model.generate_content([vision_prompt, image_parts[0]])
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
            
    except Exception as e:
        traceback.print_exc()
        return {"reply": "Something went wrong — please retry."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
