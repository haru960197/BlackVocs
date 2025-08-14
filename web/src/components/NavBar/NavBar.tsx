'use client';

import { ThemeContext } from '@/context/ThemeContext';
import { useContext } from 'react';
import { BiMoon, BiSun } from 'react-icons/bi';
import { SideDrawer } from '../SideDrawer';
import { UserButton } from './UserButton';

export const NavBar = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <div className="navbar bg-base-100 shadow-sm">
      <div className="flex-none">
        <SideDrawer />
      </div>
      <div className="flex-1">
        <a className="btn btn-ghost text-xl">BlackVocs</a>
      </div>
      <div className="flex-none flex gap-2">
        <UserButton />

        <button className="btn btn-ghost rounded-full p-2" onClick={toggleTheme}>
          {theme === 'light' ? <BiSun className="w-6 h-6" /> : <BiMoon className="w-6 h-6" />}
        </button>

        <button className="btn btn-square btn-ghost">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="inline-block h-5 w-5 stroke-current"
          >
            {' '}
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
            ></path>{' '}
          </svg>
        </button>
      </div>
    </div>
  );
};
