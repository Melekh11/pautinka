import { InputType } from "./types";
import styles from "./style.module.scss";
import Image from "next/image";

export const Input = function({
  img,
  placeholder,
  label,
  type,
  id,
}: InputType) {
  return (
    <div className={`${styles.input_wrapper}`}>
      <div className={styles.input_image_container}>
        <Image
          height={24}
          width={24}
          alt={(placeholder?.slice(0, 3) + "..")}
          src={img}
        />
      </div>
      <input
        id={id}
        type={type}
        placeholder={placeholder}
        className={styles.input} 
      />
      <label className={styles.input_label} htmlFor={id}>{label}</label>
    </div>
  )
};