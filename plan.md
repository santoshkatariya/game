# GameChat — Implementation Plan

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.11+) |
| AI Model | `gemini-2.5-flash-lite` via `google-generativeai` Python SDK |
| Frontend | Vanilla JS + the provided `code.html` (do NOT redesign) |
| Markdown rendering | `marked.js` via CDN (injected into `code.html`) |
| Config | `.env` file → loaded via `python-dotenv` |
| Server | Uvicorn, port 8000 |

---

## Free Tier Limits (gemini-2.5-flash-lite)
- 15 RPM (requests per minute)
- 1,000 RPD (requests per day)
- 1M token context window
- Multimodal (text + image) supported

---

## Project Structure

```
gamechat/
├── main.py              # FastAPI app, /chat and /vision endpoints
├── .env                 # GEMINI_API_KEY=your_key_here
├── requirements.txt     # Dependencies
└── code.html            # UI (served at / by FastAPI)
```

---

## Components — Build Order

### 1. Environment & Dependencies
- `requirements.txt`: `fastapi`, `uvicorn`, `google-generativeai`, `python-dotenv`, `python-multipart`
- `.env` file with `GEMINI_API_KEY=`
- Load key in `main.py` via `dotenv`

### 2. FastAPI App Skeleton (`main.py`)
- Initialize FastAPI app
- Load `GEMINI_API_KEY` from environment via `python-dotenv`
- Configure `google.generativeai` with the key
- Mount static file serving: `GET /` returns `code.html`

### 3. System Instruction
Define the system prompt as a module-level constant:
```
You are GameChat, an expert AI gaming assistant. You help users with:
game recommendations, strategy, settings optimization, esports, mechanics,
hardware, troubleshooting, and game comparisons. Be helpful and direct.
Answer all gaming questions fully with appropriate context.
Add disclaimers only when giving hardware or competitive advice.
Refuse ONLY: requests for cheats/hacks/exploits, clearly harmful content,
and questions entirely unrelated to video games.
For off-topic asks, respond: "I'm specialized in video games — feel free
to ask about games, strategies, or setups."
```

### 4. `/chat` POST Endpoint
- Accepts JSON: `{ "message": "string", "history": [...] }`
- Validates that `message` is non-empty (400 if empty)
- Calls `gemini-2.5-flash-lite` with system instruction + conversation history
- Returns JSON: `{ "reply": "string" }`
- Error handling:
  - 429 → retry once after 2s → return busy message or actual reply
  - 403 / `PermissionDenied` / `GoogleAPIError` → return actual error string
  - Other → log + return generic error

### 5. `/vision` POST Endpoint
- Accepts multipart form: `file` (image) + optional `message` (text)
- Reads image bytes, encodes as base64, passes to Gemini with `inline_data`
- System instruction includes image relevance check
- Returns JSON: `{ "reply": "string" }`
- Same error handling as `/chat`

### 6. Frontend Wiring (`code.html` modifications)
The HTML is used **as-is** visually. The following JS is added/modified:

#### a. marked.js CDN
```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
```
All bot bubble content is rendered via `marked.parse(reply)`.

#### b. Empty-send guard
```js
inputEl.addEventListener('input', () => {
  sendBtn.disabled = inputEl.value.trim() === '';
});
```
Send button starts disabled. Enabled only when input has non-whitespace content.

#### c. Chat state management
- `conversationHistory` array tracks `{ role, parts }` for multi-turn context
- Empty state (welcome + chips) hidden after first message sent
- Chat bubbles appended dynamically with user bubble immediately, bot bubble after API resolves

#### d. Chip click handlers
Each example chip populates the input field and triggers send.

#### e. Image upload handler
- Paperclip button triggers `<input type="file" accept="image/*">` (hidden)
- On file select: shows preview thumbnail above input, stores file reference
- On send: POST to `/vision` with `FormData` instead of `/chat`

#### f. Loading state
- While awaiting API: show a typing indicator bubble (3-dot animation)
- Remove it when the reply arrives

---

## API Contract

### POST /chat
```json
Request:  { "message": "Best games for PC?", "history": [] }
Response: { "reply": "Here are some great PC games..." }
```

### POST /vision
```
Request:  multipart/form-data
          file: <image binary>
          message: "What sensitivity should I use?" (optional)
Response: { "reply": "Based on your settings screen..." }
```

---

## Error Response Format
All errors return:
```json
{ "reply": "<user-friendly error string>" }
```
This means the frontend never needs special error-state handling — errors appear as bot messages.
