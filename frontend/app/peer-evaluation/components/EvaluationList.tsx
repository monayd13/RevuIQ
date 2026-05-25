import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { format } from 'date-fns';

export interface Evaluation {
  id: string;
  peerName: string;
  rating: number;
  strengths: string;
  areasForImprovement: string;
  feedback: string;
  createdAt: string;
}

interface EvaluationListProps {
  evaluations: Evaluation[];
}
const EvaluationList = ({ evaluations }: EvaluationListProps) => {
  if (evaluations.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No evaluations found.</p>
        <p className="text-sm text-muted-foreground mt-2">
          Submit your first evaluation using the form above.
        </p>
      </div>
    );
  }

  const getRatingColor = (rating: number) => {
    if (rating >= 4) return 'bg-green-100 text-green-800';
    if (rating >= 3) return 'bg-blue-100 text-blue-800';
    if (rating >= 2) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="space-y-6">
      {evaluations.map((evaluation) => (
        <Card key={evaluation.id} className="overflow-hidden">
          <CardHeader className="bg-muted/20 px-6 py-4 border-b">
            <div className="flex justify-between items-start">
              <div>
                <CardTitle className="text-lg">
                  Evaluation for {evaluation.peerName}
                </CardTitle>
                <p className="text-sm text-muted-foreground">
                  {format(new Date(evaluation.createdAt), 'MMMM d, yyyy')}
                </p>
              </div>
              <Badge className={`px-3 py-1 text-sm ${getRatingColor(evaluation.rating)}`}>
                {evaluation.rating.toFixed(1)} ★
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            <div>
              <h4 className="font-medium mb-2">Strengths</h4>
              <p className="text-muted-foreground whitespace-pre-line">
                {evaluation.strengths}
              </p>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Areas for Improvement</h4>
              <p className="text-muted-foreground whitespace-pre-line">
                {evaluation.areasForImprovement}
              </p>
            </div>

            {evaluation.feedback && (
              <div>
                <h4 className="font-medium mb-2">Additional Feedback</h4>
                <p className="text-muted-foreground whitespace-pre-line">
                  {evaluation.feedback}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default EvaluationList;
