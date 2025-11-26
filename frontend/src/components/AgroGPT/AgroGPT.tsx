import React, { useState, useRef, useEffect } from 'react';
import { chatWithAgroGPT } from '../../services/api';
import './AgroGPT.css';
import type { AgroGPTMessage } from '../../types';

const AgroGPT: React.FC = () => {
  const [messages, setMessages] = useState<AgroGPTMessage[]>([
    {
      role: 'assistant',
      content: 'Привет! Я AgroGPT - ваш AI-помощник в вопросах агрономии. Спросите меня о растениях, почве, удобрениях или любых других сельскохозяйственных темах!',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage: AgroGPTMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatWithAgroGPT(inputMessage, messages);
      
      const assistantResponse = response?.response || "Извините, не удалось получить ответ. Попробуйте еще раз.";
      
      const assistantMessage: AgroGPTMessage = {
        role: 'assistant',
        content: assistantResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      
      const errorMessage: AgroGPTMessage = {
        role: 'assistant',
        content: 'Извините, произошла ошибка. Пожалуйста, попробуйте еще раз.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const suggestionExamples = [
    { text: "Как правильно поливать томаты?", emoji: "💧" },
    { text: "Какие удобрения лучше для картофеля?", emoji: "🌱" },
    { text: "Как бороться с вредителями капусты?", emoji: "🐛" },
    { text: "Когда сажать морковь весной?", emoji: "🥕" },
    { text: "Почему желтеют листья у огурцов?", emoji: "🥒" },
    { text: "Как подготовить почву для посадки?", emoji: "🪴" }
  ];

  return (
    <div className="agro-gpt">
      <div className="chat-header">
        <div className="header-avatar">🤖</div>
        <div className="header-content">
          <h2>AgroGPT</h2>
          <p>Ваш интеллектуальный помощник в агрономии</p>
        </div>
      </div>
      
      <div className="chat-main">
        <div className="chat-container">
          <div className="messages-container">
            <div className="welcome-message">
              <div className="welcome-icon">🌿</div>
              <div className="welcome-text">
                <h3>Добро пожаловать в AgroGPT!</h3>
                <p>Задавайте вопросы о растениях, почве, удобрениях и сельском хозяйстве</p>
              </div>
            </div>

            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
              >
                {message.role === 'assistant' && (
                  <div className="message-avatar">🤖</div>
                )}
                <div className="message-content-wrapper">
                  <div className="message-content">
                    {message.content}
                  </div>
                  <div className="message-time">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                {message.role === 'user' && (
                  <div className="message-avatar">👤</div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="message assistant-message typing">
                <div className="message-avatar">🤖</div>
                <div className="message-content-wrapper">
                  <div className="message-content typing-indicator">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    AgroGPT печатает...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <div className="input-wrapper">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Задайте вопрос о растениях, почве, удобрениях..."
                className="message-input"
                rows={1}
                disabled={loading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || loading}
                className={`send-button ${loading ? 'loading' : ''}`}
              >
                {loading ? (
                  <div className="button-spinner"></div>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="currentColor"/>
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        <div className="suggestions-sidebar">
          <div className="suggestions-header">
            <div className="suggestions-icon">💡</div>
            <h4>Примеры вопросов</h4>
          </div>
          <div className="suggestions-list">
            {suggestionExamples.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setInputMessage(suggestion.text)}
                className="suggestion-card"
              >
                <div className="suggestion-emoji">{suggestion.emoji}</div>
                <span className="suggestion-text">{suggestion.text}</span>
                <div className="suggestion-arrow">→</div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgroGPT;