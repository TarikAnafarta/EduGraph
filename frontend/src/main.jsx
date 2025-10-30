import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './ui/AppLayout.jsx'
import Login from './views/auth/Login.jsx'
import Register from './views/auth/Register.jsx'
import Verify from './views/auth/Verify.jsx'
import CompleteProfile from './views/auth/CompleteProfile.jsx'
import Dashboard from './views/home/Dashboard.jsx'
import Profile from './views/settings/Profile.jsx'
import Graph from './views/graph/Graph.jsx'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}> 
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify" element={<Verify />} />
          <Route path="/complete-profile" element={<CompleteProfile />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/graph" element={<Graph />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
