type ToastInput = {
  title?: string;
  description?: string;
  variant?: 'default' | 'destructive';
};

export function useToast() {
  return {
    toast: ({ title, description, variant }: ToastInput) => {
      const message = [title, description].filter(Boolean).join('\n');
      if (variant === 'destructive') {
        window.alert(message || 'Something went wrong');
        return;
      }
      window.alert(message || 'Success');
    },
  };
}
