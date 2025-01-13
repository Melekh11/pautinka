'use server';

import { cookies } from 'next/headers';
import { NextRequest } from 'next/server';

type UseJWTProvider = {
  isLogged: boolean;
  token: string | undefined;
  setToken: (token: string) => Promise<void>;
};

class JWTError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "JWTError";
  }
}

const JWTKeyName = "JWT_TOKEN";


const setJWTToken = async (token: string) => {
  const cookieStore = await cookies();
  cookieStore.set(JWTKeyName, token);
}


const tokenProvider = async function(request?: NextRequest): Promise<UseJWTProvider> {

  const JWT = !!request ? request.cookies.get(JWTKeyName)?.value : (await cookies()).get(JWTKeyName)?.value;

  if (!JWT) {
    return {
      isLogged: false,
      token: undefined,
      setToken: setJWTToken,
    };
  }

  const checkTokenResp = await fetch("http://localhost:80/user/me", {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${JWT}`,
      }
    }
  );

  if (checkTokenResp.status !== 200) {
    return {
      isLogged: false,
      token: undefined,
      setToken: setJWTToken,
    };
  }

  return {
    isLogged: true,
    token: JWT,
    setToken: setJWTToken,
  };
}

export { tokenProvider, JWTError };
