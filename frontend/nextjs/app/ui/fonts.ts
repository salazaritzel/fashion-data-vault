import { Montserrat, Courier_Prime, Pinyon_Script } from 'next/font/google'; // Primary
// import { Courier_Prime } from 'next/font/google'; // Subtext
// import { Pinyon_Script } from 'next/font/google'; // Decorative

export const montserrat  = Montserrat({ 
    subsets: ['latin'] 
});
export const courier_prime  = Courier_Prime({ 
    subsets: ['latin'],
    weight: '400'
});
export const pinyon_script  = Pinyon_Script({
    subsets: ['latin'],
    weight: '400'
});

