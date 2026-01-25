/**
 * End-to-end test for the Chatbot component
 * This test verifies the complete functionality of the chatbot UI
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Chatbot from './Chatbot';

// Mock the API service
jest.mock('./services/apiService', () => ({
  apiService: {
    queryRagBackend: jest.fn(),
    checkHealth: jest.fn(),
  },
}));

// Mock the validation utilities
jest.mock('./utils/validation', () => ({
  validateMessageContent: jest.fn(),
}));

describe('Chatbot Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders chatbot interface correctly', () => {
    render(<Chatbot />);

    expect(screen.getByText('Book Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Ask a question about the book content...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Clear conversation' })).toBeInTheDocument();
  });

  test('allows user to send a message', async () => {
    const { validateMessageContent } = require('./utils/validation');
    validateMessageContent.mockReturnValue({ isValid: true });

    const { queryRagBackend } = require('./services/apiService');
    queryRagBackend.mockResolvedValue({
      answer: 'This is a test response',
      sources: [],
      retrieved_chunks: [],
      success: true,
    });

    render(<Chatbot />);

    const input = screen.getByPlaceholderText('Ask a question about the book content...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Test question')).toBeInTheDocument();
      expect(screen.getByText('This is a test response')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    const { validateMessageContent } = require('./utils/validation');
    validateMessageContent.mockReturnValue({ isValid: true });

    const { queryRagBackend } = require('./services/apiService');
    queryRagBackend.mockRejectedValue(new Error('Network error'));

    render(<Chatbot />);

    const input = screen.getByPlaceholderText('Ask a question about the book content...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('An error occurred while processing your request')).toBeInTheDocument();
    });
  });

  test('clears conversation history', async () => {
    const { validateMessageContent } = require('./utils/validation');
    validateMessageContent.mockReturnValue({ isValid: true });

    const { queryRagBackend } = require('./services/apiService');
    queryRagBackend.mockResolvedValue({
      answer: 'This is a test response',
      sources: [],
      retrieved_chunks: [],
      success: true,
    });

    render(<Chatbot />);

    // Send a message first
    const input = screen.getByPlaceholderText('Ask a question about the book content...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Test question')).toBeInTheDocument();
    });

    // Clear the conversation
    const clearButton = screen.getByRole('button', { name: 'Clear conversation' });
    fireEvent.click(clearButton);

    // Verify conversation is cleared
    expect(screen.queryByText('Test question')).not.toBeInTheDocument();
    expect(screen.queryByText('This is a test response')).not.toBeInTheDocument();
  });

  test('validates message content before sending', async () => {
    const { validateMessageContent } = require('./utils/validation');
    validateMessageContent.mockReturnValue({
      isValid: false,
      error: 'Message must be at least 3 characters long'
    });

    render(<Chatbot />);

    const input = screen.getByPlaceholderText('Ask a question about the book content...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Hi' } }); // Too short
    fireEvent.click(sendButton);

    expect(screen.getByText('Message must be at least 3 characters long')).toBeInTheDocument();
  });
});