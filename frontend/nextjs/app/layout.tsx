import Header from '@/app/header';
import '@/app/ui/global.css';
import { montserrat, pinyon_script, atkinson_hyperlegible_mono } from '@/app/ui/fonts';
import { Metadata } from 'next';
import { cn } from "@/lib/utils";

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
      <html lang = "en" className = {cn( 
          montserrat.variable, pinyon_script.variable, atkinson_hyperlegible_mono.variable, "font-sans"
      )}
      >
      <body>
        {/* <Header /> */}
        <main>
          {children}
        </main>
      </body>
    </html>
  );
}
