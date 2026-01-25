# Chatbot Integration Test

## Expected Behavior
- A floating chatbot icon should appear in the bottom right corner of every page
- Clicking the icon should open the chatbot window
- The chatbot should connect to the RAG backend API
- Users should be able to ask questions about the book content
- Responses should include source citations

## Implementation Details
1. The Root.tsx component wraps the entire application
2. The FloatingChatbot component is always present
3. The chatbot icon appears as a speech bubble in the bottom right
4. When clicked, it expands to show the full chat interface
5. It connects to the RAG backend to answer questions about book content

## Files Involved
- `src/Root.tsx` - Wraps the entire application with the floating chatbot
- `src/components/Chatbot/FloatingChatbot.tsx` - The floating icon and window component
- `src/components/Chatbot/css/floating-chatbot.css` - Styles for the floating chatbot
- `docusaurus.config.ts` - Configuration to load the Root component via clientModules

## Testing Instructions
1. Visit the website (e.g., http://localhost:3001/)
2. Look for the chatbot icon in the bottom right corner
3. Click the icon to open the chat window
4. Try asking a question about the book content
5. Verify that responses are relevant and include source citations