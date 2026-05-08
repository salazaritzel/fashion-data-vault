import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { montserrat } from './ui/fonts';
import Image from 'next/image';

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col p-6">
      {/* menu and logo area */}
      <div className="flex h-20 shrink-0 items-end rounded-lg p-4 md:h-20"> {/* removed bg-blue-500, changed md:52 to md:20 stays in place */}
        <AcmeLogo />
      </div>
      <div className="mt-4 flex grow flex-col gap-4 md:flex-row">
        <div className="flex flex-col justify-center gap-6 rounded-lg px-6 py-10 md:w-2/5 md:px-20">
          {/* <div className="relative w-0 h-0 border-l-[15px] border-r-[15px] border-b-[26px] border-l-transparent border-r-transparent border-b-black"/> */}
          <p className={`${montserrat.className} text-xl text-gray-800 md:text-2xl md:leading-normal`}>
            <strong>Welcome to the Fashion Data Vault.</strong> Unlocking fashion insights through intelligent data collection, trend forecasting, and visual storytelling.{' '}
            {/* <a href="https://nextjs.org/learn/" className="text-blue-500">
              Analyzer
            </a> */}
          </p>
          <Link
            href="/login"
            className="flex items-center gap-5 self-start rounded-lg bg-burgundy-500 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-burgundy-400 md:text-base"
          >
            <span>Learn More</span> <ArrowRightIcon className="w-5 md:w-6" />
          </Link>
        </div>
        <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12">
          {/* Add Hero Images Here */}
          <Image
            src="/hero-desktop.png"
            width={1000}
            height={760}
            className="hidden md:block" // removes img from DOM on mobile, but md:block to show on desktop
            alt="Screenshots of the dashboard project showing desktop version"
          />
          <Image
            src="/hero-mobile.png"
            width={560}
            height={620}
            className="block md:hidden" // removes img from DOM on mobile, but md:block to show on desktop
            alt="Screenshots of the dashboard project showing mobile version"
          />
        </div>
      </div>
    </main>
  );
}
