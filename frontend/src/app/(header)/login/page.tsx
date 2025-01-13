'use client'
import { useState } from "react";
import styles from "./page.module.scss";
import entStyles from "../../entities.module.scss";
import { Switcher } from "../../ui/Switcher/Switcher";
import { Form } from "../../ui/Form/Form";
import { Input } from "../../ui/Form/Input/Input";
import { useActionState } from 'react';
import Link from "next/link";
import { loginAction } from "../../actions/auth";


export default function LoginPage() {
  const switcherValues = ["Телефон", "Почта"];
  const [ isPhoneType, setPhoneType ] = useState<boolean>(true);

  const phoneInput = <Input img={"./phone.svg"} placeholder="phone" name="phone"/>;
  const emailInput = <Input img={"./email.svg"} placeholder="email" name="email"/>;

  const [state, formAction, isPending] = useActionState(loginAction, {errors: []});

  return (
    <div className={styles.form_container}>

      <div className={`${styles.circle} ${styles.circle_1}`}/>
       <div className={`${styles.circle} ${styles.circle_2}`}/>
       <Link className={styles.nav_link} href={"/register"}>зарегистрироваться</Link>

      <Form
        title="Войти"
        method="post"
        action={formAction}
        isSubmitLoading={isPending}
      >
        <Switcher
          values={switcherValues}
          setNewValue={()=>{setPhoneType(!isPhoneType)}}
        />
        { isPhoneType && phoneInput }
        { !isPhoneType && emailInput }
        <Input
          id={"firstPassword"}
          type="password"
          img={"./key.svg"}
          placeholder="пароль"
          name={"password"}
        />

        <div className={styles.data_contract_text}>Fill in the fields below to set up your new networking profile. Tell us a bit about yourself to help others connect with you.</div>
        <div className={entStyles.flex_start}>
          <input type="checkbox"/>
          <label className={styles.data_contract_text}>By clicking register, you agree to our terms of service and privacy policy.</label>
        </div>

        {state.errors.map((err, id) => 
          <p key={id}>{err}</p>
        )}
      </Form>
    </div>
  );
}