import Header from "../ui/header"
import { CardsSkeleton } from "../ui/skeletons"

export default function HeadlinesPage() {
  return (
    <>
     <Header />     
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            In the Headlines
        </h2>
        {/* temps testing */}
        <CardsSkeleton />

        <CardsSkeleton />
        <CardsSkeleton />
        <CardsSkeleton />
    </div>
    </>
)}