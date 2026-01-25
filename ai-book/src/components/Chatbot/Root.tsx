import React from 'react';
import FloatingChatbot from './FloatingChatbot';

const Root: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
};

export default Root;