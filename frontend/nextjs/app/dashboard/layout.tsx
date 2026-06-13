import SideNav from '@/app/ui/dashboard/sidenav';
 import Header from '../ui/header';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <div className = "flex h-screen flex-col md:flex-row md:overflow-hidden">
        {/* <div className="w-full flex-none md:w-64">
          <SideNav />
        </div> */}
        <div className = "flex-grow px-10 py-2 md:overflow-y-auto md:py-2">
          {children}
        </div>
      </div>
    </>
  );
}