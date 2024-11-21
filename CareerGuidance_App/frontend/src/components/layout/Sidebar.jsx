import { Link, useLocation } from 'react-router-dom';
import { Home, User, Briefcase, BookOpen, Star } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

function Sidebar() {
  const location = useLocation();
  
  const navigation = [
    { name: 'Dashboard', icon: Home, href: '/dashboard' },
    { name: 'Assessment', icon: Star, href: '/assessment' },
    { name: 'Skills', icon: BookOpen, href: '/skills' },
    { name: 'Career Path', icon: Briefcase, href: '/career' }
  ];

  const { logout } = useAuth();
  
  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="h-full flex flex-col">
        <div className="flex items-center justify-center h-16 border-b">
          <h1 className="text-xl font-bold text-indigo-600">CareerGuide</h1>
        </div>
        
        <nav className="flex-1 p-4">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-4 py-2 mt-2 text-gray-600 rounded-lg hover:bg-gray-100 ${
                  location.pathname === item.href ? 'bg-gray-100 text-indigo-600' : ''
                }`}
              >
                <Icon className="h-5 w-5" />
                <span className="ml-3">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t">
          <button
            onClick={handleLogout}
            className="flex items-center w-full px-4 py-2 text-gray-600 rounded-lg hover:bg-red-50 hover:text-red-600"
          >
            <User className="h-5 w-5" />
            <span className="ml-3">Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
