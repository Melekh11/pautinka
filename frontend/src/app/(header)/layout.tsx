import styles from "../page.module.scss";
import entStyles from "../entities.module.scss";
import Image from 'next/image';
import Link from 'next/link';


export default function HeaderLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <header className={`${styles.header} ${entStyles.flex_between}`}>
          <div className={`${entStyles.flex_align} ${entStyles.gap_s}`}>
            <Image
              src="icon.svg"
              alt="logo"
              width={37}
              height={37}
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
          {children}
        </>
  )
}