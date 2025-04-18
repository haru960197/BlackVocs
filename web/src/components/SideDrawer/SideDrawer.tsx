'use client';

import Link from 'next/link';
import clsx from 'clsx';
import { usePathname } from 'next/navigation';
import { BiBookOpen, BiPencil } from 'react-icons/bi';

const links = [
  { name: 'Register Word', href: '/register-word', icon: BiPencil },
  { name: 'Word List', href: '/word-list', icon: BiBookOpen },
];

export const SideDrawer = () => {
  const pathName = usePathname();

  return (
    <div className="drawer">
      <input id="side-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content">
        <label htmlFor="side-drawer" className="btn btn-square btn-ghost drawer-button">
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
      <div className="drawer-side z-50">
        <label htmlFor="side-drawer" aria-label="close sidebar" className="drawer-overlay"></label>
        <div className="menu bg-base-200 text-base-content min-h-full w-80 p-4 flex flex-col gap-2">
          {links.map((link) => {
            const LinkIcon = link.icon;
            return (
              <Link
                key={link.name}
                href={link.href}
                className={clsx(
                  'flex h-[48px] items-center gap-2 rounded-md p-3 bg-info-content text-sm font-medium hover:bg-accent-content hover:text-accent md:flex-none md:justify-start md:p-2 md:px-3',
                  {
                    'bg-accent-content text-accent': pathName === link.href,
                  }
                )}
              >
                <LinkIcon className="w-6" />
                {link.name}
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};
