import React from 'react';
import { MDXProvider } from '@mdx-js/react';
import MDXComponents from '@theme/MDXComponents';
import TranslationButton from '../../components/Chapter/TranslationButton';
import { useTranslation } from '../../contexts/TranslationContext';

/**
 * MDXContent Component
 *
 * This component wraps MDX content (like chapter content) and provides
 * translation functionality to allow users to switch between English and Urdu.
 * It manages the language state and applies appropriate styling for Urdu content.
 */
const MDXContent = ({ children }) => {
  const { language, setUrdu, setEnglish } = useTranslation();

  // Function to handle language switching
  const handleTranslate = (targetLang) => {
    if (targetLang === 'ur') {
      setUrdu();
    } else {
      setEnglish();
    }
  };

  // Apply appropriate direction and styling based on language
  const getContentStyle = () => {
    if (language === 'ur') {
      return {
        direction: 'rtl',
        textAlign: 'right',
      };
    }
    return {};
  };

  return (
    <MDXProvider components={MDXComponents}>
      <div className="mdx-content-wrapper">
        {/* Translation controls */}
        <div className="translation-controls" style={{ marginBottom: '1rem', textAlign: 'right' }}>
          <TranslationButton
            contentId="mdx-content"
            onTranslate={handleTranslate}
            currentLanguage={language}
          />
        </div>

        {/* MDX Content with language-specific styling */}
        <div
          className={`mdx-content ${language === 'ur' ? 'urdu-content' : 'english-content'}`}
          style={getContentStyle()}
        >
          {children}
        </div>
      </div>
    </MDXProvider>
  );
};

export default MDXContent;