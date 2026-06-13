import { Montserrat, Atkinson_Hyperlegible_Mono , Pinyon_Script } from 'next/font/google';

export const montserrat  = Montserrat({ 
    subsets: ['latin'],
    variable: '--font-sans',
});
export const atkinson_hyperlegible_mono = Atkinson_Hyperlegible_Mono({ 
    subsets: ['latin'],
    variable: '--font-mono',
});
export const pinyon_script  = Pinyon_Script({
    subsets: ['latin'],
    weight: '400',
    variable: '--font-display',
});

