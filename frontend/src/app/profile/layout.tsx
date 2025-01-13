'use server';

import { Suspense } from "react";
import { getMeAction } from "../actions/profile";
import { FetchedUser } from "../actions/auth";
import Page from "./page";

export default async function Layout() {
  const userData: Promise<FetchedUser> = getMeAction();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Page userData={userData} />
    </Suspense>
  )
  
}