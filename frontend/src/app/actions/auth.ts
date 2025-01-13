'use server';

import { redirect } from "next/navigation";
import { fetchJWT } from "../lib/fetchJWT";
import { tokenProvider } from "../lib/JWTProvider";
import { revalidatePath } from "next/cache";

type ActionState = {
  errors: string[],
}

type TokenResponse = {
  access_token: string;
  token_type: string;
}

export type FetchedUser = {
  id: number
  name: string
  surname: string
  last_name: string
  email: string
  phone: string
  university: string
  birthdate: string
  course: string
  short_status: string
  full_status: string
  about_me: string
  links: string
}

export async function loginAction(state: ActionState, formData: FormData): Promise<ActionState> {
  const phone = formData.get("phone") ?? "";
  const email = formData.get("email") ?? "";
  const password = formData.get("password");

  const resp = await fetch("http://localhost:80/user/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      password,
      phone,
      email,
    })
  });

  if (resp.status !== 200) {
    return {
      errors: [resp.statusText],
    };
  }

  const data = <TokenResponse> await resp.json();
  const { setToken } = await tokenProvider();
  console.log("log in action");
  await setToken(data.access_token);
  redirect("/profile");
}

export async function registerAction(state: ActionState, formData: FormData): Promise<ActionState> {
  const phone = formData.get("phone") ?? "";
  const email = formData.get("email") ?? "";
  const password = formData.get("password");
  const surname = formData.get("surname");
  const name = formData.get("name");
  const lastName = formData.get("last_name");
  const secondPassword = formData.get("second_password");

  if (password !== secondPassword ) {
    return {
      errors: ["Пароли должны совпадать"],
    }
  }

  const resp = await fetch("http://localhost:80/user/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      password,
      phone,
      email,
      name,
      surname,
    })
  });

  if (resp.status !== 200) {
    return {
      errors: [resp.statusText],
    };
  }

  const data = <TokenResponse> await resp.json();
  const { setToken } = await tokenProvider();
  await setToken(data.access_token);
  revalidatePath('/login')
  redirect("/profile");
}

