import { InputHTMLAttributes } from 'react';

type InputType = {
  img: string;
  label?: string;
} & InputHTMLAttributes<HTMLInputElement>;

export type { InputType };
