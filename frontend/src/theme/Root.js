import ChatbotWidget from '../components/Chat/ChatbotWidget'; // match the name
import React from 'react';

export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
}
