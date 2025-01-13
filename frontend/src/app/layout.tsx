import type { Metadata } from "next";
import { Sofia_Sans } from "next/font/google";

import "./globals.css";
import styles from "./page.module.scss";

const sofiaSans = Sofia_Sans({
  weight: ["100", "300", "400", "600", "900"],
  style: "normal",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Pautinka",
  description: "Your startup app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${sofiaSans.className}`}>
        <main className={styles.page}>
          {children}
        </main>
      </body>
    </html>
  );
}
