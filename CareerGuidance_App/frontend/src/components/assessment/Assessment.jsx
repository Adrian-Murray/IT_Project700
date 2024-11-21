import { useState } from 'react';
import { api } from '../../utils/api';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function Assessment() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth(); // Add this line
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Updated questions with properly mapped adjectives
  const questions = [
    {
      text: "How would you describe yourself?",
      type: "Self-description",
      options: ["assertive", "sociable", "calm", "structured"]
    },
    {
      text: "What qualities do you most value in a work environment?",
      type: "Expected",
      options: ["competitive", "collaborative", "stable", "organized"]
    },
    {
      text: "What motivates you most at work?",
      type: "Expected",
      options: ["achievement", "teamwork", "consistency", "excellence"]
    },
    {
      text: "How do you handle new situations?",
      type: "Self-description",
      options: ["confident", "enthusiastic", "patient", "methodical"]
    },
    {
      text: "What's your preferred work pace?",
      type: "Self-description",
      options: ["fast-paced", "energetic", "steady", "careful"]
    }
  ];

 const handleResponse = async (option) => {
    const newResponses = [...responses, {
      adjective: option.toLowerCase().trim(),
      question_type: questions[currentQuestion].type
    }];
    
    setResponses(newResponses);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      await submitAssessment(newResponses);
    }
  };

  const submitAssessment = async (finalResponses) => {
    setLoading(true);
    try {
      const response = await api.post('/submit_assessment', {
        responses: finalResponses
      });

      // After successful submission, refresh user data and redirect
      await refreshUser();
      navigate('/skills');
      
    } catch (err) {
      console.error('Assessment submission error:', err);
      setError(err.response?.data?.error || 'Failed to submit assessment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-8">Personality Assessment</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200">
          {success}
        </div>
      )}
      
      {!success && (
        <div>
          <div className="mb-8">
            <h3 className="text-xl mb-4">{questions[currentQuestion].text}</h3>
            <div className="grid grid-cols-2 gap-4">
              {questions[currentQuestion].options.map((option) => (
                <button
                  key={option}
                  onClick={() => handleResponse(option)}
                  disabled={loading}
                  className="p-4 text-left border rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors duration-200"
                >
                  <span className="capitalize">{option}</span>
                </button>
              ))}
            </div>
          </div>
          <div className="mt-4 flex items-center justify-between">
            <span className="text-sm text-gray-500">
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <div className="w-32 bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Assessment;