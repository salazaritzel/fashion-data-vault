import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import Image from 'next/image';
import FDVLogo from './ui/fdv-logo';

// I need to add the full bleed image here
export default function Page() {
  return (
    // This is the <main> element for the hp
    <main className = "relative flex min-h-screen flex-col">
      {/* This main <div> is for the hero section.*/}
        {/* <div className = "relative mt-4 flex flex-col gap-4 md:flex-row"> */}
        
        {/* <div className = "relative flex-1"> */}
        {/* Full BleedBackground Image */}
        <Image 
          alt = "Runway image displaying holographic charts."
          src = "/fdv-hero.jpg"
          quality = {100}
          fill
          style = {{
            objectFit: 'cover'
          }}
          sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          preload
        />

        {/* Fashion Data Vault Logo */}
        <div className = "relative z-10 px-8 pt-8">
          <Link href = "/">
            <FDVLogo />
          </Link>
        </div>

        <div className = "relative z-10 flex flex-col px-6 py-10 md:w-2/5 md:px-20">                   
          {/* CTA Text */}
          <div className = "font-mono flex flex-col gap-1 py-5 text-2xl md:text-3xl lg:text-5xl text-paper md:leading-normal">    
            <span>Fashion Intelligence.</span>
            <span>Powered by Data.</span>
          </div>

          {/* Dashboard Button */}
          <div className = "w-fit">
            <Link href = "/dashboard" className = "font-sans glass flex flex-row items-center self-start rounded-lg gap-5 px-4 py-3 text-sm text-paper hover:bg-white/20 whitespace-nowrap">
             <span>Explore the Vault </span>
             <ArrowRightIcon className = "w-4 shrink-0" />
            </Link>
          </div>
        </div>
        
      {/* </div>  */}

      {/* <div className = "absolute flex flex-col px-6 py-10 md:w-2/5 md:px-20">
      What is FDV? LOREM IPSUM DOLOR SIT AMET
      </div> */}
    </main> // This closing </main> ends the main of the entire page.
  );
}