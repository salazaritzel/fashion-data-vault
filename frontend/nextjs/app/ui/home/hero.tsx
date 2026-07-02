import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import Image from 'next/image';
import FDVLogo from 'app/ui/fdv-logo';

export default function Hero() {
  return (
    <div className = "relative flex min-h-screen flex-col overflow-hidden"> 
    
        {/* Background image */}
        {/* I love this, but I wish the charts became smaller as the screen size decreases. */}
        <Image 
          alt = "Runway image displaying holographic charts."
          src = "/main-img.jpg"
          quality = {75}
          fill
          style = {{
            objectFit: 'cover'
          }}
          sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          preload
        />
        
        <div className = "relative z-10 flex flex-col h-full px-4 sm:px-10 py-8">    
          {/* Fashion Data Vault logo */}
          <Link href = "/">
            <FDVLogo textColor = "text-paper" />
          </Link>

          {/* Hero text overlay */}
          <div className = "flex flex-col gap-6 mt-16 md:w-1/2 pl-4 sm:pl-0">
            <div className = "font-mono flex flex-col gap-1 text-2xl md:text-3xl lg:text-5xl text-paper">    
              <span>Fashion Intelligence.</span>
              <span>Powered by Data.</span>
            </div>

            {/* Hero dashboard button */}
            <Link href = "/dashboard" className = "font-sans glass flex items-center gap-4 self-start rounded-lg px-5 py-3 text-sm text-paper hover:bg-white/20 whitespace-nowrap">
              <span>Explore the Vault </span>
              <ArrowRightIcon className = "w-4 shrink-0" />
            </Link>
          </div>
        </div>

      </div>
  );
}