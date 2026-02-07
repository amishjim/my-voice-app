# My Voice: The AI Voice Harvester

## Why This Exists

Most AI sounds like a corporate committee wrote it. It's full of fluff, "let's dive ins," and polite padding. If you've spent 30 years on a film set or running a sawmill, that bot-speak doesn't represent you. **My Voice** is a tool designed to scrape your actual human DNA from your digital history—Facebook, Instagram, and LinkedIn—and distill it into a single file that teaches an LLM how you actually talk.

## How It Works

This app acts as a **"Data Janitor."** You feed it your messy JSON data exports, and it runs a **"High-Pass Filter"** to strip away the system noise (links, shared memories, "Happy Birthday" posts). It looks for:

- **Original Prose**: Paragraphs where you actually had something to say.
- **Humanity Markers**: Your specific slang, industry shorthand, and punctuation habits.
- **Technical DNA**: Your professional history and veteran perspective.

### Filtering Logic

The app intelligently filters content to preserve only meaningful prose:
- Posts with **more than 20 words**, OR
- Posts with **more than 10 words** that contain "human markers" like contractions ("I'm", "don't"), ellipses ("..."), or personal pronouns ("my", "I've").

It recursively searches through any JSON structure for text in `post`, `comment`, or `message` fields, while automatically ignoring `media` and `album` folders.

## How to Use It

### 1. Export Your Data
Go to your Facebook, Instagram, or LinkedIn settings and request a download of your information in **JSON format**.

### 2. Start the App
```bash
pip install -r requirements.txt
python app.py
```

Then open your browser to `http://localhost:5000`.

### 3. Drop Your Files
Drag and drop **any Facebook JSON files** into the app's Drop Zone. The app accepts multiple files at once—no specific filenames required.

### 4. Harvest
Hit **"Process Files."** The app will append your cleaned dialogue into a single library called `My_Voice_Master.txt`.

### 5. Train Your AI
Upload that `.txt` file to Gemini, Claude, or NotebookLM and tell it:

> "This is my Voice Model. Write everything from this perspective—direct, honest, and no fluff."

## Features

- ✅ **Accept Any JSON Files**: No filename restrictions—process any Facebook export files.
- ✅ **Library Building**: Appends to `My_Voice_Master.txt` instead of overwriting, so you can build your voice library over time.
- ✅ **Smart Filtering**: Keeps only meaningful prose using word count and human marker detection.
- ✅ **Recursive Extraction**: Finds text nested deep in complex JSON structures.
- ✅ **Media Filtering**: Automatically ignores non-prose folders like `media` and `album`.
- ✅ **Lyrics Mode**: Optional double-spacing for song lyrics or poetry.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Dependencies**: Flask (see `requirements.txt`)

## For the Filmmakers

This tool was built by a veteran with 30 years in the entertainment industry. It's designed to preserve the "straight through the bush" communication style of a Pittsburgh veteran who doesn't have time to go around the bush.

## License

Open source. Use it however you want.
