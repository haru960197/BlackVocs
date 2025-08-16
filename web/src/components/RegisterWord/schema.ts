import { z } from 'zod';

export const wordFormSchema = z.object({
  word: z.string().min(1, { message: '単語は必須です' }),
  meaning: z.string().min(1, { message: '意味は必須です' }),
  example: z.string().min(1, { message: '例文は必須です' }),
  exampleTranslation: z.string().min(1, { message: '例文の日本語訳は必須です' }),
});

export type WordFormInput = z.infer<typeof wordFormSchema>;
