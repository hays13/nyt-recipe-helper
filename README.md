# NYT Cooking Allergen Checker

A Chrome extension that automatically scans ingredients on [NYT Cooking](https://cooking.nytimes.com/) recipes and displays icons for the 9 major allergens:
milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy, sesame.

## Features
- Automatically extracts ingredient lists from NYT Cooking recipes
- Uses the ChatGPT API to detect allergens in natural language
- Displays icons for allergens just above the "Total Time" section
- Clean integration with the site's layout
- Built with Manifest V3, JavaScript, Flask, and OpenAI API

## Installation (Developer Mode)
1. Clone or download this repository
2. Go to `chrome://extensions` in your browser
3. Enable Developer Mode
4. Click "Load unpacked"
5. Select the extension folder

## Folder Structure
```
nyt-allergen-extension/
├── manifest.json
├── background.js
├── content.js
├── app.py
├── icons/
│   ├── milk.png
│   ├── soy.png
│   └── ... (one for each allergen)
```

## Known Limitations
- ChatGPT may occasionally miss an allergen or over-label an ingredient
- Only works on NYT Cooking pages
- API key must be configured manually in `app.py`

## To Do (Future Features)
- Detect required kitchen equipment (e.g. "sheet pan", "Dutch oven")
- Allow user-defined allergen preferences
- Add a popup settings UI
- Recipe scaling functionality
