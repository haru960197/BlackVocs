'use client';

import { useAuth } from '@/context/AuthContext';
import clsx from 'clsx';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BiBookOpen, BiPencil, BiMenu } from 'react-icons/bi';

const links = [
  { name: 'Register Word', href: '/register-word', icon: BiPencil },
  { name: 'Word List', href: '/word-list', icon: BiBookOpen },
];

export const SideDrawer = () => {
  const pathName = usePathname();

  const { isLoggedIn } = useAuth();

  return (
    <div className="drawer">
      {/* ハンバーガーメニューボタン（ログイン状態でのみ展開） */}
      <input id="side-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content">
        <div
          className={!isLoggedIn ? 'tooltip tooltip-bottom tooltip-warning' : undefined}
          data-tip={!isLoggedIn && 'Login!'}
        >
          <label
            htmlFor="side-drawer"
            className={clsx(
              'btn btn-square btn-ghost drawer-button p-2',
              !isLoggedIn && 'btn-disabled'
            )}
          >
            <BiMenu className="w-6 h-6" />
          </label>
        </div>
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
