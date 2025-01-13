import { Dispatch, InputHTMLAttributes, SetStateAction } from 'react';

type InputType = Omit<InputHTMLAttributes<HTMLInputElement>, "onChange"> & {
  img: string;
  label?: string;
  onChange?: Dispatch<SetStateAction<string>>;
};

export type { InputType };
