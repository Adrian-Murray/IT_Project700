import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../utils/api';
import { useAuth } from '../../context/AuthContext';
import { Loader2, AlertCircle } from 'lucide-react';

function Dashboard() {
    const { user } = useAuth();
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const [profileRes, recommendationRes] = await Promise.all([
                    api.get('/user/profile'),
                    api.get('/recommend')
                ]);

                setDashboardData({
                    profile: profileRes.data.user,
                    recommendation: recommendationRes.data
                });
            } catch (err) {
                console.error('Dashboard error:', err);
                setError(err.response?.data?.error || 'Failed to load dashboard data');
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
                <AlertCircle className="h-5 w-5 text-red-400 mt-0.5 mr-2" />
                <div>
                    <h3 className="text-red-800 font-medium">Error Loading Dashboard</h3>
                    <p className="text-red-600 mt-1">{error}</p>
                </div>
            </div>
        );
    }

    if (!dashboardData) {
        return (
            <div className="text-center py-12">
                <p className="text-gray-500">No dashboard data available</p>
            </div>
        );
    }

    const { recommendation } = dashboardData;

    return (
        <div className="space-y-6">
            {/* User Welcome Section */}
            <div className="bg-white p-6 rounded-lg shadow">
                <h1 className="text-2xl font-bold text-gray-900">
                    Welcome back, {user?.firstName}!
                </h1>
                <p className="mt-2 text-gray-600">
                    Here's your career development summary
                </p>
            </div>

            {user?.profile && (
              <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-2xl font-bold mb-4">Personality Profile</h2>
                  <div className="space-y-4">
                      <p className="text-xl text-indigo-600">{user.profile.name}</p>
                      <p className="text-gray-600">{user.profile.description}</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                          <div className="p-4 bg-indigo-50 rounded-lg">
                              <p className="font-medium">Dominance</p>
                              <p className="text-2xl text-indigo-600">{user.profile.dominance}%</p>
                          </div>
                          <div className="p-4 bg-indigo-50 rounded-lg">
                              <p className="font-medium">Extraversion</p>
                              <p className="text-2xl text-indigo-600">{user.profile.extraversion}%</p>
                          </div>
                          <div className="p-4 bg-indigo-50 rounded-lg">
                              <p className="font-medium">Patience</p>
                              <p className="text-2xl text-indigo-600">{user.profile.patience}%</p>
                          </div>
                          <div className="p-4 bg-indigo-50 rounded-lg">
                              <p className="font-medium">Formality</p>
                              <p className="text-2xl text-indigo-600">{user.profile.formality}%</p>
                          </div>
                      </div>
                  </div>
              </div>
          )}

            {/* Career Recommendation Card */}
            {recommendation && (
                <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-2xl font-bold mb-4">Your Career Match</h2>
                    <div className="space-y-4">
                        <div>
                            <p className="text-xl text-indigo-600">
                                {recommendation.career_recommendation}
                            </p>
                            <p className="text-gray-600">
                                Match Rating: {recommendation.recommendation_rating}%
                            </p>
                        </div>

                        {/* Related Courses Section */}
                        {recommendation.related_courses_and_schools?.length > 0 && (
                            <div className="mt-6">
                                <h3 className="text-lg font-semibold mb-3">Related Courses</h3>
                                <div className="space-y-3">
                                    {recommendation.related_courses_and_schools.map((item, index) => (
                                        <div 
                                            key={index}
                                            className="p-4 border rounded-lg hover:bg-gray-50"
                                        >
                                            <p className="font-medium">{item.course}</p>
                                            <p className="text-gray-600">{item.school}</p>
                                            {item.keySkills?.length > 0 && (
                                                <div className="mt-2">
                                                    <p className="text-sm text-gray-500">Key Skills:</p>
                                                    <div className="flex flex-wrap gap-2 mt-1">
                                                        {item.keySkills.map((skill, idx) => (
                                                            <span
                                                                key={idx}
                                                                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                                                            >
                                                                {skill}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button
                        onClick={() => navigate('/assessment')}
                        className="p-4 border rounded-lg hover:bg-gray-50 text-left"
                    >
                        <h3 className="font-medium text-gray-900">Retake Assessment</h3>
                        <p className="text-gray-500 text-sm mt-1">
                            Update your personality profile
                        </p>
                    </button>
                    <button
                        onClick={() => navigate('/skills')}
                        className="p-4 border rounded-lg hover:bg-gray-50 text-left"
                    >
                        <h3 className="font-medium text-gray-900">Update Skills</h3>
                        <p className="text-gray-500 text-sm mt-1">
                            Manage your skill set
                        </p>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;