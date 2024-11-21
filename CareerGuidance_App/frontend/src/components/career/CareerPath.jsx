import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { api } from '../../utils/api';
import { AlertCircle, DollarSign, Clock, TrendingUp } from 'lucide-react';

function CareerPath() {
    const [careerData, setCareerData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const fetchCareerPath = async () => {
            try {
                const response = await api.get('/career_path');
                if (response.data.redirect) {
                    navigate(response.data.redirect);
                    return;
                }
                setCareerData(response.data);
            } catch (err) {
                if (err.response?.status === 400 && err.response.data.redirect) {
                    navigate(err.response.data.redirect);
                    return;
                }
                setError(err.response?.data?.error || 'Failed to load career data');
            } finally {
                setLoading(false);
            }
        };

        fetchCareerPath();
    }, [navigate]);

    return (
        <div className="max-w-4xl mx-auto space-y-8 p-4">
            {careerData && (
                <>
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-2xl font-bold mb-4">Career Match: {careerData.current_career}</h2>
                        <p className="text-lg text-indigo-600">Match Rating: {careerData.match_rating}%</p>
                    </div>
                    
                    <div className="space-y-6">
                        <h2 className="text-2xl font-bold text-gray-900">Career Progression</h2>
                        
                        <div className="relative">
                            {careerData.progression.map((stage, index) => (
                                <div key={index} className="mb-8 flex">
                                    <div className="flex flex-col items-center mr-4">
                                        <div className="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold">
                                            {index + 1}
                                        </div>
                                        {index < careerData.progression.length - 1 && (
                                            <div className="w-1 h-24 bg-indigo-200" />
                                        )}
                                    </div>
                                    
                                    <div className="bg-white p-6 rounded-lg shadow flex-1">
                                        <h3 className="text-xl font-bold text-indigo-600">{stage.title}</h3>
                                        <div className="mt-4 grid grid-cols-2 gap-4">
                                            <div className="flex items-center">
                                                <DollarSign className="h-5 w-5 text-green-500 mr-2" />
                                                <span>${stage.salary.toLocaleString()}/year</span>
                                            </div>
                                            <div className="flex items-center">
                                                <Clock className="h-5 w-5 text-indigo-500 mr-2" />
                                                <span>{stage.years}+ years experience</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}

export default CareerPath;