import { NextResponse } from 'next/server';
import { z } from 'zod';
import { db } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';

// Schema for evaluation
const evaluationSchema = z.object({
  peerId: z.string().min(1, 'Peer ID is required'),
  rating: z.number().min(1).max(5),
  feedback: z.string().min(10, 'Feedback must be at least 10 characters'),
  strengths: z.string().min(1, 'Please mention at least one strength'),
  areasForImprovement: z.string().min(1, 'Please mention at least one area for improvement'),
});

export async function GET() {
  try {
    const user = await getCurrentUser();
    if (!user) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    // In a real app, you would fetch evaluations from your database
    // This is a mock implementation
    const evaluations = [];
    
    return NextResponse.json({ evaluations });
  } catch (error) {
    console.error('Error fetching evaluations:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const user = await getCurrentUser();
    if (!user) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    const json = await request.json();
    const { peerId, rating, feedback, strengths, areasForImprovement } = evaluationSchema.parse(json);

    // In a real app, you would save this to your database
    // This is a mock implementation
    const newEvaluation = {
      id: Math.random().toString(36).substring(2, 9),
      peerId,
      peerName: 'Peer Name', // In a real app, fetch this from your database
      rating,
      feedback,
      strengths,
      areasForImprovement,
      createdAt: new Date().toISOString(),
      evaluatorId: user.id,
    };

    return NextResponse.json(newEvaluation);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return new NextResponse(JSON.stringify(error.errors), { status: 422 });
    }
    
    console.error('Error creating evaluation:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
