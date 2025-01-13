import { JWTError, tokenProvider } from "./JWTProvider";

export const fetchJWT = async <T>(
  url: string,
  data?: RequestInit,
): Promise<Response> => {

  const { isLogged, token, } = await tokenProvider();

  if (!isLogged) throw new JWTError("not logged");
  console.log("fetchJWT", token)

  console.log(token, isLogged, {...data});

  return fetch(url, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    ...data,
  }); 
}