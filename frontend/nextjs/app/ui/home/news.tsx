import { CardSkeleton } from "../skeletons";

export default function Headlines() {
 return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            In the Headlines
        </h2>

        <p className = "font-monoitalic text-ink mb-8">
            The latest funding rounds, product launches, partnerships, acquisitions, and major industry developments.
        </p>
                
        {/* Above is placeholder text. We'll be adding cards here with actual content. */}
        {/* <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"></div> */}

    </div>
    );
  }  