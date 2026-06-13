import FDVLogo from '@/app/ui/fdv-logo';
import Link from 'next/link';

export default function Header() {
    return (
        <header className = "sticky top-0 z-50 px-10 py-8 bg-paper">
            <Link href = "/">
                <FDVLogo />
            </Link>
        </header>
    );
}