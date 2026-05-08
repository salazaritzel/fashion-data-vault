import { Card } from '@/app/ui/dashboard/cards';
import { montserrat } from '@/app/ui/fonts';
import { fetchTrends, fetchBrands, fetchMaterials, fetchSeasons } from '@/app/lib/data';
import EntityList from '@/app/ui/entities';

export default async function Page() {

  // Fetching the data for the dashboard. The imported functions are defined in the lib/data.ts file and they fetch data from the FastAPI backend.
  const trends = await fetchTrends(); 
  const brands = await fetchBrands();
  const materials = await fetchMaterials();
  const seasons = await fetchSeasons();
  
  return (
    <main>
      <h1 className={`${montserrat.className} mb-4 text-xl md:text-2xl`}>
        Trends Dashboard
      </h1>
      
      <EntityList data = {trends}/>
      <EntityList data = {brands}/>
      <EntityList data = {materials}/>
      <EntityList data = {seasons}/>
      
      <div className = "grid gap-6 sm:grid-cols-2 lg:grid-cols-5"></div> {/* For later use. */}
    </main>
  );
}

// *********************************************OLD ACME********************************************
// import { Card } from '@/app/ui/dashboard/cards';
// import RevenueChart from '@/app/ui/dashboard/revenue-chart';
// import LatestInvoices from '@/app/ui/dashboard/latest-invoices';
// import { montserrat } from '@/app/ui/fonts';
// import { fetchRevenue, fetchLatestInvoices, fetchCardData } from '@/app/lib/data';

// // The page is an async server component. This allows you to use await to fetch data.
// export default async function Page() {
//   const revenue = await fetchRevenue();
//   const latestInvoices = await fetchLatestInvoices();
//   // Destructuring the values returned from the function.
//   const {
//     numberOfInvoices,
//     numberOfCustomers,
//     totalPaidInvoices,
//     totalPendingInvoices
//   } = await fetchCardData();

//   return (
//     <main>
//       <h1 className={`${montserrat.className} mb-4 text-xl md:text-2xl`}>
//         Dashboard
//       </h1>
//       <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
//         <Card title="Collected" value={totalPaidInvoices} type="collected" />
//         <Card title="Pending" value={totalPendingInvoices} type="pending" />
//         <Card title="Total Invoices" value={numberOfInvoices} type="invoices" />
//         <Card
//           title="Total Customers"
//           value={numberOfCustomers}
//           type="customers"
//         />
//       </div>
//       <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
//         <RevenueChart revenue={revenue}  />
//         <LatestInvoices latestInvoices={latestInvoices} />

//         {/* ERROR HERE WHICH IS IRRELEVANT TO FDV BUT MAY BE USEFUL FOR FURTHER DEBUGGING */}
//       </div>
//     </main>
//   );
// }





