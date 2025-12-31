import React, { useState, useEffect } from 'react';
import { useTranslation } from '@site/src/contexts/TranslationContext';
import translationService from '@site/src/services/translationService';

const TranslatedContent = ({ children }) => {
  const { language } = useTranslation();
  const [translatedContent, setTranslatedContent] = useState(children);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const translate = async () => {
      if (language === 'ur') {
        setIsLoading(true);
        try {
          const result = await translationService.translateContent(children, 'ur');
          setTranslatedContent(result);
        } catch (error) {
          console.error('Translation failed:', error);
          setTranslatedContent(children);
        } finally {
          setIsLoading(false);
        }
      } else {
        setTranslatedContent(children);
      }
    };

    translate();
  }, [language, children]);

  return (
    <div
      dir={language === 'ur' ? 'rtl' : 'ltr'}
      className={language === 'ur' ? 'urdu-content' : ''}
      style={{ opacity: isLoading ? 0.6 : 1, transition: 'opacity 0.3s' }}
    >
      {translatedContent}
    </div>
  );
};

export default TranslatedContent;