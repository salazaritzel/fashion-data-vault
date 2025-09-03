import { GlobeAltIcon } from '@heroicons/react/24/outline';
import { pinyon_script } from '@/app/ui/fonts';
// import { lusitana } from '@/app/ui/fonts';
// Tutorial shows lusitana, I used pinyon_script.

export default function AcmeLogo() {
  return (
    <div className={`${pinyon_script.className} flex flex-row items-center leading-none text-black`}>
      {/* <GlobeAltIcon className="h-12 w-12 rotate-[15deg]" /> */}
      <p className="text-[44px]">Fashion Data Vault</p>
    </div>
  );
}
