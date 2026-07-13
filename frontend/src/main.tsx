import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from '@/app/App';
/* Global design system */
import '@/styles/globals.css';

/* Pixel scene background animations (vanilla CSS project) */
import '../css/pixel-scene.css';

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found. Ensure index.html has a <div id="root"></div>.');
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
