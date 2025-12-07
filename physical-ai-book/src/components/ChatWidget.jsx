import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent' // Add status for message delivery indicators
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Simulate network delay for better UX
      await new Promise(resolve => setTimeout(resolve, 500));

      // Call the backend API to get response
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: 'default_conversation' // In a real app, you'd manage conversation IDs
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
          timestamp: new Date(),
          status: 'delivered'
        };

        // Update user message status
        setMessages(prev =>
          prev.map(msg =>
            msg.id === userMessage.id ? {...msg, status: 'delivered'} : msg
          )
        );

        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error processing your request.',
          sender: 'bot',
          timestamp: new Date(),
          status: 'delivered'
        };

        // Update user message status
        setMessages(prev =>
          prev.map(msg =>
            msg.id === userMessage.id ? {...msg, status: 'failed'} : msg
          )
        );

        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I\'m having trouble connecting to the server.',
        sender: 'bot',
        timestamp: new Date(),
        status: 'delivered'
      };

      // Update user message status
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id ? {...msg, status: 'failed'} : msg
        )
      );

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-widget">
      {isOpen ? (
        <div className="chat-container">
          <div className="chat-header">
            <div className="chat-header-content">
              <div className="chat-header-icon">🤖</div>
              <h3>Textbook Assistant</h3>
              <div className="chat-status-indicator">
                <div className="status-dot online"></div>
              </div>
            </div>
            <button className="chat-close" onClick={toggleChat} aria-label="Close chat">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <div className="welcome-icon">📚</div>
                <p>Hello! I'm your Textbook Assistant.</p>
                <p>Ask me anything about Physical AI and Humanoid Robotics.</p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={message.id}
                  className={`message ${message.sender} message-enter`}
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>
                    <div className="message-footer">
                      <div className="message-time">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                      {message.sender === 'user' && (
                        <div className={`message-status ${message.status}`}>
                          {message.status === 'sent' && '✓'}
                          {message.status === 'delivered' && '✓✓'}
                          {message.status === 'failed' && '⚠️'}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot message-enter">
                <div className="message-content">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the textbook..."
              className="chat-input"
              rows="1"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="chat-send-button"
              aria-label="Send message"
            >
              {isLoading ? (
                <div className="send-spinner"></div>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </button>
          </div>
        </div>
      ) : (
        <button
          className="chat-open-button floating-button"
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <div className="chat-button-content">
            <div className="chat-icon">💬</div>
            <div className="chat-label">Ask AI</div>
          </div>
          <div className="chat-unread-badge"></div>
        </button>
      )}
    </div>
  );
};

export default ChatWidget;