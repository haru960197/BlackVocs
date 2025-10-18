'use client';

import { ThemeContext } from '@/context/ThemeContext';
import { useContext } from 'react';
import { BiMoon, BiSun, BiLogoGithub } from 'react-icons/bi';
import { SideDrawer } from '../SideDrawer';
import { UserButton } from './UserButton';
import Link from 'next/link';

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

        <Link href="https://github.com/haru960197/BlackVocs" target='_blank' className="btn btn-square btn-ghost">
          <BiLogoGithub className='w-6 h-6'/>
        </Link>
      </div>
    </div>
  );
};
