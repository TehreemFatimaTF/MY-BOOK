import React, { createContext, useContext, useState } from 'react';

const TranslationContext = createContext();

export const TranslationProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'ur' : 'en');
  };

  const setUrdu = () => {
    setLanguage('ur');
  };

  const setEnglish = () => {
    setLanguage('en');
  };

  return (
    <TranslationContext.Provider value={{
      language,
      toggleLanguage,
      setUrdu,
      setEnglish,
      isUrdu: language === 'ur'
    }}>
      {children}
    </TranslationContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
};