# GameChat — Product Requirements Document

## Vision
GameChat is a topic-specialized AI chatbot that serves as an expert gaming companion. It answers questions about game recommendations, strategies, settings optimization, esports, hardware, troubleshooting, and game mechanics — all powered by Gemini. It accepts both text and images (e.g., gameplay screenshots, settings screens) and responds with practical, helpful guidance. The bot is friendly and knowledgeable, not overly cautious.

---

## Target User
- **Primary:** Mobile and PC gamers aged 14–30 in South/Southeast Asia, particularly BGMI, Free Fire, and Valorant players.
- **Secondary:** Casual gamers seeking hardware or settings advice.
- **Environment:** Mobile browser (primary), desktop browser (secondary). Low-bandwidth tolerance expected.

---

## Must-Have Features

### 1. Topic-Specialized Chat
- The bot answers only video game–related questions: recommendations, strategy, settings, mechanics, esports, hardware, troubleshooting, and game comparisons.
- Responses are helpful and direct. General gaming knowledge questions (e.g., "what is recoil control?") must be answered fully, not refused.
- Off-topic questions (food, medical, politics, etc.) receive a polite redirect: *"I'm specialized in video games — feel free to ask about games, strategies, or setups."*
- The bot refuses only: requests for cheats/exploits, harmful instructions, and genuinely off-topic asks.

### 2. Image Upload with Topic Verification
- Users can attach an image (gameplay screenshot, HUD layout, settings screen, error screen, etc.) via the paperclip icon.
- The backend sends the image to Gemini's vision endpoint and verifies relevance to gaming.
- If the image is unrelated to gaming (e.g., food photo, selfie), the bot responds: *"This image doesn't appear to be related to video games. Try uploading a gameplay screenshot, settings page, or in-game setup."*
- If relevant, the bot analyzes the image and provides contextual gaming advice.

### 3. Empty-Send Guard
- The Send button is disabled when the input field is empty or contains only whitespace.
- No empty API calls are ever made.

### 4. Markdown Rendering
- All bot responses are rendered as formatted HTML (bold, italics, lists, headers) using marked.js.
- Raw `**`, `*`, and `-` symbols must never appear in the chat UI.

### 5. Error Handling (User-Visible)
- **429 Rate Limit:** Retry once after 2 seconds. If still failing, show: *"I'm a bit busy right now — please try again in a moment."*
- **403 / PermissionDenied / GoogleAPIError:** Show the actual API error message in the chat to help developers debug (e.g., *"API key is invalid or has no permissions for this project."*).
- **Other errors:** Show: *"Something went wrong — please retry."*

### 6. Real Responses Only
- No demo messages, placeholder replies, hardcoded sample conversations, or fake history in the UI.
- The chat area is empty on load; the empty state (welcome screen + chips) is shown only before the first message.

---

## Non-Goals
- No user authentication or accounts.
- No persistent chat history across sessions.
- No support for non-gaming domains (sports scores, finance, health, etc.).
- No admin dashboard or moderation panel.
- No push notifications.
- No native mobile app (web only).

---

## Success Criteria
| Metric | Target |
|---|---|
| Time to first bot response | < 3 seconds on 4G |
| Empty-send attempts blocked | 100% |
| Off-topic image redirects correctly | ≥ 95% |
| Markdown renders without raw symbols | 100% |
| 429 retried before showing busy message | 100% |
| 403 shows actual API error (not generic) | 100% |
