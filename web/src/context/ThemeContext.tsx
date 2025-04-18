'use client';

import { Theme, themes } from '@/constant/theme';
import { createContext, useEffect, useState } from 'react';

export const ThemeContext = createContext<{
  theme: Theme;
  toggleTheme: () => void;
}>({
  theme: themes[0],
  toggleTheme: () => {},
});

export const ThemeProvider = ({ children }: React.PropsWithChildren) => {
  const [theme, setTheme] = useState<Theme>(themes[0]);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    const storageValue = localStorage.getItem('theme');
    const storedTheme: Theme =
      storageValue && themes.includes(storageValue as Theme) ? (storageValue as Theme) : themes[0];

    setTheme(storedTheme);
  }, []);

  if (!isMounted) {
    return <>Loading ...</>;
  }

  const toggleTheme = () => {
    const newTheme = theme === themes[0] ? themes[1] : themes[0];
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div data-theme={theme}>{children}</div>
    </ThemeContext.Provider>
  );
};
