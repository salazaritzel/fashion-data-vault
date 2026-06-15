import { CardSkeleton } from "../skeletons";

export default function ReadingRoom() {
  return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            Reading Room
        </h2>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <p className = "font-style: italic">Coming Soon...</p>
        </div>
    </div>
    );
  }