# SpeakUp English Tutor

An interactive English tutoring web application for Russian speakers progressing from B1 to C1 level, with a focus on spoken/conversational English.

## Architecture

**Single file: `index.html`**
- All CSS is embedded in `<style>` tags
- All JavaScript is embedded in `<script>` tags
- No build step, no npm install, no bundler
- Opens directly in any modern browser

## How to Run

```bash
# Option 1: Just open the file
open index.html

# Option 2: Serve locally (avoids CORS issues with translation API)
npx serve . -p 3000
# Then visit http://localhost:3000

# Option 3: Live reload during development
npx live-server --port=3000 --open=index.html
```

## Features

### Session Flow (6 phases)
1. **Topic Selection** — user picks from 3 demo topics
2. **Roleplay / Conversation** — 5–6 exchange scripted dialogue
3. **Mistake Correction** — common errors explained in Russian
4. **New Vocabulary** — 3 words/phrases with examples and translations
5. **C1 Challenge** — rephrase a simple sentence at C1 level
6. **Session Score** — score out of 10 with Russian feedback

### Translation System
- Every tutor message has an inline **RU** button
- Clicking the RU button fetches a Russian translation via **MyMemory API** (free, no API key)
- API endpoint: `https://api.mymemory.translated.net/get?q=TEXT&langpair=en|ru`
- Translations are cached in memory to avoid redundant requests
- "Translate all automatically" toggle at the top applies translations to new messages as they arrive
- Vocabulary panel words each have their own Russian translation toggle

### Demo Topics (pre-scripted flows)
| Topic | Level | Scenario |
|-------|-------|----------|
| Job Interview | B2–C1 | Marketing Manager application at international company |
| Travel & Airport | B1–B2 | Heathrow arrival, lost luggage, taxi, hotel check-in |
| Restaurant & Food | B1–B2 | Upscale restaurant, dietary needs, complaint, bill query |

### Vocabulary Panel
- Right sidebar (desktop) auto-populates with words learned each session
- Each card shows: word, part of speech, IPA transcription, example sentence, Russian translation toggle
- "Export" button downloads a `.txt` file of all session words

### Learner Support (B1-friendly)
- Every roleplay question has a **Russian hint** under the input field
- **💬 Пример ответа** button under each tutor question reveals a model answer
- **Sentence starters** (quick-reply chips) fill the input field for the student to complete — they do not auto-send
- Russian onboarding message on the welcome screen explains the lesson structure

### Session Persistence
- Full chat history, vocabulary, stats, and lesson position are saved to `localStorage` (key `speakup_session_v2`) on every message
- Reloading the page restores the session and **resumes** interrupted auto-phases (corrections/vocab/challenge/score) via `resumeFlow()`
- "Заново" button clears saved history and starts fresh

## Code Structure

```
index.html
├── <style>             CSS variables, layout, component styles, animations
├── <body>              HTML structure
│   ├── header          Branding + controls
│   ├── phase-bar       Session progress indicator (6 steps)
│   ├── translate-bar   Auto-translate toggle
│   ├── #messages       Chat message area
│   ├── #input-area     Textarea + Send button + quick replies
│   └── #vocab-panel    Right sidebar vocabulary tracker
└── <script>
    ├── freshState()    Factory for default session state
    ├── state{}         Session state object (incl. resume markers)
    ├── saveHistory()/loadHistory()  localStorage persistence
    ├── resumeFlow()    Continues an interrupted lesson after reload
    ├── TOPICS[]        Topic metadata
    ├── DEMO_SCRIPTS{}  Full scripted flows for 3 topics
    ├── translateText() MyMemory API call with caching
    ├── msgButtons()    Translate + model-answer buttons under tutor messages
    ├── startSession()  Entry point — welcome + RU onboarding + topic cards
    ├── selectTopic()   Begins roleplay phase
    ├── sendMessage()   Dispatches user input
    ├── handleRoleplay()    Advances scripted dialogue
    ├── triggerCorrections() Phase 3 — shows errors (resumable)
    ├── triggerVocab()       Phase 4 — shows new words (resumable)
    ├── triggerChallenge()   Phase 5 — C1 rephrase task
    ├── triggerScore()       Phase 6 — score + improvement focus
    └── resetSession()  Full reset to welcome state
```

## Design Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--navy` | `#0d1b2a` | Page background |
| `--navy-mid` | `#1a2e44` | Header, panels |
| `--navy-light` | `#243b55` | Cards, inputs |
| `--gold` | `#f0b429` | Primary accent, borders |
| `--gold-light` | `#ffd166` | Highlighted text |
| `--text` | `#e8eaf0` | Body text |
| `--text-dim` | `#94a3b8` | Secondary text |

## Extending the App

### Adding a New Topic
1. Add an entry to the `TOPICS` array with `id`, `icon`, `title`, `desc`, `level`
2. Add a matching key to `DEMO_SCRIPTS` with:
   - `intro` — opening tutor message (supports `**bold**` and `*italic*`)
   - `intro_hint_ru` / `intro_starters[]` / `intro_example` — Russian hint, sentence starters, and model answer for the intro question
   - `turns[]` — array of `{ tutor, hint_ru, starters[], example }` objects (5 turns)
   - `corrections[]` — array of `{ original, fixed, ru_note }` (2–4 errors)
   - `vocab[]` — array of `{ word, pos, ipa, example, ru }` (exactly 3)
   - `challenge` — `{ prompt, example_answer }`
   - `score` — `{ value (1–10), feedback (Russian), improve (Russian — focus for next lesson) }`

### Connecting a Real AI Backend
Replace `handleRoleplay()` with a `fetch()` call to your API endpoint.
The conversation state (`state.userTurns`, `state.topic`) provides context.
All rendering helpers (`appendMessage`, `addVocabWord`, etc.) remain unchanged.

### Translation API Notes
- MyMemory free tier: ~1000 requests/day per IP
- For production use, register at https://mymemory.translated.net to get higher limits
- Swap the `translateText()` function body to use DeepL, Google Translate, or any other API

## Browser Compatibility
Works in all modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+).
No polyfills required. Uses: CSS Grid/Flexbox, CSS Custom Properties, async/await, Fetch API.
