# Telegram Mini App Guidelines

> This document is intended for automatic use by AI models when generating code for Telegram Mini Apps.  
> Adherence to these guidelines is mandatory for all Telegram Mini App parts of the project.

---

## 1. Telegram WebApp API Usage

### 1.1. Initialization

The Telegram WebApp must be initialized at the very beginning of the application lifecycle.

```tsx
// ✅ Correct — initialize Telegram WebApp on app startup
import { useEffect } from 'react';

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp;
    };
  }
}

interface TelegramWebApp {
  initData: string;
  initDataUnsafe: {
    query_id?: string;
    user?: TelegramUser;
    auth_date?: string;
    hash?: string;
  };
  colorScheme: 'light' | 'dark';
  themeParams: ThemeParams;
  isExpanded: boolean;
  viewportHeight: number;
  viewportStableHeight: number;
  platform: string;
  headerColor: string;
  backgroundColor: string;
  isClosingConfirmationEnabled: boolean;
  BackButton: BackButton;
  MainButton: MainButton;
  HapticFeedback: HapticFeedback;
  ready: () => void;
  expand: () => void;
  close: () => void;
  setHeaderColor: (color: string) => void;
  setBackgroundColor: (color: string) => void;
  enableClosingConfirmation: () => void;
  disableClosingConfirmation: () => void;
  onEvent: (eventType: string, callback: () => void) => void;
  offEvent: (eventType: string, callback: () => void) => void;
  sendData: (data: string) => void;
  switchInlineQuery: (query: string, chooseChatTypes?: string[]) => void;
  version: string;
}

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium?: boolean;
}

interface ThemeParams {
  bg_color?: string;
  text_color?: string;
  hint_color?: string;
  link_color?: string;
  button_color?: string;
  button_text_color?: string;
  secondary_bg_color?: string;
  header_bg_color?: string;
  accent_text_color?: string;
  section_bg_color?: string;
  section_header_text_color?: string;
  subtitle_text_color?: string;
  destructive_text_color?: string;
}

interface BackButton {
  isVisible: boolean;
  show: () => void;
  hide: () => void;
  onClick: (callback: () => void) => void;
  offClick: (callback: () => void) => void;
}

interface MainButton {
  text: string;
  color: string;
  textColor: string;
  isVisible: boolean;
  isActive: boolean;
  isProgressVisible: boolean;
  setText: (text: string) => void;
  setColor: (color: string) => void;
  setTextColor: (color: string) => void;
  show: () => void;
  hide: () => void;
  enable: () => void;
  disable: () => void;
  showProgress: () => void;
  hideProgress: () => void;
  onClick: (callback: () => void) => void;
  offClick: (callback: () => void) => void;
}

interface HapticFeedback {
  impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
  notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
  selectionChanged: () => void;
}
```

### 1.2. Initialization Hook

Create a dedicated hook for Telegram WebApp initialization.

```tsx
// ✅ Correct — Telegram initialization hook
import { create } from 'zustand';

interface TelegramState {
  webApp: TelegramWebApp | null;
  user: TelegramUser | null;
  colorScheme: 'light' | 'dark';
  theme: ThemeParams | null;
  platform: string;
  isReady: boolean;
}

export const useTelegramStore = create<TelegramState>((set) => ({
  webApp: null,
  user: null,
  colorScheme: 'light',
  theme: null,
  platform: '',
  isReady: false,
}));

export function useTelegramInit() {
  const setStore = useTelegramStore.setState;

  useEffect(() => {
    const tg = window.Telegram?.WebApp;

    if (!tg) {
      console.warn('Telegram WebApp is not available');
      return;
    }

    // Initialize
    tg.ready();
    tg.expand();

    setStore({
      webApp: tg,
      user: tg.initDataUnsafe.user ?? null,
      colorScheme: tg.colorScheme,
      theme: tg.themeParams,
      platform: tg.platform,
      isReady: true,
    });

    // Listen for theme changes
    const handleThemeChange = () => {
      setStore({
        colorScheme: tg.colorScheme,
        theme: tg.themeParams,
      });
    };

    tg.onEvent('themeChanged', handleThemeChange);

    return () => {
      tg.offEvent('themeChanged', handleThemeChange);
    };
  }, []);
}
```

### 1.3. Accessing Telegram Data

Always use the store to access Telegram data — never access `window.Telegram` directly in components.

```tsx
// ✅ Correct
const user = useTelegramStore((state) => state.user);
const colorScheme = useTelegramStore((state) => state.colorScheme);

// ❌ Incorrect — direct window access in components
const user = window.Telegram?.WebApp.initDataUnsafe.user;
```

### 1.4. Lifecycle Events

Listen to Telegram lifecycle events for proper behavior.

| Event | Description |
|---|---|
| `themeChanged` | Theme (light/dark) or color scheme changed |
| `viewportChanged` | Viewport size changed (keyboard opened/closed) |
| `mainButtonClicked` | Main button was pressed |
| `backButtonClicked` | Back button was pressed |
| `popupClosed` | Popup was closed |
| `clipboardTextReceived` | Text was received from clipboard |

```tsx
// ✅ Correct — lifecycle event handling
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  const handleViewportChange = () => {
    setStore({
      viewportHeight: tg.viewportHeight,
      viewportStableHeight: tg.viewportStableHeight,
      isExpanded: tg.isExpanded,
    });
  };

  tg.onEvent('viewportChanged', handleViewportChange);
  return () => tg.offEvent('viewportChanged', handleViewportChange);
}, []);
```

---

## 2. Dark Theme

### 2.1. Detecting Dark Mode

Detect the current Telegram theme and always respect the user's choice.

```tsx
// ✅ Correct — use Telegram's colorScheme
const colorScheme = useTelegramStore((state) => state.colorScheme);
const isDark = colorScheme === 'dark';

// Apply theme class to document
useEffect(() => {
  document.documentElement.classList.toggle('dark', isDark);
}, [isDark]);
```

### 2.2. Using Telegram Theme Colors

Use Telegram's theme parameters for seamless integration.

```tsx
// ✅ Correct — applying Telegram theme colors via CSS variables
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  const root = document.documentElement;
  const tp = tg.themeParams;

  root.style.setProperty('--tg-bg-color', tp.bg_color || '#ffffff');
  root.style.setProperty('--tg-text-color', tp.text_color || '#000000');
  root.style.setProperty('--tg-hint-color', tp.hint_color || '#999999');
  root.style.setProperty('--tg-link-color', tp.link_color || '#2481cc');
  root.style.setProperty('--tg-button-color', tp.button_color || '#2481cc');
  root.style.setProperty('--tg-button-text-color', tp.button_text_color || '#ffffff');
  root.style.setProperty('--tg-secondary-bg-color', tp.secondary_bg_color || '#f4f4f5');
  root.style.setProperty('--tg-header-bg-color', tp.header_bg_color || '#ffffff');
  root.style.setProperty('--tg-accent-text-color', tp.accent_text_color || '#2481cc');
  root.style.setProperty('--tg-section-bg-color', tp.section_bg_color || '#ffffff');
  root.style.setProperty('--tg-section-header-text-color', tp.section_header_text_color || '#2481cc');
  root.style.setProperty('--tg-subtitle-text-color', tp.subtitle_text_color || '#999999');
  root.style.setProperty('--tg-destructive-text-color', tp.destructive_text_color || '#e53935');
}, [colorScheme]);
```

### 2.3. Tailwind Dark Mode

Configure Tailwind to use class-based dark mode and apply Telegram colors.

```ts
// tailwind.config.ts — class-based dark mode
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        tg: {
          bg: 'var(--tg-bg-color)',
          text: 'var(--tg-text-color)',
          hint: 'var(--tg-hint-color)',
          link: 'var(--tg-link-color)',
          button: 'var(--tg-button-color)',
          'button-text': 'var(--tg-button-text-color)',
          'secondary-bg': 'var(--tg-secondary-bg-color)',
          'header-bg': 'var(--tg-header-bg-color)',
          'accent-text': 'var(--tg-accent-text-color)',
          'section-bg': 'var(--tg-section-bg-color)',
          'section-header-text': 'var(--tg-section-header-text-color)',
          'subtitle-text': 'var(--tg-subtitle-text-color)',
          'destructive-text': 'var(--tg-destructive-text-color)',
        },
      },
    },
  },
};
```

```tsx
// ✅ Correct — using Telegram theme colors in components
<div className="bg-tg-bg text-tg-text">
  <h1 className="text-tg-text">Title</h1>
  <p className="text-tg-hint">Description</p>
  <a href="#" className="text-tg-link">Link</a>
  <button className="bg-tg-button text-tg-button-text rounded-lg px-4 py-2">
    Button
  </button>
</div>
```

### 2.4. Dark Mode Styles

Always test components in both themes. Never hardcode colors that ignore Telegram's theme.

```tsx
// ✅ Correct — respects Telegram theme
<div className="bg-tg-bg text-tg-text" />

// ❌ Incorrect — hardcoded colors ignore user's theme
<div className="bg-white text-black dark:bg-gray-900 dark:text-white" />
```

---

## 3. Light Theme

### 3.1. Light Mode Detection

Light mode is the default. The same Telegram theme variables handle both modes automatically.

```tsx
// ✅ Correct — light mode is handled by Telegram theme variables
// No additional logic needed; Telegram provides the correct colors
const isDark = useTelegramStore((state) => state.colorScheme) === 'dark';
```

### 3.2. Handling Both Themes

Use the same CSS variables for both themes — Telegram automatically provides correct values for each.

```tsx
// ✅ Correct — single set of CSS variables works for both themes
// Telegram's themeParams change automatically when user switches theme
<div
  style={{
    backgroundColor: 'var(--tg-bg-color)',
    color: 'var(--tg-text-color)',
  }}
>
  Content
</div>
```

---

## 4. Safe Area

### 4.1. Understanding Safe Areas

Telegram Mini Apps have safe areas to avoid overlapping with Telegram's native UI elements (header, navigation bar, keyboard).

### 4.2. Applying Safe Area Padding

```tsx
// ✅ Correct — applying safe area padding
import { cn } from '@/shared/lib/cn';

interface SafeAreaProps {
  children: React.ReactNode;
  className?: string;
}

export function SafeArea({ children, className }: SafeAreaProps) {
  return (
    <div
      className={cn(
        'px-4',
        'pt-[env(safe-area-inset-top)]',
        'pb-[env(safe-area-inset-bottom)]',
        'pl-[env(safe-area-inset-left)]',
        'pr-[env(safe-area-inset-right)]',
        className
      )}
    >
      {children}
    </div>
  );
}
```

### 4.3. Safe Area for iOS Notch

iOS devices with a notch need extra top padding.

```tsx
// ✅ Correct — iOS safe area with notch support
<div
  className={cn(
    'min-h-screen',
    'pt-12 md:pt-0',          // Extra top padding for notch
    'pb-20 md:pb-0',           // Extra bottom padding for home indicator
    'bg-tg-bg'
  )}
>
  {children}
</div>
```

### 4.4. Safe Area Utility Hook

```tsx
// ✅ Correct — safe area values hook
export function useSafeArea() {
  const platform = useTelegramStore((state) => state.platform);
  const isIOS = platform === 'ios' || platform === 'macos';

  return {
    top: isIOS ? 44 : 0,     // iOS notch ~44px, Android: 0
    bottom: isIOS ? 34 : 0,  // iOS home indicator ~34px, Android: 0
    left: 0,
    right: 0,
    isIOS,
  };
}
```

### 4.5. Expanding to Full Screen

Always request full screen expansion for a better user experience.

```tsx
// ✅ Correct — expand to full screen on init
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (tg) {
    tg.expand();
    // Set header color to match app background
    tg.setHeaderColor(tg.themeParams.bg_color || '#ffffff');
    tg.setBackgroundColor(tg.themeParams.bg_color || '#ffffff');
  }
}, []);
```

---

## 5. Navigation

### 5.1. Navigation Structure

Telegram Mini Apps should use simple, flat navigation. Avoid complex nested routing.

```tsx
// ✅ Correct — simple flat routing for Telegram Mini App
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'profile', element: <ProfilePage /> },
      { path: 'settings', element: <SettingsPage /> },
      { path: 'item/:id', element: <ItemDetailPage /> },
    ],
  },
]);
```

### 5.2. Navigation Between Screens

Keep navigation simple. Depth should not exceed 2-3 levels.

```tsx
// ✅ Correct — use navigation hooks
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div>
      <button onClick={() => navigate('/profile')}>
        Go to Profile
      </button>
      <button onClick={() => navigate('/item/123')}>
        View Item
      </button>
    </div>
  );
}
```

### 5.3. Managing Navigation History

Track navigation history to control the Back button behavior.

```tsx
// ✅ Correct — navigation history tracking
import { create } from 'zustand';

interface NavigationState {
  history: string[];
  push: (path: string) => void;
  pop: () => string | undefined;
  clear: () => void;
}

export const useNavigationStore = create<NavigationState>((set, get) => ({
  history: [],
  push: (path) => set((state) => ({ history: [...state.history, path] })),
  pop: () => {
    const state = get();
    if (state.history.length === 0) return undefined;
    const newHistory = [...state.history];
    const last = newHistory.pop();
    set({ history: newHistory });
    return last;
  },
  clear: () => set({ history: [] }),
}));
```

---

## 6. Keyboard Opening

### 6.1. Detecting Keyboard State

Listen for viewport changes to detect when the keyboard opens or closes.

```tsx
// ✅ Correct — keyboard detection hook
import { useState, useEffect } from 'react';
import { useTelegramStore } from '@/features/telegram/hooks/useTelegramInit';

export function useKeyboard() {
  const webApp = useTelegramStore((state) => state.webApp);
  const [isKeyboardOpen, setIsKeyboardOpen] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(0);

  useEffect(() => {
    const tg = webApp;
    if (!tg) return;

    const handleViewportChange = () => {
      const stableHeight = tg.viewportStableHeight;
      const height = tg.viewportHeight;
      const diff = stableHeight - height;

      if (diff > 100) {
        setIsKeyboardOpen(true);
        setKeyboardHeight(diff);
      } else {
        setIsKeyboardOpen(false);
        setKeyboardHeight(0);
      }
    };

    tg.onEvent('viewportChanged', handleViewportChange);
    return () => tg.offEvent('viewportChanged', handleViewportChange);
  }, [webApp]);

  return { isKeyboardOpen, keyboardHeight };
}
```

### 6.2. Adjusting Layout When Keyboard Opens

Shift content up when the keyboard appears so inputs remain visible.

```tsx
// ✅ Correct — scroll input into view when keyboard opens
function ChatInput() {
  const { isKeyboardOpen } = useKeyboard();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isKeyboardOpen) {
      // Small delay to wait for keyboard animation
      setTimeout(() => {
        inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 300);
    }
  }, [isKeyboardOpen]);

  return (
    <div
      className={cn(
        'fixed bottom-0 left-0 right-0 transition-transform duration-300',
        isKeyboardOpen && 'translate-y-[-50%]'
      )}
    >
      <input ref={inputRef} type="text" className="w-full p-4 bg-tg-bg text-tg-text" />
    </div>
  );
}
```

### 6.3. Input Best Practices

```tsx
// ✅ Correct — input handling with Telegram
function TelegramInput() {
  return (
    <div className="p-4">
      <label className="block text-tg-text mb-2">Name</label>
      <input
        type="text"
        className={cn(
          'w-full p-3 rounded-lg border',
          'bg-tg-section-bg text-tg-text',
          'border-tg-hint focus:border-tg-link',
          'outline-none transition-colors'
        )}
        placeholder="Enter your name"
        autoComplete="off"
      />
    </div>
  );
}
```

---

## 7. Back Button

### 7.1. Showing and Hiding the Back Button

Control the Telegram Back button via the WebApp API based on navigation state.

```tsx
// ✅ Correct — Back button manager hook
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useTelegramStore } from '@/features/telegram/hooks/useTelegramInit';
import { useNavigationStore } from '@/shared/hooks/useNavigationStore';

export function useBackButton() {
  const webApp = useTelegramStore((state) => state.webApp);
  const location = useLocation();
  const { history, push, pop } = useNavigationStore();

  // Track navigation
  useEffect(() => {
    push(location.pathname);
  }, [location.pathname]);

  // Show/hide back button
  useEffect(() => {
    const tg = webApp;
    if (!tg) return;

    // Show Back button only if we're not on the main page
    if (history.length > 1) {
      tg.BackButton.show();
    } else {
      tg.BackButton.hide();
    }
  }, [webApp, history.length]);

  // Handle Back button click
  useEffect(() => {
    const tg = webApp;
    if (!tg) return;

    const handleBack = () => {
      if (history.length > 1) {
        pop();
        // Navigate back using your router
        window.history.back();
      } else {
        // If there's no history, close the app
        tg.close();
      }
    };

    tg.BackButton.onClick(handleBack);
    return () => tg.BackButton.offClick(handleBack);
  }, [webApp, history.length]);
}
```

### 7.2. Using the Back Button Hook

```tsx
// ✅ Correct — use the back button in any page component
function ProfilePage() {
  useBackButton();

  return <div>Profile Content</div>;
}
```

### 7.3. Back Button Behavior Rules

| Scenario | Behavior |
|---|---|
| User on main page | Back button hidden |
| User navigated to subpage | Back button visible |
| User clicks Back | Navigate to previous page |
| No history (direct link) | Close the Mini App |
| Complex forms with steps | Show back, confirm before leaving |

---

## 8. Main Button

### 8.1. Main Button Configuration

Use the MainButton for primary actions like "Submit", "Save", "Confirm".

```tsx
// ✅ Correct — Main Button hook
import { useEffect } from 'react';
import { useTelegramStore } from '@/features/telegram/hooks/useTelegramInit';

interface UseMainButtonOptions {
  text: string;
  onClick: () => void;
  isVisible?: boolean;
  isActive?: boolean;
  isProgress?: boolean;
  color?: string;
  textColor?: string;
}

export function useMainButton({
  text,
  onClick,
  isVisible = true,
  isActive = true,
  isProgress = false,
  color,
  textColor,
}: UseMainButtonOptions) {
  const webApp = useTelegramStore((state) => state.webApp);

  useEffect(() => {
    const tg = webApp;
    if (!tg) return;

    const btn = tg.MainButton;
    btn.setText(text);
    btn.setColor(color || tg.themeParams.button_color || '#2481cc');
    btn.setTextColor(textColor || tg.themeParams.button_text_color || '#ffffff');

    if (isVisible) btn.show();
    else btn.hide();

    if (isActive) btn.enable();
    else btn.disable();

    if (isProgress) btn.showProgress();
    else btn.hideProgress();

    const handleClick = () => onClick();
    btn.onClick(handleClick);

    return () => {
      btn.offClick(handleClick);
      btn.hide();
    };
  }, [webApp, text, isVisible, isActive, isProgress, color, textColor, onClick]);
}
```

### 8.2. Using the Main Button

```tsx
// ✅ Correct — Main Button usage
function SubmitForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isFormValid, setIsFormValid] = useState(false);

  const handleSubmit = useCallback(async () => {
    setIsSubmitting(true);
    try {
      // Submit logic
      await submitData();
      window.Telegram?.WebApp.close();
    } finally {
      setIsSubmitting(false);
    }
  }, []);

  useMainButton({
    text: 'Submit',
    onClick: handleSubmit,
    isVisible: true,
    isActive: isFormValid && !isSubmitting,
    isProgress: isSubmitting,
  });

  return (
    <form>
      {/* Form fields */}
    </form>
  );
}
```

### 8.3. Main Button States

| State | Visual | Behavior |
|---|---|---|
| Hidden | Not visible | `btn.hide()` |
| Active | Full color, clickable | `btn.enable()` |
| Disabled | Grayed out, not clickable | `btn.disable()` |
| Loading | Spinner shown, not clickable | `btn.showProgress()` |

### 8.4. Main Button Best Practices

- Always show the MainButton at the bottom of the screen.
- Disable the button while processing to prevent double-clicks.
- Show progress when performing async operations.
- Use consistent text: "Save", "Submit", "Confirm", "Continue".
- Close the app after successful final actions.

---

## 9. Haptic Feedback

### 9.1. Haptic Feedback Hook

Provide tactile feedback for user interactions.

```tsx
// ✅ Correct — Haptic Feedback hook
import { useCallback } from 'react';
import { useTelegramStore } from '@/features/telegram/hooks/useTelegramInit';

export function useHapticFeedback() {
  const webApp = useTelegramStore((state) => state.webApp);

  const impact = useCallback(
    (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft' = 'medium') => {
      webApp?.HapticFeedback.impactOccurred(style);
    },
    [webApp]
  );

  const notification = useCallback(
    (type: 'error' | 'success' | 'warning' = 'success') => {
      webApp?.HapticFeedback.notificationOccurred(type);
    },
    [webApp]
  );

  const selection = useCallback(() => {
    webApp?.HapticFeedback.selectionChanged();
  }, [webApp]);

  return { impact, notification, selection };
}
```

### 9.2. Usage Examples

```tsx
// ✅ Correct — using haptic feedback
function InteractiveButton() {
  const { impact, notification } = useHapticFeedback();

  const handleClick = () => {
    impact('light');        // Light tap feedback
    // action...
    notification('success'); // Success notification
  };

  const handleError = () => {
    notification('error');  // Error notification
  };

  const handleSelection = () => {
    selection();             // Selection changed feedback
  };

  return (
    <button
      onClick={handleClick}
      className="bg-tg-button text-tg-button-text rounded-lg px-6 py-3"
    >
      Tap me
    </button>
  );
}
```

### 9.3. When to Use Haptic Feedback

| Action | Feedback Type | Style |
|---|---|---|
| Button press | `impactOccurred` | `light` |
| Toggle switch | `impactOccurred` | `medium` |
| Submit success | `notificationOccurred` | `success` |
| Submit error | `notificationOccurred` | `error` |
| Warning | `notificationOccurred` | `warning` |
| Item selection | `selectionChanged` | — |
| Long press | `impactOccurred` | `heavy` |

- **Do not overuse**: haptic feedback should be meaningful, not noisy.
- **No haptic on page transitions** — only on user-initiated actions.

---

## 10. Android Adaptation

### 10.1. Platform Detection

Detect Android to apply platform-specific adjustments.

```tsx
// ✅ Correct — platform detection
const platform = useTelegramStore((state) => state.platform);
const isAndroid = platform === 'android';

// Platform information from Telegram:
// 'android' — Android
// 'ios' — iOS
// 'macos' — macOS
// 'web' — Web (Telegram Web)
// 'unknown' — unknown platform
```

### 10.2. Android-Specific Adjustments

```tsx
// ✅ Correct — Android-specific styles
function AndroidAdaptiveContainer({ children }: { children: React.ReactNode }) {
  const platform = useTelegramStore((state) => state.platform);
  const isAndroid = platform === 'android';

  return (
    <div
      className={cn(
        'min-h-screen bg-tg-bg',
        isAndroid && 'pb-16' // Extra bottom padding for Android navigation bar
      )}
    >
      {children}
    </div>
  );
}
```

### 10.3. Android Status Bar

Android status bar behaves differently. Handle it properly.

```tsx
// ✅ Correct — Android status bar handling
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  // On Android, the status bar is part of the app
  // Set header color to match the app background
  tg.setHeaderColor(tg.themeParams.bg_color || '#ffffff');
  tg.setBackgroundColor(tg.themeParams.bg_color || '#ffffff');
}, []);
```

### 10.4. Android Back Button

Android has a system back button. Handle it in coordination with Telegram's back button.

```tsx
// ✅ Correct — handle Android system back button
useEffect(() => {
  const handlePopState = () => {
    const tg = window.Telegram?.WebApp;
    if (tg && useNavigationStore.getState().history.length <= 1) {
      // On main page — let Telegram handle the back
      return;
    }
  };

  window.addEventListener('popstate', handlePopState);
  return () => window.removeEventListener('popstate', handlePopState);
}, []);
```

### 10.5. Android Material Design

On Android, use Material Design-inspired styles for a native feel.

```tsx
// ✅ Correct — Android Material ripple effect simulation
function AndroidButton({ children, onClick }: ButtonProps) {
  const platform = useTelegramStore((state) => state.platform);
  const isAndroid = platform === 'android';

  return (
    <button
      onClick={onClick}
      className={cn(
        'rounded-lg px-6 py-3 font-medium transition-colors',
        'bg-tg-button text-tg-button-text',
        isAndroid ? 'active:opacity-80' : 'active:opacity-70',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-tg-link'
      )}
    >
      {children}
    </button>
  );
}
```

---

## 11. iOS Adaptation

### 11.1. Platform Detection

```tsx
// ✅ Correct — iOS detection
const platform = useTelegramStore((state) => state.platform);
const isIOS = platform === 'ios';
```

### 11.2. iOS Safe Area

iOS has a notch and home indicator that must be accounted for.

```tsx
// ✅ Correct — iOS-specific safe area
function iOSContainer({ children }: { children: React.ReactNode }) {
  const platform = useTelegramStore((state) => state.platform);
  const isIOS = platform === 'ios';

  return (
    <div
      className={cn(
        'min-h-screen bg-tg-bg',
        isIOS && 'pt-[env(safe-area-inset-top)]',
        isIOS && 'pb-[env(safe-area-inset-bottom)]'
      )}
    >
      {children}
    </div>
  );
}
```

### 11.3. iOS Swipe Gestures

iOS users expect swipe-back gestures. Do not disable them.

```tsx
// ✅ Correct — preserve iOS swipe-back gesture
// Do NOT prevent default touch/mouse events on the body
// Do NOT set overscroll-behavior: none on the body on iOS
// Let the system handle swipe-back natively
```

### 11.4. iOS Keyboard Handling

iOS keyboard behavior differs from Android.

```tsx
// ✅ Correct — iOS keyboard handling
export function useIOSKeyboard() {
  const platform = useTelegramStore((state) => state.platform);
  const isIOS = platform === 'ios';
  const { isKeyboardOpen, keyboardHeight } = useKeyboard();

  // On iOS, the keyboard pushes the viewport up
  // On Android, the keyboard overlaps the viewport
  const adjustedHeight = isIOS ? 0 : keyboardHeight;

  return {
    isKeyboardOpen,
    keyboardHeight: adjustedHeight,
    isIOS,
  };
}
```

### 11.5. iOS Native Scrolling

iOS has native smooth scrolling. Leverage it.

```tsx
// ✅ Correct — iOS native scrolling
<div
  className={cn(
    'overflow-y-auto',
    '-webkit-overflow-scrolling: touch' // Native smooth scroll on iOS
  )}
>
  {children}
</div>
```

---

## 12. Performance Optimization

### 12.1. Minimize Re-renders

Telegram Mini Apps run in a WebView with limited resources. Optimize rendering.

```tsx
// ✅ Correct — memoize components that render frequently
const UserListItem = React.memo(function UserListItem({ user }: { user: User }) {
  return (
    <div className="p-4 bg-tg-section-bg rounded-lg mb-2">
      <p className="text-tg-text">{user.name}</p>
    </div>
  );
});

// ✅ Correct — use useCallback for event handlers passed to children
const handleItemClick = useCallback((id: string) => {
  navigate(`/item/${id}`);
}, [navigate]);
```

### 12.2. Bundle Size Optimization

Telegram Mini Apps must load fast. Keep the bundle small.

```tsx
// ✅ Correct — lazy load pages
const HomePage = React.lazy(() => import('@/pages/Home/HomePage'));
const ProfilePage = React.lazy(() => import('@/pages/Profile/ProfilePage'));

// ✅ Correct — use Suspense
function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
```

### 12.3. Image Optimization

Images should be optimized for mobile networks.

```tsx
// ✅ Correct — optimized image component
function OptimizedImage({ src, alt }: { src: string; alt: string }) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      className="w-full h-auto"
      // Specify dimensions to prevent layout shift
      width={640}
      height={360}
    />
  );
}
```

### 12.4. Memory Management

Clean up resources when components unmount.

```tsx
// ✅ Correct — cleanup Telegram event listeners
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  const handler = () => { /* ... */ };

  tg.onEvent('viewportChanged', handler);

  return () => {
    tg.offEvent('viewportChanged', handler); // Always cleanup
  };
}, []);
```

### 12.5. Network Optimization

Reduce API calls and cache data effectively.

```tsx
// ✅ Correct — use TanStack Query with appropriate stale time
export function useUserData() {
  return useQuery({
    queryKey: ['user'],
    queryFn: () => fetchUser(),
    staleTime: 5 * 60 * 1000, // 5 minutes — user data rarely changes
    gcTime: 10 * 60 * 1000,   // Keep in cache for 10 minutes
  });
}
```

### 12.6. CSS Performance

Optimize CSS for smooth animations and transitions.

```tsx
// ✅ Correct — GPU-accelerated animations
<div
  className={cn(
    'transition-transform duration-300',
    'will-change-transform', // Hint the browser for GPU acceleration
    isOpen ? 'translate-x-0' : '-translate-x-full'
  )}
>
  Sidebar content
</div>

// ❌ Incorrect — animating layout properties triggers expensive reflows
<div
  className={cn(
    'transition-all duration-300',
    isOpen ? 'width: 300px' : 'width: 0'
  )}
>
  Sidebar content
</div>
```

### 12.7. Initial Load Speed

Optimize the first paint for a fast initial experience.

```tsx
// ✅ Correct — inline critical CSS and defer non-critical
// index.html
{`
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Critical CSS inlined for instant paint */
    body { margin: 0; background: var(--tg-bg-color, #fff); }
    .loading-screen { display: flex; align-items: center; justify-content: center; height: 100vh; }
  </style>
</head>
<body>
  <div id="root">
    <div class="loading-screen">
      <div class="spinner"></div>
    </div>
  </div>
  <script type="module" src="/src/main.tsx" defer></script>
</body>
</html>
`}
```

### 12.8. Performance Checklist

| Area | Action |
|---|---|
| Bundle | Lazy load pages, tree-shake unused imports |
| Images | Use modern formats (WebP), lazy loading |
| Re-renders | Memoize heavy components, use useCallback |
| API calls | Cache with TanStack Query, deduplicate requests |
| Animations | Use `transform` and `opacity` only, `will-change` |
| Memory | Cleanup event listeners in useEffect return |
| CSS | Inline critical CSS, defer the rest |
| Fonts | Use system fonts or subset custom fonts |

---

## 13. Additional Telegram Mini App Rules

### 13.1. Sending Data to Telegram

Use `sendData` to send JSON data back to the bot.

```tsx
// ✅ Correct — send data to Telegram bot
function handleSubmit(data: Record<string, unknown>) {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  tg.sendData(JSON.stringify(data));
  tg.close(); // Close the Mini App after sending data
}
```

### 13.2. Closing Confirmation

Enable closing confirmation to prevent accidental exits.

```tsx
// ✅ Correct — enable closing confirmation when there's unsaved data
useEffect(() => {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  if (hasUnsavedChanges) {
    tg.enableClosingConfirmation();
  } else {
    tg.disableClosingConfirmation();
  }
}, [hasUnsavedChanges]);
```

### 13.3. Popups

Use Telegram's native popup instead of custom modals for system-level messages.

```tsx
// ✅ Correct — use Telegram popup
export function showTelegramPopup(
  title: string,
  message: string,
  buttons: Array<{ id: string; type?: 'ok' | 'close' | 'cancel' | 'destructive'; text: string }> = []
) {
  const tg = window.Telegram?.WebApp;
  if (!tg) return;

  tg.showPopup(
    { title, message, buttons },
    (buttonId) => {
      // Handle button press
      console.log('Popup button pressed:', buttonId);
    }
  );
}

// ❌ Incorrect — custom modal overlay for system messages
// Use Telegram popup instead for better UX and smaller bundle
```

### 13.4. Version Checking

Check the Telegram WebApp version before using newer APIs.

```tsx
// ✅ Correct — version check
export function isVersionAtLeast(version: string): boolean {
  const tg = window.Telegram?.WebApp;
  if (!tg) return false;

  const current = tg.version.split('.').map(Number);
  const required = version.split('.').map(Number);

  for (let i = 0; i < Math.max(current.length, required.length); i++) {
    const cur = current[i] || 0;
    const req = required[i] || 0;
    if (cur < req) return false;
    if (cur > req) return true;
  }
  return true;
}

// Usage
if (isVersionAtLeast('6.9')) {
  tg.HapticFeedback.impactOccurred('medium');
}
```

### 13.5. Error Handling

Gracefully handle cases where Telegram WebApp is not available (e.g., local development).

```tsx
// ✅ Correct — safe Telegram access
export function getTelegram(): TelegramWebApp | null {
  return window.Telegram?.WebApp ?? null;
}

// ✅ Correct — check availability before calling Telegram APIs
function useTelegramSafe() {
  const webApp = useTelegramStore((state) => state.webApp);
  const isAvailable = !!webApp;

  return { webApp, isAvailable };
}
```

---

> **Important**: The AI model must strictly follow these guidelines when generating code for Telegram Mini Apps.  
> Every Telegram-specific interaction must use the WebApp API through the provided hooks and stores.  
> Always respect the user's theme preference and platform-specific behavior.
