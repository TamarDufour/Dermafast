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
    text: '1. When you look at the lesion, does one half look different from the other half in shape or thickness?'
  },
  {
    id: 'border',
    text: '2. Have you noticed if the edges of the lesion look ragged, notched, or blurred rather than smooth?'
  },
  {
    id: 'color',
    text: '3. Do you see more than one color in the lesion, such as brown, black, red, white, or blue?'
  },
  {
    id: 'diameter',
    text: '4. Would you say it is larger than about 6 millimeters, roughly the size of a pencil eraser?'
  },
  {
    id: 'evolution',
    text: '5. Has the lesion changed recently in size, shape, color, or caused any new symptoms like itching, bleeding, or crusting?'
  }
];

const LesionQuestionnairePage = ({ nationalId }) => {
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);
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
        setShowSuccess(true);
    } catch (error) {
        console.error("Error submitting questionnaire:", error);
        alert(`Error submitting questionnaire: ${error.message}`);
    }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Lesion Questionnaire</CardTitle>
          <CardDescription>Please answer the following questions about the lesion.</CardDescription>
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

      {showSuccess && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <h2 className="text-2xl font-bold mb-4">Questionnaire submitted successfully!</h2>
            <p>please move on to the next step.</p>
            <Button
              onClick={() => {
                setShowSuccess(false);
                navigate('/check-lesion');
              }}
              className="mt-4"
            >
              Next Step
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LesionQuestionnairePage;
