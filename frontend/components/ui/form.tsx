import * as React from 'react';
import { Controller, FormProvider, useFormContext } from 'react-hook-form';
import type { ControllerProps, FieldPath, FieldValues } from 'react-hook-form';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';

export const Form = FormProvider;

export function FormField<TFieldValues extends FieldValues = FieldValues, TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>>(
  props: ControllerProps<TFieldValues, TName>
) {
  return <Controller {...props} />;
}

export const FormItem = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('space-y-2', className)} {...props} />
));
FormItem.displayName = 'FormItem';

export const FormLabel = React.forwardRef<React.ElementRef<typeof Label>, React.ComponentPropsWithoutRef<typeof Label>>(({ className, ...props }, ref) => (
  <Label ref={ref} className={cn(className)} {...props} />
));
FormLabel.displayName = 'FormLabel';

export const FormControl = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ ...props }, ref) => (
  <div ref={ref} {...props} />
));
FormControl.displayName = 'FormControl';

export const FormDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-gray-500', className)} {...props} />
));
FormDescription.displayName = 'FormDescription';

export function FormMessage({ className, children, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  const context = useFormContext();
  const message = children || Object.values(context.formState.errors)[0]?.message?.toString();

  if (!message) {
    return null;
  }

  return (
    <p className={cn('text-sm font-medium text-red-600', className)} {...props}>
      {message}
    </p>
  );
}
