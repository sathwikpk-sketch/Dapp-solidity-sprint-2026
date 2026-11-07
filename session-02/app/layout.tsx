import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'MessageBoard', description: 'A simple Sepolia MessageBoard demo' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
