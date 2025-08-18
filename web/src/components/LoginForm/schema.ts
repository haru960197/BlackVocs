import { z } from 'zod';

export const loginSchema = z.object({
  userName: z
    .string()
    .max(25, { message: 'ユーザー名は25文字以下で入力してください' })
    .min(3, { message: 'ユーザー名は3文字以上で入力してください' }),
  password: z
    .string()
    .max(25, { message: 'パスワードは25文字以下で入力してください' })
    .min(8, { message: 'パスワードは8文字以上で入力してください' })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$#!%*?&]{8,}$/, {
      message: 'パスワードは、大文字、小文字、数字をそれぞれ1つ以上含んでください。',
    }),
});

export type LoginFormInput = z.infer<typeof loginSchema>;
