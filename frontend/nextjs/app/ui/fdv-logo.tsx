import Image from 'next/image';
import clsx from 'clsx';

export default function FDVLogo({ textColor = 'text-ink' }: { textColor?: string }) {
  return (
    <>
    {/* Desktop Logo */}
    {/* <div className="hidden sm:flex items-center"> */} {/* revert to this when i have the new svg logo */}
    {/* <div className = "items-center"> */}
    {/* <p className = "font-display text-[28px] sm:text-[36px] md:text-[44px] leading-none text-paper"> */}
    {/* Trying to fix mobile spacing issues. */}
    <div className = "flex justify-start">
      {/* <p className="font-display text-[28px] sm:text-[36px] md:text-[44px] leading-none text-paper text-left"> */}
      <p className = {clsx('font-display text-[28px] sm:text-[36px] md:text-[44px] leading-none text-left', textColor)}>
        Fashion Data Vault
      </p>
    </div>

    {/* Logo needs to be svg. Add the new one. */}
     {/* Mobile Logo */}
      {/* <div className = "flex sm:hidden">
        <Image
          src = "/fdv-mono.png"
          alt = "Fashion Data Vault Logo"
          width = {120}
          height = {120}
          preload
        />
      </div> */}
    </>
  );
}
