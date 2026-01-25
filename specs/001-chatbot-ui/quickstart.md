# Quickstart Guide: Chatbot UI Integration

## Overview
This guide provides the essential steps to set up and integrate the chatbot UI with the Docusaurus book site.

## Prerequisites
- Node.js 18+ and npm/yarn
- Docusaurus 3.x installed and configured
- RAG backend API running and accessible
- Basic knowledge of React and TypeScript

## Installation Steps

### 1. Clone and Set Up the Repository
```bash
git clone [repository-url]
cd [repository-name]
cd ai-book
npm install
```

### 2. Verify Backend Connection
Before running the UI, ensure your RAG backend is running:
```bash
# Check if backend is accessible
curl http://localhost:8000/health
```

### 3. Add Chatbot Components
The chatbot components will be located in `ai-book/src/components/Chatbot/`:
- `Chatbot.tsx` - Main chatbot container
- `ChatWindow.tsx` - Message display area
- `MessageInput.tsx` - Input field with send button
- `MessageBubble.tsx` - Individual message display
- `LoadingIndicator.tsx` - Loading state indicator

### 4. Environment Configuration
Add the backend API URL to your environment configuration:

Create `.env.local` in the `ai-book` directory:
```bash
# RAG Backend API URL
REACT_APP_RAG_API_URL=http://localhost:8000
```

### 5. Integrate with Docusaurus
Import and add the chatbot component to your desired page:

In `ai-book/src/pages/index.tsx` or desired page:
```tsx
import Chatbot from '../components/Chatbot/Chatbot';

function HomePage() {
  return (
    <Layout>
      {/* Your existing page content */}
      <Chatbot />
    </Layout>
  );
}
```

### 6. Run the Development Server
```bash
cd ai-book
npm start
```

The chatbot UI should now be available on your Docusaurus site.

## Basic Usage

### For Users
1. Type your question about the book content in the input field
2. Press Enter or click the Send button
3. View the response with source citations
4. Ask follow-up questions to continue the conversation

### For Developers
- The chat history is maintained within the React component state
- API calls are made to the RAG backend endpoint
- Error handling is implemented for various failure scenarios
- The UI is responsive and works on mobile devices

## Testing the Integration

### Manual Testing
1. Start the development server: `npm start`
2. Navigate to the page where the chatbot is integrated
3. Type a question and verify the response appears
4. Test error handling by temporarily stopping the backend
5. Verify mobile responsiveness

### API Testing
The chatbot makes POST requests to `/query` endpoint with the following format:
```json
{
  "query": "Your question here",
  "top_k": 3
}
```

## Troubleshooting

### Common Issues
- **Backend not responding**: Verify the RAG backend is running and accessible at the configured URL
- **CORS errors**: Ensure the backend allows requests from your frontend origin
- **Component not rendering**: Check that all required dependencies are installed
- **Styling conflicts**: The chatbot uses CSS modules to avoid conflicts with Docusaurus styles

### Environment Variables
- `REACT_APP_RAG_API_URL` - Backend API URL (default: http://localhost:8000)
- `REACT_APP_CHATBOT_ENABLED` - Toggle to enable/disable chatbot (default: true)

## Next Steps
1. Customize the chatbot styling to match your site's theme
2. Add analytics to track usage and improve the experience
3. Implement conversation persistence if needed
4. Add additional features like conversation history export