import '@/app/ui/global.css';
import { montserrat } from '@/app/ui/fonts';
// import { courier_prime } from '@/app/ui/fonts';
// import { cutive_mono } from '@/app/ui/fonts';
// import { pinyon_script } from '@/app/ui/fonts';
import { Metadata } from 'next';
 
// Metadata details, for SEO purposes
export const metadata: Metadata = {
  title: {
    template: '%s | Acme Dashboard',
    default: 'Acme Dashboard',
  },
  description: 'The official Next.js Learn Dashboard built with App Router.',
  metadataBase: new URL('https://next-learn-dashboard.vercel.sh'),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${montserrat.className} antialiased`}>{children}</body>
    </html>
  );
}
