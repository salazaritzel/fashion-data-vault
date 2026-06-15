import Hero from './ui/home/hero';
import Methodology  from './ui/home/methodology';
import Headlines from './ui/home/news';
import ReadingRoom from './ui/home/reading-room';
import Substack from './ui/home/substack-preview';
import PageFooter from './ui/footer';

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
              Fashion Data Vault is a fashion intelligence platform built from a genuine obsession with fashion and a realization of how inaccessible, 
              scattered, and siloed the industry's data is. From AI and materials to supply chains and emerging technologies, FDV transforms
              that noise into structured knowledge for researchers, builders, industry professionals, and anyone curious about the intersection of fashion and technology.
            </p>
          </div>
        <Methodology />
        <Headlines />
        <ReadingRoom />
        <Substack />
        <hr className = "border-t border-gray-200 mx-6" />
        <PageFooter />
      </div>
    </main>
  );
}