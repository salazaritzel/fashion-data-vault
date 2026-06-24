import Image from 'next/image';

export default function Methodology() {
  
  return (
    <div className = "px-10 py-10 md:px-20 overflow-hidden">
        
        <h2 className = "font-sans font-bold text-3xl text-ink mb-4">
            Methodology
        </h2>

        {/* --- Desktop View --- */}
        <div className = "hidden md:flex items-center">

            {/* Replace this one i dont like it. */}
            {/* Step 1 - RSS feed */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                RSS Feed
              </p>
              <div className = "relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Open magazine with model wearing a silver dress posing."
                  src = "/fashion/rss-new.png"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </div>
            </div>
            
            {/* For the curved lines, use SVG. */}
            <div className="w-8 border-t border-blue-300" />

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
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </div>
            </div>
            
            <div className="w-8 border-t border-blue-300" />
            
            {/* Step 3 - NLP analysis */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                NLP Analysis
              </p>
              <div className="relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Flowing data."
                  src = "/fashion/nlp.png"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </div>
            </div>
            
            <div className="w-8 border-t border-blue-300" />
            
            {/* Step 4 - Trend output */}
            <div className = "flex-1 min-w-0">
              <p className = "font-mono text-ink md:text-sm">
                Trend Output
              </p>
              <div className="relative aspect-[3/4] rounded-md overflow-hidden">
                <Image 
                  alt = "Stylish young woman posing dramatically in black outfit, wearing oversized sunglasses, showcasing a blend of fashion and confidence against a dark monochrome background."
                  src = "/fashion/trends.jpeg"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
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
                  alt = "Open magazine with model wearing a silver dress posing."
                  src = "/fashion/rss-new.png"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </div>
            </div>
            
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
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
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
                  alt = "Flowing data."
                  src = "/fashion/nlp.png"
                  fill
                  style = {{
                    objectFit: 'cover'
                  }}
                  // sizes = "(max-width: 768px) 160px, 25vw"
                  sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </div>
            </div>

            {/* Step 4 - Trend output */}
            <div className = "-mt-16 self-end">
                <p className = "font-mono text-ink text-end">
                   Trend Output
                </p>
                <div className = "relative w-40 h-52 rounded-md overflow-hidden shrink-0">
                    <Image 
                    alt = "Stylish young woman posing dramatically in black outfit, wearing oversized sunglasses, showcasing a blend of fashion and confidence against a dark monochrome background."
                    src = "/fashion/trends.jpeg"
                    fill
                    style = {{
                        objectFit: 'cover'
                    }}
                    // sizes = "(max-width: 768px) 160px, 25vw"
                    sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    />
                </div>
            </div>
        </div>

    </div>
    );
}