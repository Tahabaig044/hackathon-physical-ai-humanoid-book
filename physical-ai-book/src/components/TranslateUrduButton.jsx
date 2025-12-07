import React, { useState, useEffect } from 'react';
import './TranslateUrduButton.css';

const TranslateUrduButton = () => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [originalContent, setOriginalContent] = useState('');
  const [translatedContent, setTranslatedContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentUrl, setCurrentUrl] = useState('');

  // Function to get the current page content
  const getCurrentPageContent = () => {
    // Get the main content area from Docusaurus
    const contentElement = document.querySelector('article.markdown');
    if (contentElement) {
      return contentElement.innerText || contentElement.textContent;
    }
    return '';
  };

  // Function to get current URL
  const getCurrentUrl = () => {
    return window.location.pathname;
  };

  // Function to translate content
  const translateContent = async (text) => {
    setIsLoading(true);
    try {
      // In a real implementation, this would call the backend translation API
      // For now, we'll simulate the translation with a mock response
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          source_lang: 'en',
          target_lang: 'ur'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.translated_text;
      } else {
        console.error('Translation API error:', response.status);
        return null;
      }
    } catch (error) {
      console.error('Translation error:', error);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // Function to toggle translation
  const toggleTranslation = async () => {
    if (isTranslated) {
      // Switch back to original content
      setIsTranslated(false);
      restoreOriginalContent();
    } else {
      // Translate the content
      const content = getCurrentPageContent();
      if (!content) {
        console.warn('No content found to translate');
        return;
      }

      // Check if we already have a translation for this page
      const url = getCurrentUrl();
      const savedTranslation = localStorage.getItem(`translation_${url}`);

      if (savedTranslation) {
        // Use saved translation
        setTranslatedContent(savedTranslation);
        applyTranslation(savedTranslation);
        setIsTranslated(true);
      } else {
        // Need to translate
        const translated = await translateContent(content);
        if (translated) {
          setTranslatedContent(translated);
          localStorage.setItem(`translation_${url}`, translated);
          applyTranslation(translated);
          setIsTranslated(true);
        }
      }
    }
  };

  // Function to apply translation to the page
  const applyTranslation = (translatedText) => {
    const contentElement = document.querySelector('article.markdown');
    if (contentElement) {
      // Store original content for later restoration
      setOriginalContent(contentElement.innerHTML);

      // Create a temporary element to parse the translated text
      const tempElement = document.createElement('div');
      tempElement.textContent = translatedText;

      // Apply the translated content
      contentElement.innerHTML = `<div class="translated-content">${tempElement.innerHTML}</div>`;
    }
  };

  // Function to restore original content
  const restoreOriginalContent = () => {
    const contentElement = document.querySelector('article.markdown');
    if (contentElement && originalContent) {
      contentElement.innerHTML = originalContent;
    }
  };

  // Check if content is already translated when URL changes
  useEffect(() => {
    const url = getCurrentUrl();
    if (url !== currentUrl) {
      setCurrentUrl(url);

      // Check if there's a saved translation for this page
      const savedTranslation = localStorage.getItem(`translation_${url}`);
      if (savedTranslation) {
        const currentContent = getCurrentPageContent();
        if (currentContent && currentContent !== savedTranslation) {
          // Content has changed, check if we should apply translation
          // For now, we'll keep it as is unless user explicitly toggles
        }
      }
    }
  }, [currentUrl]);

  return (
    <div className="translate-urdu-container">
      <button
        className={`translate-urdu-button premium-button ${isTranslated ? 'translated' : ''} ${isLoading ? 'loading' : ''}`}
        onClick={toggleTranslation}
        disabled={isLoading}
        aria-label={isTranslated ? "Switch back to English" : "Translate to Urdu"}
      >
        {isLoading ? (
          <div className="button-content">
            <div className="button-spinner"></div>
            <span>ترجمہ ہو رہا ہے... {/* Translating... */}</span>
          </div>
        ) : isTranslated ? (
          <div className="button-content">
            <span className="button-icon">🇬🇧</span>
            <span>انگریزی میں واپس جائیں {/* Back to English */}</span>
          </div>
        ) : (
          <div className="button-content">
            <span className="button-icon">🇵🇰</span>
            <span>اردو میں ترجمہ کریں {/* Translate to Urdu */}</span>
          </div>
        )}
      </button>
    </div>
  );
};

export default TranslateUrduButton;