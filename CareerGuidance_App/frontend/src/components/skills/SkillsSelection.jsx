import { useState, useEffect } from 'react';
import { api } from '../../utils/api';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';

function SkillsSelection() {
  const [availableSkills, setAvailableSkills] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadSkills = async () => {
      try {
        const [skillsRes, profileRes] = await Promise.all([
          api.get('/skills'),
          api.get('/user/profile')
        ]);
        
        setAvailableSkills(skillsRes.data);
        setSelectedSkills(profileRes.data.user.skills || []);
      } catch (err) {
        console.error('Skills loading error:', err);
        setError('Failed to load skills');
      } finally {
        setLoading(false);
      }
    };

    loadSkills();
  }, []);

  const handleSkillToggle = (skill) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter(s => s !== skill));
    } else {
      setSelectedSkills([...selectedSkills, skill]);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError('');
    setSuccess('');
    
    try {
      await api.post('/submit_skills', {
        skills: selectedSkills
      });
      setSuccess('Skills updated successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update skills');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Select Your Skills</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-50 rounded-lg flex items-center">
          <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
          <span className="text-red-700">{error}</span>
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 bg-green-50 rounded-lg flex items-center">
          <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
          <span className="text-green-700">{success}</span>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {availableSkills.map((skill) => (
          <button
            key={skill}
            onClick={() => handleSkillToggle(skill)}
            className={`p-3 rounded-lg text-left transition-colors ${
              selectedSkills.includes(skill)
                ? 'bg-indigo-100 text-indigo-700 border-indigo-300'
                : 'bg-gray-50 text-gray-700 border-gray-200'
            } border hover:bg-indigo-50`}
          >
            {skill}
          </button>
        ))}
      </div>

      <div className="mt-6">
        <button
          onClick={handleSubmit}
          disabled={submitting}
          className="w-full sm:w-auto px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? (
            <span className="flex items-center">
              <Loader2 className="animate-spin -ml-1 mr-2 h-5 w-5" />
              Saving...
            </span>
          ) : (
            'Save Skills'
          )}
        </button>
      </div>
    </div>
  );
}

export default SkillsSelection;