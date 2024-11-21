import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function ProtectedRoute() {
    const { user, loading } = useAuth();
    const location = useLocation();
    
    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
            </div>
        );
    }
    
    // Not logged in
    if (!user) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }
    
    // No profile (assessment not completed) and not on assessment page
    if (!user.profile && location.pathname !== '/assessment') {
        return <Navigate to="/assessment" replace />;
    }
    
    // Assessment completed but no skills and not on skills page
    if (user.profile && (!user.skills || user.skills.length === 0) && 
        location.pathname !== '/skills') {
        return <Navigate to="/skills" replace />;
    }
    
    return <Outlet />;
}

export default ProtectedRoute;