import { z } from 'zod';

export const signupSchema = z.object({
  userName: z.string().min(3, { message: 'ユーザー名は3文字以上で入力してください' }),
  email: z.string().email({ message: '有効なメールアドレスを入力してください' }),
  password: z
    .string()
    .min(8, { message: 'パスワードは8文字以上で入力してください' })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/, {
      message: 'パスワードは、大文字、小文字、数字をそれぞれ1つ以上含んでください。',
    }),
});

export type SignupFormInput = z.infer<typeof signupSchema>;
