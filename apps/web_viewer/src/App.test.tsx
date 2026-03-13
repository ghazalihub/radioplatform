import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders platform title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Advanced Radiology Platform/i);
  expect(titleElement).toBeInTheDocument();
});
