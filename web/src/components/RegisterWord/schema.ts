import { z } from 'zod';

export const wordFormSchema = z.object({
  word: z
    .string()
    .max(45, { message: '45文字以内で入力してください' })
    .min(1, { message: '単語は必須です' }),
  meaning: z
    .string()
    .max(45, { message: '45文字以内で入力してください' })
    .min(1, { message: '意味は必須です' }),
  example: z
    .string()
    .max(150, { message: '150文字以内で入力してください' }),
  exampleTranslation: z
    .string()
    .max(150, { message: '150文字以内で入力してください' }),
});

export type WordFormInput = z.infer<typeof wordFormSchema>;
