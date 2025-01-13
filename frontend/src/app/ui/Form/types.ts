import { FormHTMLAttributes } from 'react';

type FormType = {
  title: string;
  isSubmitLoading: boolean;
} & FormHTMLAttributes<HTMLFormElement>

export type { FormType };
