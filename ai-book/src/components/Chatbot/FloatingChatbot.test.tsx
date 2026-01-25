// Basic unit tests for FloatingChatbot component
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FloatingChatbot from './FloatingChatbot';

describe('FloatingChatbot Component', () => {
  test('renders floating icon initially', () => {
    render(<FloatingChatbot />);
    const icon = screen.getByLabelText(/Open chatbot/i);
    expect(icon).toBeInTheDocument();
  });

  test('toggles chat panel on icon click', () => {
    render(<FloatingChatbot />);
    const icon = screen.getByLabelText(/Open chatbot/i);

    // Initially panel should not be visible
    expect(screen.queryByLabelText(/Close chatbot/i)).not.toBeInTheDocument();

    // Click icon to open panel
    fireEvent.click(icon);

    // Panel should now be visible
    expect(screen.getByLabelText(/Close chatbot/i)).toBeInTheDocument();
  });

  test('closes panel when close button is clicked', () => {
    render(<FloatingChatbot />);
    const icon = screen.getByLabelText(/Open chatbot/i);

    // Open the panel
    fireEvent.click(icon);
    expect(screen.getByLabelText(/Close chatbot/i)).toBeInTheDocument();

    // Close the panel
    const closeBtn = screen.getByLabelText(/Close chatbot/i);
    fireEvent.click(closeBtn);

    // Panel should be closed
    expect(screen.queryByLabelText(/Close chatbot/i)).not.toBeInTheDocument();
  });

  test('tooltip appears on hover', () => {
    render(<FloatingChatbot />);
    const icon = screen.getByLabelText(/Open chatbot/i);

    fireEvent.mouseEnter(icon);
    expect(screen.getByText(/Ask a question about the book/i)).toBeInTheDocument();

    fireEvent.mouseLeave(icon);
    expect(screen.queryByText(/Ask a question about the book/i)).not.toBeInTheDocument();
  });
});