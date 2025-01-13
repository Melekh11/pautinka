'use client';

import { Children, ComponentPropsWithoutRef, DialogHTMLAttributes, Dispatch, InputHTMLAttributes, MouseEventHandler, ReactNode, SetStateAction, use, useEffect, useId, useRef, useState } from "react";
import Image from "next/image";
import styles from "./page.module.scss";
import entStyles from "../entities.module.scss";
import { FetchedUser } from "../actions/auth";

interface Props {
  children?: ReactNode
  text?: string;
  // any props that come into the component
};

type PropsInput = {
  label: string;
  name: string;
  onChange: Dispatch<SetStateAction<FetchedUser>>;
} & Omit<InputHTMLAttributes<HTMLInputElement>, "onChange">;

type WorkProps = {
  company: string;
  src: string;
  alt: string;
  position: string;
  date_start: string;
  date_end: string;
}

type CrateTagDialogProps = {
  close: () => void;
  addTag: Dispatch<SetStateAction<string[]>>;
} & ComponentPropsWithoutRef<"dialog">;

const Tag = ({text}: Props) => {
  return (
    <span className={styles.tag_item}>
      { text }
      <Image
        width={10}
        height={10}
        alt={'del'}
        src={'./no.svg'}
        className={styles.no_tag}
      />
    </span>
  )
};

const Click = ({ children }: Props) => {
  return (
    <div className={entStyles.rel}>

      {children}
      <span className={styles.clickable}>+</span>
    </div>
  )
};

const LocalInput = ({ name, label, placeholder, value, onChange }: PropsInput) => {
  const id = useId();

  const handleChange = (e: React.FormEvent<HTMLInputElement>) => {
    const newValue = e.currentTarget.value;
    onChange((data: FetchedUser) => {
        const ob = {
          [name]: newValue,
          ...data,
        }
        return ob;
      }
    )
  }
  return (
    <div className={styles.input_container}>
      <label htmlFor={id}>{label}</label>
      <input defaultValue={value} name={name} className={styles.field} placeholder={placeholder} id={id}/>
    </div>
  )
};

const Work = ({ company, src, alt, position, date_start, date_end }: WorkProps) => {
  return (
    <div className={styles.work}>
      <span className={styles.work_company}>{company}</span>
      <Image
        width={35}
        height={35}
        src={src}
        alt={alt}
        className={styles.work_image}
      />
      <span className={styles.work_position}>{position}</span>

      <p className={styles.work_dates}>{date_start} - {date_end}</p>
    </div>
  )
}

const CrateTagDialog = (props: CrateTagDialogProps) => {
  const { open, close, addTag, ...rest } = props;

  const ref = useRef<HTMLDialogElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  console.log(open);

  const handleClick = () => {
    const value = inputRef.current?.value ?? "";
    addTag((vals) => {
      return [value, ...vals];
    });
    close();
  }

  // useEffect(() => {
  //   console.log("state changed");
  //   const dialog = ref.current!;
  //   if (open) {
  //     dialog.showModal();
  //   } else {
  //     console.log("closed dialog")
  //     dialog.close();
  //   }
  // }, [open]);

  return (
    <dialog className={styles.dialog} open={open} ref={ref} {...rest}>
      <input ref={inputRef} className={styles.dialog_input}/>
      <button onClick={handleClick} className={styles.dialog_button}>Добавить</button>
    </dialog>
  )
}

const initState: FetchedUser = {
  id: 0,
  name: "",
  surname: "",
  last_name: "",
  email: "",
  phone: "",
  university: "",
  birthdate: "",
  course: "",
  short_status: "",
  full_status: "",
  about_me: "",
  links: ""
}

type ProfileProps = {
  userData: Promise<FetchedUser>;
}

export default function Page({ userData }: ProfileProps) {

  
  const user = use(userData);
  const [values, updateValues] = useState(user);
  const [ isModalOpen, setModalOpen ] = useState(false);
  const [tags, setTags] = useState(["графический дизайнер", "3-D дизайнер", "Unit-экономика", "Goland"])

  console.log("profile component", user);
  console.log(isModalOpen);

  return (
    <div className={styles.profile_container}>
      <div className={styles.top_info}>
        <Image
          src={'./user.svg'}
          width={250}
          height={250}
          alt={"your image"}
          className={styles.ava}
        />
        <h2 className={styles.h2}>{values.name} {values.surname}</h2>

        <div className={styles.subscribers_data}>
          <span className={styles.subscriber_item}>
            <div>подписчики</div>
            <div className={styles.subscriber_item_number}>4</div>
          </span>
          <span className={styles.subscriber_item}>
            <div>подписки</div>
            <div className={styles.subscriber_item_number}>10</div>
          </span>
          <span className={styles.subscriber_item}>
            <div>узлы</div>
            <div className={styles.subscriber_item_number}>2</div>
          </span>
        </div>

        <div style={{
          
        }}>
          {/* <Tag text={'графический дизайнер'}/>
          <Tag text={'3-D дизайнер'}/>
          <Tag text={'Unit-экономика'}/>
          <Tag text={'Goland'}/> */}
          {tags.map((tagName, id) => (
            <Tag key={id} text={tagName}/>
          ))}
          <span
            className={styles.new_tag}
            onClick={() => {
              setModalOpen(true);
              console.log("trueee");
            }}
          >
            <Image
              width={10}
              height={10}
              alt={'del'}
              src={'./no.svg'}
              className={styles.new_tag_image}
            />
          </span>
          <CrateTagDialog
            close={()=>setModalOpen(false)}
            addTag={setTags}
            open={isModalOpen}
          />
        </div>
      </div>

    <div className={styles.contact_data}>
      <LocalInput onChange={updateValues} name={"name"} value={values.name} placeholder="Елизавета" label="имя"/>
      <LocalInput onChange={updateValues} name={"surname"} value={values.surname} placeholder="Егорова" label="фамилия"/>
      <LocalInput onChange={updateValues} name={"last_name"} value={values.last_name} placeholder="Алексеевна" label="отчество"/>
      <LocalInput onChange={updateValues} name={"phone"} value={values.phone} placeholder="+7(926)191-43-52" label="номер телефона"/>
      <LocalInput onChange={updateValues} name={"email"} value={values.email} placeholder="dnossova@gmail.com" label="почта"/>
    </div>

    <div className={styles.study_data}>
      <LocalInput onChange={updateValues} name={"university"} value={values.university} placeholder="НИУ ВШЭ" label="ВУЗ"/>
      <LocalInput onChange={updateValues} name={"birthdate"} value={values.birthdate} placeholder="11.02.2006" label="Дата рождения"/>
      <LocalInput onChange={updateValues} name={"course"} value={values.course} placeholder="2 курс (бак)" label="Курс"/>

      <div className={styles.blog_container}>
        To <br/> My <br/> Blog
        <div className={`${styles.circle} ${styles.circle_2}`}/>
        <div className={`${styles.circle} ${styles.circle_1}`}/>
        <Image
          src={"./right-arrow.svg"}
          width={27}
          height={17}
          alt="to blog"
          className={styles.go_to_blog}
        />
      </div>
    </div>

    <div className={styles.status}>
      <span className={styles.top_status}>статус: провожу кейс-чемпионаты</span>
      <ul className={styles.status_list}>
        <li><span className={styles.down_status}>Карьерные треки для соискателей</span></li>
        <li><span className={styles.down_status}>HR-консалтинг для компаний</span></li>
      </ul>
    </div>

    <div className={styles.about}>
      <span className={styles.title}>about me</span>
      Руководитель направления обучения в СБЕР «Деловая среда».
      Карьерный консультант, психолог. Спикер в EdTech HRTech.

      Найти работу можно тут: https://set.ki/community /kco4mJW
    </div>

    <div className={styles.links_jobs}>
      <div className={styles.links}>
        <span className={styles.title}>my links</span>
        <p>
          тг - @maty_melekh
          inst - @july_lara
          linkedIn - https://careers.linkedin.cn/maty
        </p>
      </div>
      <div className={styles.jobs}>
        <span className={styles.title}>Опыт работы</span>
        <Work company={"VK"} src={"./vk.svg"} alt={"VK"} position="Маркетолог" date_start="04.24" date_end="сейчас"/>
        <Work company={"Т-банк"} src={"./tink.svg"} alt={"Т-банк"} position="СММ Менеджер" date_start="10.23" date_end="04.24"/>
      </div>
    </div>
    </div>
  )
}