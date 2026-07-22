import { CardSkeleton } from "../skeletons";

export default function ReadingRoom() {
      return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            Reading Room
        </h2>

        <p className = "font-mono italic text-ink/85 mb-8">
            A collection of research papers, industry reports, whitepapers, books and articles shaping the future of fashion.
        </p>
        
        {/* Above is placeholder text. We'll be adding cards here with actual content. */}
        {/* <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"></div> */}

    </div>
    );
  }