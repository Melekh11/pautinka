'use client'
import { useState, useActionState } from "react";
import styles from "./page.module.scss";
import entStyles from "../../entities.module.scss";
import { Switcher } from "../../ui/Switcher/Switcher";
import { Form } from "../../ui/Form/Form";
import { Input } from "../../ui/Form/Input/Input";
import Link from "next/link";
import { registerAction } from "../../actions/auth";
// import { register } from "../actions";
// import { handlers } from "../auth"; // Referring to the auth.ts we just created
// export const { GET, POST } = handlers;



export default function RegisterPage() {
  const switcherValues = ["Телефон", "Почта"];
  const [ isPhoneType, setPhoneType ] = useState<boolean>(true);
  const phoneInput = <Input name="phone" img={"./phone.svg"} placeholder="phone"/>;
  const emailInput = <Input name="email" img={"./email.svg"} placeholder="email"/>;

  // const [ email, setEmail ] = useState();
  // const [ phone, setPhone ] = useState();
  // const [ firstName, setFirstName ] = useState();
  // const [ secondName, setSecondName ] = useState();
  // const [ lastName, setLastName ] = useState();
  // const [ password, setPassword ] = useState();
  // const [ secondPassword, setSecondPassword ] = useState();

  // const initialState = { message: '', errors: {} };

  const [state, formAction, isPending] = useActionState(registerAction, {errors: []});


  return (
    <div className={styles.form_container}>

      <div className={`${styles.circle} ${styles.circle_1}`}/>
      <div className={`${styles.circle} ${styles.circle_2}`}/>
      <Link className={styles.nav_link} href={"/login"}>войти</Link>

      <Form
        title="Регистрация"
        action={formAction}
        isSubmitLoading={isPending}
      >
        <Switcher
          values={switcherValues}
          setNewValue={()=>{setPhoneType(!isPhoneType)}}
        />
        { isPhoneType && phoneInput }
        { !isPhoneType && emailInput }
        <Input name="surname" id={"secName"} img={"./user.svg"} placeholder="фамилия"/>
        <Input name="name" id={"firstName"} img={"./user.svg"} placeholder="имя"/>
        <Input name="last_name" id={"lastName"} img={"./user.svg"} placeholder="отчество"/>
        <Input name="password" id={"firstPassword"} type="password" img={"./key.svg"} placeholder="пароль"/>
        <Input name="second_password" id={"secondPassword"} type="password" img={"./key.svg"} placeholder="повт пароль"/>

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