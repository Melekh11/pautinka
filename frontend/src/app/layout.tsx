import type { Metadata } from "next";
import { Sofia_Sans } from "next/font/google";
import Image from 'next/image';
import Link from 'next/link';

import "./globals.css";
import styles from "./page.module.scss";
import entStyles from "./entities.module.scss";

const sofiaSans = Sofia_Sans({
  weight: "400",
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
        <header className={`${styles.header} ${entStyles.flex_between}`}>
          <div className={`${entStyles.flex_align} ${entStyles.gap_s}`}>
            <Image
              src="icon.svg"
              alt="logo"
              width={37}
              height={37}
              // className={styles.header__title}
            />
            <h2 className={styles.header__title} >Паутинка</h2>
          </div >
          <Link 
            className={`
              ${entStyles.flex_align}
              ${entStyles.gap_s}
              ${styles.header_rounded}
              `
            }
            href="https://t.me/belkinasaraa">
          <Image
            src={"tg-icon.svg"}
            height={14}
            width={16}
            alt={"tg logo"}
          />
            <p className={styles.header__h2}>@pautinka_channel</p>
          </Link>
        </header>
        <main className={styles.page}>
          {children}
        </main>
      </body>
    </html>
  );
}
