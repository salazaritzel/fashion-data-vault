import '@/app/ui/global.css';
import { montserrat } from '@/app/ui/fonts';
import { Metadata } from 'next';
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

// Metadata details, for SEO purposes
export const metadata: Metadata = {
  title: {
    template: '%s | Fashion Data Vault',
    default: 'Fashion Data Vault',
  },
  description: 'Fashion trends and analytics platform.',
  metadataBase: new URL('https://fashiondatavault.com'),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)}>
      <body className={`${montserrat.className} antialiased`}>{children}</body>
    </html>
  );
}
