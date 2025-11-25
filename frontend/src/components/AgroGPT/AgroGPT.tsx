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
      
      // ФИКС: проверяем что response и response.response существуют
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

  return (
    <div className="agro-gpt">
      <h2>🤖 AgroGPT - Ваш агрономический помощник</h2>
      
      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant-message">
              <div className="message-content typing-indicator">
                AgroGPT печатает...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Задайте вопрос о растениях, почве, удобрениях..."
            className="message-input"
            rows={3}
            disabled={loading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || loading}
            className="send-button"
          >
            Отправить
          </button>
        </div>
      </div>

      <div className="suggestions">
        <h4>Примеры вопросов:</h4>
        <div className="suggestion-chips">
          <button
            onClick={() => setInputMessage("Как правильно поливать томаты?")}
            className="suggestion-chip"
          >
            Полив томатов
          </button>
          <button
            onClick={() => setInputMessage("Какие удобрения лучше для картофеля?")}
            className="suggestion-chip"
          >
            Удобрения для картофеля
          </button>
          <button
            onClick={() => setInputMessage("Как бороться с вредителями капусты?")}
            className="suggestion-chip"
          >
            Вредители капусты
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgroGPT;