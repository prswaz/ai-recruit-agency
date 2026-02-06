import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CompaniesDashboard from './pages/CompaniesDashboard';
import Jobs from './pages/Jobs';
import JobDetail from './pages/JobDetail';
import PostJob from './pages/PostJob';
import Profile from './pages/Profile';
import ResumeUpload from './pages/ResumeUpload';
import Interviews from './pages/Interviews';
import JobApplications from './pages/JobApplications';
import MyApplications from './pages/MyApplications';
import AnalysisHistory from './pages/AnalysisHistory';
import ProtectedRoute from './components/ProtectedRoute';
import { useAuth } from './context/AuthContext';

import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const { loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <ErrorBoundary>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/companies" element={<CompaniesDashboard />} />
              <Route path="/jobs" element={<Jobs />} />
              <Route path="/jobs/:id" element={<JobDetail />} />
              <Route path="/post-job" element={<PostJob />} />
              <Route path="/resume-upload" element={<ResumeUpload />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/analysis-history" element={<AnalysisHistory />} />
              <Route path="/job/:id/applications" element={<JobApplications />} />
              <Route path="/my-applications" element={<MyApplications />} />
              <Route path="/interviews" element={<Interviews />} />
              {/* Add more routes as needed */}
            </Route>
          </Routes>
        </main>
        <Footer />
      </div>
    </ErrorBoundary>
  );
}

export default App;
