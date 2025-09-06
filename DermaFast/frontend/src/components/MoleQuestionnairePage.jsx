import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { supabase } from "@/supabase";

const questions = [
  {
    id: 'asymmetry',
    text: '1. When you look at the mole, does one half look different from the other half in shape or thickness?'
  },
  {
    id: 'border',
    text: '2. Have you noticed if the edges of the mole look ragged, notched, or blurred rather than smooth?'
  },
  {
    id: 'color',
    text: '3. Do you see more than one color in the mole, such as brown, black, red, white, or blue?'
  },
  {
    id: 'diameter',
    text: '4. Would you say it is larger than about 6 millimeters, roughly the size of a pencil eraser?'
  },
  {
    id: 'evolution',
    text: '5. Has the mole changed recently in size, shape, color, or caused any new symptoms like itching, bleeding, or crusting?'
  }
];

const MoleQuestionnairePage = ({ nationalId }) => {
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleValueChange = (questionId, value) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
    setError(''); // Clear error when user makes a selection
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.keys(answers).length < questions.length) {
      setError('Please answer all questions before submitting.');
      return;
    }
    setError('');
    
    const submissionData = {
        national_id: nationalId,
    };
    questions.forEach((q, index) => {
        submissionData[`q${index + 1}`] = answers[q.id] === 'yes';
    });

    try {
        const { data, error } = await supabase
            .from('mole_questionnaires')
            .insert([submissionData]);

        if (error) {
            throw error;
        }

        console.log("Questionnaire submitted successfully:", data);
        alert("Questionnaire submitted successfully!");
        navigate('/check-mole');
    } catch (error) {
        console.error("Error submitting questionnaire:", error);
        alert(`Error submitting questionnaire: ${error.message}`);
    }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Mole Questionnaire</CardTitle>
          <CardDescription>Please answer the following questions about the mole.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-8">
            {questions.map((q) => (
              <div key={q.id} className="space-y-4">
                <Label className="text-base">{q.text}</Label>
                <RadioGroup onValueChange={(value) => handleValueChange(q.id, value)}>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="yes" id={`${q.id}-yes`} />
                    <Label htmlFor={`${q.id}-yes`}>Yes</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="no" id={`${q.id}-no`} />
                    <Label htmlFor={`${q.id}-no`}>No</Label>
                  </div>
                </RadioGroup>
              </div>
            ))}

            {error && <p className="text-sm text-red-600">{error}</p>}
            
            <CardFooter className="px-0">
              <Button type="submit" className="w-full">
                Submit Questionnaire
              </Button>
            </CardFooter>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default MoleQuestionnairePage;
