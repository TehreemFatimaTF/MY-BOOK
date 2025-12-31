# Urdu Translation Feature

This feature implements Urdu translation functionality for the book website. Here's how it works:

## Components

1. **TranslationContext** - Manages the current language state across the application
2. **TranslationButton** - A yellow button that toggles between English and Urdu
3. **TranslatedContent** - Wraps content and applies translation/RTE styling
4. **TranslationService** - Handles translation API calls (currently mocked)

## How It Works

1. The yellow "Translate to Urdu" button appears at the top of each chapter
2. When clicked, it toggles the content between English and Urdu
3. In Urdu mode, the text direction changes to RTL (right-to-left) and the content is translated
4. The button text changes based on the current language state

## Implementation Details

- The translation button is implemented as a React component with a yellow color as requested
- It appears at the top of every chapter via the custom DocPage theme component
- The content is wrapped in a div with `dir="rtl"` when in Urdu mode
- A mock translation service is implemented that can be replaced with a real API

## Extending with Real Translation API

To connect to a real translation API:

1. Update `src/services/translationService.js` with actual API calls
2. Replace the mock translation API with calls to services like:
   - Google Cloud Translation API
   - Microsoft Translator Text API
   - AWS Translate
   - Or any other translation service

Example implementation for Google Translate API:

```javascript
const translateTextWithGoogle = async (text, targetLang) => {
  const response = await fetch(
    `https://translation.googleapis.com/language/translate/v2?key=${API_KEY}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        q: text,
        target: targetLang,
        format: 'text',
      }),
    }
  );
  
  const data = await response.json();
  return data.data.translations[0].translatedText;
};
```

## File Structure

```
src/
├── components/
│   └── Chapter/
│       ├── TranslationButton.js
│       ├── TranslationButton.module.css
│       └── TranslatedContent.js
├── contexts/
│   └── TranslationContext.js
├── services/
│   └── translationService.js
└── theme/
    ├── DocPage/
    │   └── index.js
    └── Root.js
```

## Styling

- The translation button is styled with yellow color (#FFD700) as requested
- Urdu content is displayed with RTL direction and appropriate font styling
- Loading states are indicated with opacity changes
- Error handling is implemented with user feedback

## Future Enhancements

1. Add support for more languages
2. Implement translation caching for better performance
3. Add progress indicators for longer content
4. Implement server-side rendering for translated content
5. Add font selection for better Urdu typography