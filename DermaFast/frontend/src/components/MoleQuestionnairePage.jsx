import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabase';

const MoleQuestionnairePage = ({ nationalId = "123456789" }) => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const { data, error } = await supabase
          .from('question_definitions')
          .select('question_key, question_text');

        if (error) {
          throw error;
        }
        
        setQuestions(data);
      } catch (error) {
        setError("Failed to fetch questions.");
        console.error("Error fetching questions:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  const handleAnswerChange = (questionKey, value) => {
    setAnswers(prevAnswers => ({
      ...prevAnswers,
      [questionKey]: value === 'yes',
    }));
  };

  const allQuestionsAnswered = questions.length > 0 && Object.keys(answers).length === questions.length;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!allQuestionsAnswered) {
      return;
    }

    const payload = {
      national_id: nationalId,
      ...answers,
    };

    try {
      const { error } = await supabase.from('mole_questionnaires').insert([payload]);

      if (error) {
        throw error;
      }

      console.log('Questionnaire submitted successfully');
      navigate('/check-mole');
    } catch (error) {
      setError('Failed to submit questionnaire');
      console.error('Error submitting questionnaire:', error);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading questions...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">Error: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Mole Questionnaire
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form onSubmit={handleSubmit} className="space-y-6">
            {questions.map((question, index) => (
              <fieldset key={question.question_key} className="space-y-2">
                <legend className="text-base font-medium text-gray-900">
                  {index + 1}. {question.question_text}
                </legend>
                <div className="flex items-center space-x-6 pt-2">
                  <div className="flex items-center">
                    <input
                      id={`${question.question_key}-yes`}
                      name={question.question_key}
                      type="radio"
                      value="yes"
                      checked={answers[question.question_key] === true}
                      onChange={() => handleAnswerChange(question.question_key, 'yes')}
                      className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                      required
                    />
                    <label htmlFor={`${question.question_key}-yes`} className="ml-3 block text-sm font-medium text-gray-700">
                      Yes
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id={`${question.question_key}-no`}
                      name={question.question_key}
                      type="radio"
                      value="no"
                      checked={answers[question.question_key] === false}
                      onChange={() => handleAnswerChange(question.question_key, 'no')}
                      className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                      required
                    />
                    <label htmlFor={`${question.question_key}-no`} className="ml-3 block text-sm font-medium text-gray-700">
                      No
                    </label>
                  </div>
                </div>
              </fieldset>
            ))}

            <div>
              <button
                type="submit"
                disabled={!allQuestionsAnswered}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Continue
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default MoleQuestionnairePage;
