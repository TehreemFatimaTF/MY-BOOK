/**
 * TranslationButton Component
 *
 * A button component that allows users to translate chapter content to Urdu.
 * This component handles the translation functionality and UI.
 */

import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './TranslationButton.module.css';
import { useTranslation } from '@site/src/contexts/TranslationContext';

const TranslationButton = ({ contentId, onTranslate }) => {
  const { language, toggleLanguage, setUrdu, setEnglish } = useTranslation();
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationStatus, setTranslationStatus] = useState('idle'); // idle, loading, success, error

  const handleTranslate = async () => {
    if (onTranslate) {
      // If onTranslate callback is provided, use it
      const targetLanguage = language === 'ur' ? 'en' : 'ur';
      onTranslate(targetLanguage);
      return;
    }

    if (language === 'ur') {
      // If already in Urdu, switch back to English
      setEnglish();
      return;
    }

    setIsTranslating(true);
    setTranslationStatus('loading');

    try {
      // In a real implementation, this would call the backend translation API
      // For now, we'll simulate the translation process
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call

      // Switch to Urdu
      setUrdu();
      setTranslationStatus('success');

      // Reset status after a short delay
      setTimeout(() => setTranslationStatus('idle'), 2000);
    } catch (error) {
      console.error('Translation failed:', error);
      setTranslationStatus('error');
      setTimeout(() => setTranslationStatus('idle'), 3000);
    } finally {
      setIsTranslating(false);
    }
  };

  // Determine button text based on current language
  const getButtonText = () => {
    if (translationStatus === 'loading') {
      return language === 'ur' ? 'ترجمہ ہو رہا ہے...' : 'Translating...';
    }
    if (language === 'ur') {
      return 'Switch to English'; // Switch to English
    }
    return 'Translate to Urdu'; // Translate to Urdu
  };

  // Determine button class based on status
  const getButtonClass = () => {
    return clsx(
      styles.translateButton,
      {
        [styles.loading]: translationStatus === 'loading',
        [styles.success]: translationStatus === 'success',
        [styles.error]: translationStatus === 'error',
        [styles.urduMode]: language === 'ur',
      }
    );
  };

  return (
    <div className={styles.translationContainer}>
      <button
        className={getButtonClass()}
        onClick={handleTranslate}
        disabled={isTranslating}
        title={language === 'ur' ? 'انگریزی میں تبدیل کریں' : 'اردو میں ترجمہ کریں'}
      >
        <span className={styles.buttonText}>
          {getButtonText()}
        </span>
        {translationStatus === 'loading' && (
          <span className={styles.spinner}>↻</span>
        )}
        {translationStatus === 'success' && (
          <span className={styles.checkmark}>✓</span>
        )}
        {translationStatus === 'error' && (
          <span className={styles.errorIcon}>⚠️</span>
        )}
      </button>
      {translationStatus === 'error' && (
        <div className={styles.errorMessage}>
          Translation failed. Please try again.
        </div>
      )}
    </div>
  );
};

export default TranslationButton;