import React from 'react';
import FloatingChatbot from './components/Chatbot/FloatingChatbot';

const Root = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
};

export default Root;