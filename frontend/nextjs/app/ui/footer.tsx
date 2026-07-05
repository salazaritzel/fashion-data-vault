import Link from "next/link";
import Image from "next/image";
export default function PageFooter() {

    const socialLinks = [
        { label: "Instagram", icon: "instagram",  href: "https://instagram.com/fashiondatavault/" },
        { label: "GitHub", icon: "github", href: "https://github.com/salazaritzel" },
        // { label: "LinkedIn", icon: "linkedin", href: "https://linkedin.com/in/itzel-salazar" },
        { label: "Substack", icon: "substack", href: "https://substack.com/@fashiondatavault" },
      ];

    const currentYear = new Date().getFullYear();

    return (
        <footer className = "bg-neutral text-neutral-content px-10 py-10 md:px-20">
            <div className = "flex flex-row md:flex-row items-center justify-between gap-4">
                {/* Copyright Text */}
                <p className="font-mono text-ink text-sm">
                    <span className = "sm:hidden">© {currentYear} FDV</span>
                    <span className = "hidden sm:inline">© {currentYear} Fashion Data Vault</span>
                </p>
                
                {/* Contact Links */}
                <nav className = "flex gap-4">
                    {socialLinks.map((social) => (
                        <Link key = {social.icon} href = {social.href} aria-label = {social.label}>
                            <Image 
                                alt = {social.label}
                                src = {`/icons/${social.icon}.png`}
                                width = {25}
                                height = {25}
                            />
                        </Link>
                    ))}
                </nav>
            </div>
        </footer>
    );
}