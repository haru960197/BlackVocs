"use server";

export const registerNewWord = async (word: string) => {
    await fetch('http://127.0.0.1:4000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: 'testuser',
          password: 'password123',
        }),
      })
}