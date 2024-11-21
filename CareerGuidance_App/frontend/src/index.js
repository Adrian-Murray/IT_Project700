import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // Make sure this import is here
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

export const Button = ({ children, variant = 'primary', ...props }) => {
    const baseClass = variant === 'primary' ? 'btn-primary' : 'btn-secondary';
    return (
      <button className={baseClass} {...props}>
        {children}
      </button>
    );
  };
  
  // Input components
  export const Input = ({ error, label, ...props }) => {
    return (
      <div className="form-group">
        {label && <label className="form-label">{label}</label>}
        <input className="input" {...props} />
        {error && <p className="form-error">{error}</p>}
      </div>
    );
  };
  
  // Alert component
  export const Alert = ({ children, variant = 'info' }) => {
    return (
      <div className={`alert-${variant}`}>
        {children}
      </div>
    );
  };
  
  // Card component
  export const Card = ({ children, title }) => {
    return (
      <div className="card">
        {title && (
          <div className="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              {title}
            </h3>
          </div>
        )}
        <div className="card-body">
          {children}
        </div>
      </div>
    );
  };