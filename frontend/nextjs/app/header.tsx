import FDVLogo from '@/app/ui/fdv-logo';
import Link from 'next/link';

export default function Header() {
    return (
        // stickky until i have black background transition from white to black text
        <header className="sticky top-0 z-50 px-8 py-8 e"> {/* sticky unsure */}
            <Link href="/">
                <FDVLogo />
            </Link>
        </header>
    );
}