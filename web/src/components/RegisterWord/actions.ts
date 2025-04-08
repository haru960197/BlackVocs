'use server';

/**
 * 英単語を登録する
 * @param word 登録したい英単語
 */
export const registerNewWord = async (word: string) => {
  await fetch(`${process.env.SERVICE_URI}/new_word`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ word }),
  });
};
