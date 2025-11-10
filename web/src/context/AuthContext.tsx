"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { handleLogin, handleLogout, loggedInCheck } from "./actions";

type AuthContextType = {
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (userName: string, password: string) => Promise<boolean>;
  logout: () => Promise<boolean>;
};

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: React.PropsWithChildren) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initialCheck = async () => {
      const res = await loggedInCheck();

      if (res.success && res.data?.user_id) {
        setIsLoggedIn(true);
      }

      setIsLoading(false);
    };

    initialCheck();
  }, []);

  const login = async (userName: string, password: string) => {
    setIsLoading(true);

    const res = await handleLogin(userName, password);

    setIsLoading(false);

    if (!res.success) {
      return false;
    }

    setIsLoggedIn(true);
    return true;
  };

  const logout = async () => {
    setIsLoading(true);

    const res = await handleLogout();

    setIsLoading(false);

    if (!res.success) {
      return false;
    }

    setIsLoggedIn(false);
    return true;
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within a AuthProvider");
  }
  return context;
};
