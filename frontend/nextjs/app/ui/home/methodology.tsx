import Image from 'next/image';
import { ArrowLeft, ArrowBigRight } from 'lucide-react';
// I want that grey bg seen as loading from the skeleton?
export default function Methodology() {
  return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            Methodology
        </h2>

        {/* --- Desktop View --- */}
        <div className = "hidden md:flex items-center">

            {/* Step 1 - RSS feed */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                RSS Feed
              </p>
              <div className = "relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Stack of magazinez"
                  src = "/fashion/magazines.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>
            
            {/* For the curved lines, use SVG. */}
            <div className = "flex items-center self-center">
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
              <div className="w-8 border-t border-blue-300" />
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
            </div>
            
            {/* Step 2 - Database */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                Database
              </p>
              <div className="relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Image of silver database."
                  src = "/fashion/database.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>
            
            <div className = "flex items-center self-center">
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
              <div className="w-8 border-t border-blue-300" />
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
            </div>
            
            {/* Step 3 - NLP analysis */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                NLP Analysis
              </p>
              <div className="relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Flowing data"
                  src = "/fashion/data.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>
            
            <div className = "flex items-center self-center">
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
              <div className="w-8 border-t border-blue-300" />
              <div className="w-0.5 h-0.5 rounded-full bg-blue-300 shrink-0" />
            </div>
            
            {/* Step 4 - Trend output */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                Trend Output
              </p>
              <div className="relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Two women posing"
                  src = "/fashion/trends.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>
            

        </div>

        {/* --- Mobile View --- */}
        <div className = "flex md:hidden flex-col">
        
            {/* Step 1 - RSS feed */}
            <div  className = "self-start">
              <p className = "font-mono text-ink">
                RSS Feed
              </p>
              {/* The rss feed needs to change*/}
              <div className = "relative w-40 h-52 rounded-md overflow-hidden shrink-0">
                <Image
                  alt = "Stack of magazines"
                  src = "/fashion/magazines.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>
            
            {/* <div className="flex-1 h-px bg-blue-300" /> Connector line */}

            {/* Step 2 - Database */}
            <div className = "-mt-16 self-end">
              <p className = "font-mono text-ink text-end">
                Database
              </p>
              <div className = "relative w-40 h-52 rounded-md overflow-hidden shrink-0">
                <Image 
                  alt = "Image of silver database."
                  src = "/fashion/database.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>

            {/* Step 3 - NLP analysis */}
            <div className = "-mt-16 self-start">
              <p className = "font-mono text-ink">
                NLP Analysis
              </p>
              <div className = "relative w-40 h-52 rounded-md overflow-hidden shrink-0">
                <Image 
                  alt = "Flowing data"
                  src = "/fashion/data.jpg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                />
              </div>
            </div>

            {/* <div className="flex-1 h-px bg-blue-300" /> Connector line */}

            {/* Step 4 - Trend output */}
            <div className = "-mt-16 self-end">
                <p className = "font-mono text-ink text-end">
                   Trend Output
                </p>
                <div className = "relative w-40 h-52 rounded-md overflow-hidden shrink-0">
                    <Image 
                    alt = "Two women posing"
                    src = "/fashion/trends.jpg"
                    fill
                    style = {{
                        objectFit: 'cover'
                    }}
                    />
                </div>
            </div>
        </div>

    </div>
    );
}