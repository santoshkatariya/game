# GameChat — Build Tasks

---

**Task 1 — Create project structure and dependencies**
Create the `gamechat/` folder. Inside it, create `requirements.txt` with: `fastapi`, `uvicorn[standard]`, `google-generativeai`, `python-dotenv`, `python-multipart`. Copy `code.html` into this folder.

**Task 2 — Set up `.env` and key loading**
Create a `.env` file in the project root with `GEMINI_API_KEY=` (blank, for the student to fill). In `main.py`, use `python-dotenv` to load it at startup and configure the `google.generativeai` SDK with the key. Raise a clear startup error if the key is missing.

**Task 3 — Create FastAPI app skeleton and serve `code.html`**
Initialize the FastAPI app in `main.py`. Add a `GET /` route that reads and returns `code.html` as an `HTMLResponse`. Run via `uvicorn main:app --port 8000 --reload`. Verify the UI loads in the browser before proceeding.

**Task 4 — Define the system instruction constant**
At the top of `main.py`, define `SYSTEM_INSTRUCTION` as a multi-line string. It must instruct the bot to: answer all video game questions helpfully and directly, add disclaimers only for hardware/competitive advice, and refuse ONLY cheats/exploits, harmful content, and fully off-topic questions. Include the exact off-topic redirect message from the PRD.

**Task 5 — Build the `/chat` POST endpoint**
Create a Pydantic model `ChatRequest` with fields `message: str` and `history: list`. In the endpoint, validate that `message.strip()` is non-empty (return 400 if not). Call `gemini-2.5-flash-lite` with the system instruction and conversation history. Return `{ "reply": response_text }`.

**Task 6 — Add error handling to `/chat` — 429, 403, and generic**
Wrap the Gemini call in try/except. For HTTP 429: sleep 2 seconds and retry once; if still failing, return `{ "reply": "I'm a bit busy right now — please try again in a moment." }`. For 403 / `PermissionDenied` / any `GoogleAPIError`: return `{ "reply": f"API error: {str(e)}" }` — do NOT use the generic busy message. For all other exceptions: log the traceback and return `{ "reply": "Something went wrong — please retry." }`.

**Task 7 — Build the `/vision` POST endpoint**
Accept `multipart/form-data` with a required `file` (image) and optional `message` (text, default empty). Read the image bytes and pass them to Gemini as `inline_data` alongside the text prompt. Include image relevance checking in the prompt: if the image is not gaming-related, the model should respond with the exact redirect message from the PRD. Apply the same error handling as Task 6.

**Task 8 — Remove all demo/placeholder content from `code.html`**
Delete the commented-out demo chat bubble block (`<!-- Hidden Chat Bubbles for reference -->`) from `code.html`. Ensure the chat message list area is completely empty on page load — no hardcoded messages, no sample replies, no fake history.

**Task 9 — Add `marked.js` and wire bot bubble rendering**
Add `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` to `code.html`'s `<head>`. In the JS that appends bot messages to the chat, set the bubble's `innerHTML` to `marked.parse(reply)` instead of `textContent`. Add scoped CSS inside the chat bubble to style `strong`, `em`, `ul`, `ol`, `li`, `p` so they inherit the design system's colors and spacing.

**Task 10 — Implement the empty-send guard**
On page load, set the send button's `disabled` attribute and apply the existing `cursor-not-allowed` + `text-surface-variant` Tailwind classes. Add an `input` event listener on the text field: enable the button (remove disabled, swap to active color classes) when `inputEl.value.trim() !== ''`, disable it otherwise. The guard must also prevent form submission via `Enter` key when the field is empty.

**Task 11 — Wire chip buttons to the chat input**
Add `click` event listeners to each of the four example chip buttons. On click: populate the text input with the chip's label text, dispatch an `input` event (to trigger the empty-send guard and enable the send button), and programmatically click the send button to fire the API call immediately.

**Task 12 — Add image upload UI and wire to `/vision`**
Add a hidden `<input type="file" accept="image/*">` to `code.html`. Make the paperclip button trigger it on click. On file selection, show a small thumbnail preview above the input bar. Store the selected file. When send is clicked and a file is pending: POST to `/vision` using `FormData` (append file + message text). Clear the preview after sending.

**Task 13 — Add typing indicator and hide empty state after first send**
When the user sends a message, immediately: (a) hide the empty-state welcome section, (b) append the user's message as a right-aligned bubble, (c) append a typing-indicator bubble (three animated dots using CSS keyframes). When the API responds, replace the typing indicator with the rendered bot reply bubble. Never show the welcome/chips section again once the first message is sent.

**Task 14 — End-to-end test and polish**
Test all flows: normal chat, image upload (gaming image), image upload (non-gaming image), empty-send blocked, chip click → auto-send, 429 retry (mock or real), 403 with bad key shows actual error. Confirm Markdown renders (bold, lists, italics) with no raw symbols. Confirm the send button state toggles correctly on type/clear.
