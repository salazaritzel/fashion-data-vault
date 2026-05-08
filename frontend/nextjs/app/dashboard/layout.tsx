import SideNav from '@/app/ui/dashboard/sidenav';
 
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="w-full flex-none md:w-64">
        <SideNav /> {/* any components that are imported will be part of the layout */}
      </div>
      <div className="flex-grow p-6 md:overflow-y-auto md:p-12">
        {children} {/* layout component receives a children prop 
                    (can be a page or a layout, in this case the page.tsx 
                    inside /dashboard will be nested inside layout )*/}
      </div>
    </div>
  );
}