import { CardSkeleton } from "../skeletons";

export default function CompaniesToWatch() {
  return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            Companies to Watch
        </h2>

        <p className = "font-mono text-xs text-ink mb-8">
           A curated directory of companies driving innovation across fashion technology, manufacturing, materials, retail, and sustainability.
        </p>
        
        {/* Above is placeholder text. We'll be adding cards here with actual content. */}
        {/* <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"></div> */}

    </div>
    );
  }