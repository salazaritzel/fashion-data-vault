'use client';

import { UserGroupIcon, SwatchIcon, ViewfinderCircleIcon, HomeIcon, ArrowTrendingUpIcon, Squares2X2Icon, GlobeAltIcon} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

// Map of links to display in the side navigation.
// Depending on the size of the application, this would be stored in a database.
const links = [
  { name: 'Home', href: '/dashboard', icon: HomeIcon },
  { name: 'Trends', href: '/dashboard/invoices', icon: ArrowTrendingUpIcon, },
  { name: 'Brands', href: '/dashboard/customers', icon: GlobeAltIcon },
  { name: 'Seasons', href: '/dashboard/customers', icon: Squares2X2Icon },
  { name: 'Materials', href: '/dashboard/customers', icon: SwatchIcon },
  { name: 'Explore', href: '/dashboard/customers', icon: ViewfinderCircleIcon },
];

export default function NavLinks() {
  const pathname = usePathname();
  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          // replaced the <a> tag with <Link>
          <Link 
            key = {link.name}
            href = {link.href}
            className = {clsx('flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
            )}          
          
          >
            <LinkIcon className="w-6" />
              <p className="hidden md:block">{link.name}</p>
            </Link>
        );
      })}
    </>
  );
}
