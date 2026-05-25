import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    evaluations: [],
    storage: 'client-local-storage',
    message: 'Peer evaluations are persisted in browser storage for this frontend deployment.',
  });
}

export async function POST(request: Request) {
  try {
    const json = await request.json();
    const { peerId, peerName, rating, feedback, strengths, areasForImprovement } = json;

    if (!peerId || !peerName || !rating || !feedback || !strengths || !areasForImprovement) {
      return NextResponse.json({ error: 'Missing required evaluation fields' }, { status: 422 });
    }

    return NextResponse.json({
      id: Math.random().toString(36).substring(2, 9),
      peerId,
      peerName,
      rating: Number(rating),
      feedback,
      strengths,
      areasForImprovement,
      createdAt: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error creating evaluation:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
