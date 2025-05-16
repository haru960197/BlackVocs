'use client';

import clsx from 'clsx';
import { createContext, useContext, useState } from 'react';

type ToastType = 'info' | 'success' | 'warning' | 'error';

type ToastData = {
  message: string;
  type: ToastType;
};

type ToastContextType = {
  showToast: (message: string, type?: ToastType) => void;
};

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toast, setToast] = useState<ToastData | null>(null);

  const showToast = (message: string, type: ToastType = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && (
        <div className="toast toast-end">
          <div
            className={clsx(
              'alert',
              toast.type === 'info' && 'alert-info',
              toast.type === 'success' && 'alert-success',
              toast.type === 'error' && 'alert-error',
              toast.type === 'warning' && 'alert-warning'
            )}
          >
            <span>{toast.message}</span>
            <span>{toast.type}</span>
          </div>
        </div>
      )}
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}
