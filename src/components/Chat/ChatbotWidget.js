import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChatbotWidget.module.css';

const ChatbotWidget = ({ initialOpen = false }) => {
  const [isOpen, setIsOpen] = useState(initialOpen);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // 1. User ka message UI par dikhayein
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue; // Copy for API call
    setInputValue('');
    setIsLoading(true);

    try {
      // 2. Python Agent (FastAPI) ko call karein
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: currentInput }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // 3. Agent ka real response UI mein add karein
      const botMessage = {
        id: Date.now() + 1,
        text: data.reply, 
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: ['Physical AI Textbook']
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      // Error handling agar backend off ho
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting to my brain. Is the backend running?",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error("API Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.chatContainer}>
      {isOpen ? (
        <div className={styles.chatWidget}>
          <div className={styles.chatHeader}>
            <div className={styles.chatTitle}>Physical AI Assistant</div>
            <div className={styles.chatSubtitle}>Connected to Agent</div>
            <button className={styles.closeButton} onClick={toggleChat}>×</button>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your Physical AI assistant. I will answer using the textbook data.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div key={message.id} className={clsx(styles.message, styles[message.sender])}>
                  <div className={styles.messageContent}>
                    <div className={styles.messageText}>{message.text}</div>
                    <div className={styles.messageMeta}>
                      <span className={styles.timestamp}>{message.timestamp}</span>
                      {message.sender === 'bot' && message.sources && (
                        <span className={styles.sources}>Sources: {message.sources.join(', ')}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className={clsx(styles.message, styles.bot)}>
                <div className={styles.typingIndicator}>
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputArea}>
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about the textbook..."
              className={styles.chatInput}
              rows="1"
              disabled={isLoading}
            />
            <button 
              onClick={handleSendMessage} 
              disabled={!inputValue.trim() || isLoading}
              className={clsx(styles.sendButton, (!inputValue.trim() || isLoading) && styles.sendButtonDisabled)}
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <img src="/img/chatboiconn.jpg" width={100} alt="Chat Icon" className={styles.chatFloatingIcon} onClick={toggleChat} />
      )}
    </div>
  );
};

export default ChatbotWidget;