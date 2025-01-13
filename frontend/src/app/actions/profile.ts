import { fetchJWT } from "../lib/fetchJWT";
import { FetchedUser } from "../actions/auth";

export const getMeAction = async (): Promise<FetchedUser> => {
  console.log("fetch for profile");
  const resp = await fetchJWT("http://localhost:80/user/me");
  return resp.json();
}
