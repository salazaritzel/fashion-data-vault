import Hero from './ui/home/hero';
import Methodology  from './ui/home/methodology';
import Headlines from './ui/home/news';

export default function Page() {
  return (
    <main>
      <div className = "relative flex min-h-screen flex-col"> 
        <Hero/>
     
        {/* What is FDV? */}
        <div className = "px-10 py-10 md:px-20">
            <h2 className = "font-sans font-bold text-3xl text-ink float-left pr-6">
              What is FDV?
            </h2>   
            <p className = "font-mono text-ink">
              Fashion Data Vault is an open fashion intelligence platform built from a genuine obsession with fashion and a realization of how inaccessible, 
              scattered, and siloed the industry's data is. From supply chains and sustainability, to materials, culture, AI, and emerging technologies FDV aims to transform 
              that noise into structured knowledge for researchers, builders, industry professionals, and anyone curious about the intersection of fashion and technology.
            </p>
          </div>
        <Methodology />
        <Headlines />
      </div>
    </main>
  );
}