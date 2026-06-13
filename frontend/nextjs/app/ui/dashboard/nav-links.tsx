'use client';

import { ViewfinderCircleIcon, HomeIcon, ArrowTrendingUpIcon, Squares2X2Icon, GlobeAltIcon} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import Header from '@/app/ui/header';

const links = [ 
  { name: 'Home', href: '/', icon: HomeIcon },
  { name: 'Dashboard', href: '/dashboard', icon: ArrowTrendingUpIcon, },
  { name: 'In the News', href: '/dashboard/customers', icon: GlobeAltIcon },
  { name: 'Companies to Watch', href: '/dashboard/customers', icon: Squares2X2Icon },
  { name: 'Reading Room', href: '/dashboard/customers', icon: GlobeAltIcon },
  { name: 'Substack', href: '/dashboard/customers', icon: GlobeAltIcon },
  { name: 'Explore', href: '/dashboard', icon: ViewfinderCircleIcon },
];

export default function NavLinks() {
  const pathname = usePathname();
  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          <Link 
            key = {link.name}
            href = {link.href}
            className = {clsx('flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
            )}          
          
          >
            <LinkIcon className = "w-6" />
              <p className = "hidden md:block">{link.name}</p>
            </Link>
        );
      })}
    </>
  );
}
