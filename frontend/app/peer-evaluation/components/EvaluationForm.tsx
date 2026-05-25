'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';

const evaluationSchema = z.object({
  peerId: z.string().min(1, 'Please select a peer'),
  peerName: z.string().min(1, 'Please select a peer'),
  rating: z.number().min(1).max(5),
  feedback: z.string().min(10, 'Feedback must be at least 10 characters'),
  strengths: z.string().min(1, 'Please mention at least one strength'),
  areasForImprovement: z.string().min(1, 'Please mention at least one area for improvement'),
});

export type EvaluationFormValues = z.infer<typeof evaluationSchema>;

interface EvaluationFormProps {
  onSubmit: (data: EvaluationFormValues) => void;
}

export default function EvaluationForm({ onSubmit }: EvaluationFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [peers, setPeers] = useState<Array<{ id: string; name: string; email: string }>>([]);
  const { toast } = useToast();

  useEffect(() => {
    const users = JSON.parse(localStorage.getItem('revuiq_users') || '[]');
    const currentUser = JSON.parse(localStorage.getItem('userData') || '{}');
    const availablePeers = users
      .filter((user: { email?: string }) => user.email && user.email !== currentUser.email)
      .map((user: { id?: string; name?: string; email: string }) => ({
        id: user.id || user.email,
        name: user.name || user.email,
        email: user.email,
      }));
    setPeers(availablePeers);
  }, []);

  const form = useForm<EvaluationFormValues>({
    resolver: zodResolver(evaluationSchema),
    defaultValues: {
      peerId: '',
      peerName: '',
      rating: 3,
      feedback: '',
      strengths: '',
      areasForImprovement: '',
    },
  });

  const handleSubmit = async (data: EvaluationFormValues) => {
    try {
      setIsSubmitting(true);

      const result = {
        ...data,
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
      };

      onSubmit(result);
      
      toast({
        title: 'Evaluation submitted!',
        description: 'Your peer evaluation has been submitted successfully.',
      });
      
      form.reset();
    } catch (error) {
      console.error('Error submitting evaluation:', error);
      toast({
        title: 'Error',
        description: 'Failed to submit evaluation. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="peerId"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Select Peer to Evaluate</FormLabel>
              <Select
                onValueChange={(value) => {
                  const peer = peers.find((item) => item.id === value);
                  field.onChange(value);
                  form.setValue('peerName', peer?.name || '');
                }}
                defaultValue={field.value}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a peer" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {peers.length > 0 ? (
                    peers.map((peer) => (
                      <SelectItem key={peer.id} value={peer.id}>
                        {peer.name} ({peer.email})
                      </SelectItem>
                    ))
                  ) : (
                    <SelectItem value="no-peers" disabled>
                      No other signed-up users available
                    </SelectItem>
                  )}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="rating"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Overall Rating</FormLabel>
              <Select
                onValueChange={(value) => field.onChange(Number(value))}
                defaultValue={field.value?.toString()}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a rating" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {[5, 4, 3, 2, 1].map((num) => (
                    <SelectItem key={num} value={num.toString()}>
                      {'★'.repeat(num) + '☆'.repeat(5 - num)} ({num})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormDescription>
                1 = Needs Improvement, 5 = Excellent
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="strengths"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Strengths</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="What are this peer's key strengths?"
                  className="min-h-[100px]"
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Be specific about what this peer does well.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="areasForImprovement"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Areas for Improvement</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="What could this peer improve on?"
                  className="min-h-[100px]"
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Provide constructive and actionable feedback.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="feedback"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Additional Feedback</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Any additional comments or feedback for this peer?"
                  className="min-h-[120px]"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end">
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Submit Evaluation'}
          </Button>
        </div>
      </form>
    </Form>
  );
}
