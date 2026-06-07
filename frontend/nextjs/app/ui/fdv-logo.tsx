import Image from 'next/image';

export default function FDVLogo() {
  return (
    <>
    {/* Desktop Logo */}
    {/* <div className="hidden sm:flex items-center"> */} {/* revert to this when i have the new svg logo */}
    <div className="items-center">
      <p className = "font-display text-[44px] leading-none text-paper">
        Fashion Data Vault
      </p>
    </div>

    {/* Logo needs to be svg. Add the new one. */}
     {/* Mobile Logo */}
      {/* <div className="flex sm:hidden">
        <Image
          src = "/fdv-monogram.png"
          alt = "Fashion Data Vault Logo"
          width = {120}
          height = {120}
          preload
        />
      </div> */}
    </>
  );
}
