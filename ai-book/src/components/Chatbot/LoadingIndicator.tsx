import React from 'react';

const LoadingIndicator: React.FC = () => {
  return (
    <div className="loading-indicator" role="status" aria-label="Loading">
      <div className="loading-dots">
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
      </div>
    </div>
  );
};

export default LoadingIndicator;