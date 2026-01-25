import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from './types';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-content">
        <ReactMarkdown
          components={{
            // Customize rendering for different markdown elements
            p: ({ node, ...props }) => <p {...props} />,
            ul: ({ node, ...props }) => <ul className="markdown-list" {...props} />,
            ol: ({ node, ...props }) => <ol className="markdown-list" {...props} />,
            li: ({ node, ...props }) => <li {...props} />,
            code: ({ node, ...props }) => <code className="markdown-code" {...props} />,
            pre: ({ node, ...props }) => <pre className="markdown-pre" {...props} />,
            strong: ({ node, ...props }) => <strong {...props} />,
            em: ({ node, ...props }) => <em {...props} />,
            a: ({ node, ...props }) => <a {...props} target="_blank" rel="noopener noreferrer" />,
          }}
        >
          {message.content}
        </ReactMarkdown>
      </div>
      {message.sources && message.sources.length > 0 && (
        <div className="message-sources">
          <h4>Sources:</h4>
          <ul>
            {message.sources.map((source, index) => (
              <li key={index}>
                <a href={source.url} target="_blank" rel="noopener noreferrer">
                  {source.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MessageBubble;