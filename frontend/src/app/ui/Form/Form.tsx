import { FormType } from "./types";
import styles from "./style.module.scss";
import entStyles from "../../entities.module.scss";
import Image from "next/image";

export const Form = function({
  action,
  className,
  title,
  children,
  isSubmitLoading,
}: FormType) {
  return (
    <form
      action={action}
      className={`${styles.form} ${className}`}
    >
      <h1>{title}</h1>
      {children}

      <div 
        style={{
          width: "110px",
          alignSelf: "center",
        }}
        className={`${entStyles.flex_align}`}
      >
        <button
          type="submit"
          disabled={isSubmitLoading}
          className={entStyles.button}
        >Ввод</button>
        <div
          style={{
            width: "30px",
            height: "30px",
            borderRadius: "50%",
            backgroundColor: "white",
            display: "flex",
            alignItems: "center",
          }}
        >
          <Image
            style={{
              width: "auto",
              alignSelf: "center",
              verticalAlign: "bottom",
              margin: "auto",
            }}
            height={20}
            width={20}
            alt={"next"}
            src={"./go.svg"}
          />
        </div>
      </div>

    </form>
  )
} 