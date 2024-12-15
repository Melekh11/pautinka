'use client'
import { useState } from "react";
import styles from "./page.module.scss";
import entStyles from "../entities.module.scss";
import { Switcher } from "../ui/Switcher/Switcher";
import { Form } from "../ui/Form/Form";
import { Input } from "../ui/Form/Input/Input";



export default function RegisterPage() {
  const switcherValues = ["Телефон", "Почта"];
  const [ isPhoneType, setPhoneType ] = useState<boolean>(true);
  const phoneInput = <Input img={"./phone.svg"} placeholder="phone"/>;
  const emailInput = <Input img={"./email.svg"} placeholder="email"/>;
  return (
    <div className={styles.form_container}>

      <div className={`${styles.circle} ${styles.circle_1}`}/>
      <div className={`${styles.circle} ${styles.circle_2}`}/>

      <Form
        title="Регистрация"
      >
        <Switcher
          values={switcherValues}
          setNewValue={()=>{setPhoneType(!isPhoneType)}}
        />
        { isPhoneType && phoneInput }
        { !isPhoneType && emailInput }
        <Input img={"./user.svg"} placeholder="фамилия"/>
        <Input img={"./user.svg"} placeholder="имя"/>
        <Input img={"./user.svg"} placeholder="отчество"/>
        <Input img={"./key.svg"} placeholder="пароль"/>
        <Input img={"./key.svg"} placeholder="повт пароль"/>

        <div className={styles.data_contract_text}>Fill in the fields below to set up your new networking profile. Tell us a bit about yourself to help others connect with you.</div>

        <div className={entStyles.flex_start}>
          <input type="checkbox"/>
          <label className={styles.data_contract_text}>By clicking register, you agree to our terms of service and privacy policy.</label>
        </div>
      </Form>
    </div>
  );
}