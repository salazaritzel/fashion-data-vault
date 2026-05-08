'use client'; // This is a Client Component, which means you can use event listeners and hooks.

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { SearchParams } from 'next/dist/server/request/search-params';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useDebouncedCallback } from 'use-debounce';

export default function Search({ placeholder }: { placeholder: string }) {
  
  const searchParams = useSearchParams();
  const pathname = usePathname(); // ${pathname} is the current path, in your case, "/dashboard/invoices"
                                  // As the user types into the search bar, params.toString() translates this input into a URL-friendly format.
  const { replace } = useRouter(); 
  
  const handleSearch = useDebouncedCallback((term) => {
    console.log(`Searching... ${term}`); 
    const params = new URLSearchParams(searchParams);
    params.set('page', '1');
    
    if (term) {
      params.set('query', term);
    } else {
      params.delete('query');
    }
    //  updates the URL with the user's search data. 
    // For example, /dashboard/invoices?query=lee if
    // the user searches for "Lee".
    // The URL is updated without reloading the page.
    replace(`${pathname}?${params.toString()}`);
  }, 300);
  
  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <input
        className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
        placeholder={placeholder}
        onChange={(e) => {
          handleSearch(e.target.value);
        }}
        defaultValue={searchParams.get('query')?.toString()} // ensures input field is in sync w the URL and will be populated when sharing
      />
      <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
    </div>
  );
}
