'use client';

import { useAuth } from '@/context/AuthContext';
import clsx from 'clsx';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BiBookOpen, BiPencil } from 'react-icons/bi';

const links = [
  { name: 'Register Word', href: '/register-word', icon: BiPencil },
  { name: 'Word List', href: '/word-list', icon: BiBookOpen },
];

export const SideDrawer = () => {
  const pathName = usePathname();

  const { isLoggedIn } = useAuth();

  return (
    <div className="drawer">
      {/* ハンバーガーメニューボタン（ログイン状態での展開） */}
      <input id="side-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content">
        <label
          htmlFor='side-drawer'
          className={clsx(
            "btn btn-square btn-ghost drawer-button",
            !isLoggedIn && "btn-disabled"
          )}
        >
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
              d="M4 6h16M4 12h16M4 18h16"
            ></path>{' '}
          </svg>
        </label>
      </div>

      {/* ドロワー本体 */}
      <div className="drawer-side z-50">
        <label htmlFor="side-drawer" aria-label="close sidebar" className="drawer-overlay"></label>
        <div className="menu bg-base-200 text-base-content min-h-full w-80 p-4 flex flex-col gap-2">
          {/* body */}
          <div className="flex flex-1 flex-col gap-2">
            {links.map((link) => {
              const LinkIcon = link.icon;
              return (
                <Link
                  key={link.name}
                  href={link.href}
                  className={clsx(
                    'btn btn-soft justify-start items-center h-12',
                    pathName === link.href && 'text-accent'
                  )}
                >
                  <LinkIcon className="w-4 h-4" />
                  {link.name}
                </Link>
              );
            })}
          </div>

          {/* footer */}
          <div className="flex justify-end"></div>
        </div>
      </div>
    </div>
  );
};
