import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import FloatingChatbot from './FloatingChatbot';

const meta: Meta<typeof FloatingChatbot> = {
  title: 'Components/Chatbot/FloatingChatbot',
  component: FloatingChatbot,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;

type Story = StoryObj<typeof FloatingChatbot>;

export const Default: Story = {
  args: {},
};

export const Open: Story = {
  args: {},
  render: () => {
    const [isOpen, setIsOpen] = React.useState(true);
    return <FloatingChatbot />;
  },
};

export const Closed: Story = {
  args: {},
  render: () => {
    const [isOpen, setIsOpen] = React.useState(false);
    return <FloatingChatbot />;
  },
};