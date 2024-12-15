import { FormHTMLAttributes } from 'react';

type FormType = {
  title: string;
} & FormHTMLAttributes<HTMLFormElement>

export type { FormType };
