'use client';

import { useState, useEffect } from 'react';
import EvaluationForm, { type EvaluationFormValues } from './components/EvaluationForm';
import EvaluationList from './components/EvaluationList';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

type Evaluation = {
  id: string;
  peerId?: string;
  peerName: string;
  rating: number;
  strengths: string;
  areasForImprovement: string;
  feedback: string;
  createdAt: string;
};

export default function PeerEvaluationPage() {
  const [activeTab, setActiveTab] = useState('evaluate');
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch existing evaluations
  useEffect(() => {
    const fetchEvaluations = async () => {
      try {
        const response = await fetch('/api/peer-evaluation');
        const data = await response.json();
        if (response.ok) {
          setEvaluations((data.evaluations || []) as Evaluation[]);
        }
      } catch (error) {
        console.error('Error fetching evaluations:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchEvaluations();
  }, []);

  const handleEvaluationSubmit = (newEvaluation: EvaluationFormValues | Evaluation) => {
    const normalizedEvaluation: Evaluation = {
      id: 'id' in newEvaluation ? newEvaluation.id : Date.now().toString(),
      peerId: newEvaluation.peerId,
      peerName: 'peerName' in newEvaluation ? newEvaluation.peerName : newEvaluation.peerId,
      rating: newEvaluation.rating,
      strengths: newEvaluation.strengths,
      areasForImprovement: newEvaluation.areasForImprovement,
      feedback: newEvaluation.feedback,
      createdAt: 'createdAt' in newEvaluation ? newEvaluation.createdAt : new Date().toISOString(),
    };
    setEvaluations([normalizedEvaluation, ...evaluations]);
    setActiveTab('my-evaluations');
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Peer Evaluation</h1>
      
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 max-w-md mb-8">
          <TabsTrigger value="evaluate">Evaluate Peers</TabsTrigger>
          <TabsTrigger value="my-evaluations">My Evaluations</TabsTrigger>
        </TabsList>
        
        <TabsContent value="evaluate">
          <Card>
            <CardHeader>
              <CardTitle>Evaluate Your Peers</CardTitle>
              <CardDescription>
                Provide constructive feedback to your team members.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <EvaluationForm onSubmit={handleEvaluationSubmit} />
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="my-evaluations">
          <Card>
            <CardHeader>
              <CardTitle>My Evaluations</CardTitle>
              <CardDescription>
                View and manage your peer evaluations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="flex justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                </div>
              ) : (
                <EvaluationList evaluations={evaluations} />
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
