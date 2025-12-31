import React, { useState, useEffect } from 'react';
import OriginalDocPage from '@theme-original/DocPage';
import TranslationButton from '@site/src/components/Chapter/TranslationButton';
import TranslatedContent from '@site/src/components/Chapter/TranslatedContent';
import { useTranslation } from '@site/src/contexts/TranslationContext';

// Wrapper component to ensure content updates when language changes
const DocPageContent = (props) => {
  const { language } = useTranslation();
  const [key, setKey] = useState(0);

  useEffect(() => {
    // Update key when language changes to force re-render
    setKey(prev => prev + 1);
  }, [language]);

  return <OriginalDocPage key={key} {...props} />;
};

export default function DocPage(props) {
  // Generate a unique content ID based on the document metadata
  const contentId = props.content.metadata?.permalink || 'default-content-id';

  return (
    <>
      <div style={{
        padding: '10px',
        backgroundColor: '#f9f9f9',
        textAlign: 'center',
        borderBottom: '1px solid #e0e0e0'
      }}>
        <TranslationButton contentId={contentId} />
      </div>
      <TranslatedContent>
        <DocPageContent {...props} />
      </TranslatedContent>
    </>
  );
}