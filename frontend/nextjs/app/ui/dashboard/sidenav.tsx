import NavLinks from '@/app/ui/dashboard/nav-links';

export default function SideNav() {
  return (
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
      </div>
  );
}
