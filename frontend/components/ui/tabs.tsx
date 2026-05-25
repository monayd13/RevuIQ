import * as React from 'react';
import { cn } from '@/lib/utils';

type TabsContextValue = {
  value: string;
  onValueChange: (value: string) => void;
};

const TabsContext = React.createContext<TabsContextValue | null>(null);

export function Tabs({ value, onValueChange, className, children }: React.HTMLAttributes<HTMLDivElement> & TabsContextValue) {
  return (
    <TabsContext.Provider value={{ value, onValueChange }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('inline-flex h-10 items-center justify-center rounded-md bg-gray-100 p-1 text-gray-500', className)} {...props} />;
}

export function TabsTrigger({ value, className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { value: string }) {
  const context = React.useContext(TabsContext);
  const active = context?.value === value;

  return (
    <button
      type="button"
      className={cn('inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all', active ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900', className)}
      onClick={() => context?.onValueChange(value)}
      {...props}
    >
      {children}
    </button>
  );
}

export function TabsContent({ value, className, children, ...props }: React.HTMLAttributes<HTMLDivElement> & { value: string }) {
  const context = React.useContext(TabsContext);

  if (context?.value !== value) {
    return null;
  }

  return <div className={cn('mt-2', className)} {...props}>{children}</div>;
}
