import React from 'react';
import Layout from '@theme-original/Layout';
import Chatbot from '../components/Chatbot/Chatbot';
import FloatingChatbot from '../components/Chatbot/FloatingChatbot';

type Props = {
  children?: React.ReactNode;
};

const ChatbotLayout: React.ComponentType<Props> = ({ children }) => {
  return (
    <Layout>
      {children}
      <FloatingChatbot/>
    </Layout>
  );
};

export default ChatbotLayout;
 