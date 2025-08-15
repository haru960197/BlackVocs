import { z } from 'zod';

export const loginSchema = z.object({
  userName: z.string().min(3, { message: 'ユーザー名は3文字以上で入力してください' }),
  password: z
    .string()
    .min(8, { message: 'パスワードは8文字以上で入力してください' })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/, {
      message: 'パスワードは、大文字、小文字、数字をそれぞれ1つ以上含んでください。',
    }),
});

export type LoginFormInput = z.infer<typeof loginSchema>;
