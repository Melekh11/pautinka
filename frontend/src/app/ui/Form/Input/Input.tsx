import { InputType } from "./types";
import styles from "./style.module.scss";
import Image from "next/image";
import { useState, HTMLInputTypeAttribute, FormEvent } from "react";

export const Input = function({
  img,
  placeholder,
  onChange,
  label,
  type,
  id,
  name,
}: InputType) {
  const [ inputType, setInputType ] = useState<HTMLInputTypeAttribute>(type ?? "text");
  const imageElement = <Image
    height={24}
    width={24}
    alt={(placeholder?.slice(0, 3) + "..")}
    src={img}
  />
  return (
    <div className={`${styles.input_wrapper}`}>
      <div className={styles.input_image_container}>
        {imageElement}
      </div>
      <input
        id={id}
        name={name}
        type={inputType}
        placeholder={placeholder}
        className={styles.input} 
        onChange={(e: FormEvent<HTMLInputElement>) => {
          console.log("change");
          if (onChange) onChange(e.currentTarget.value);
        }}
      />
      {type === "password" &&
        <span
          className={styles.is_visible_label}
          onClick={ () => {setInputType((prev) => prev === "password" ? "text" : "password")} }
        >
          <Image height={20} width={20} alt="eye" src={"./closed-eye.svg"}/>
        </span>
      }
      <label className={styles.input_label} htmlFor={id}>{label}</label>
    </div>
  )
};