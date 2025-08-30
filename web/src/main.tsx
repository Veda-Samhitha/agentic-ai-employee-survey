import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Protected from "./components/Protected";
import Login from "./pages/Login";
import EmployeeSurveys from "./pages/EmployeeSurveys";
import TakeSurvey from "./pages/TakeSurvey";
import AdminDashboard from "./pages/AdminDashboard";
import AdminSurveys from "./pages/AdminSurveys";
import NewSurvey from "./pages/NewSurvey";
import SurveyResults from "./pages/SurveyResults";
import Analytics from "./pages/Analytics";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Employee */}
        <Route path="/employee/surveys" element={
          <Protected allow={["employee"]}><EmployeeSurveys /></Protected>
        } />
        <Route path="/employee/surveys/:id/take" element={
          <Protected allow={["employee"]}><TakeSurvey /></Protected>
        } />

        {/* Admin */}
        <Route path="/admin/dashboard" element={
          <Protected allow={["admin"]}><AdminDashboard /></Protected>
        } />
        <Route path="/admin/surveys" element={
          <Protected allow={["admin"]}><AdminSurveys /></Protected>
        } />
        <Route path="/admin/surveys/new" element={
          <Protected allow={["admin"]}><NewSurvey /></Protected>
        } />
        <Route path="/admin/surveys/:id/results" element={
          <Protected allow={["admin"]}><SurveyResults /></Protected>
        } />
        <Route path="/admin/analytics" element={
          <Protected allow={["admin"]}><Analytics /></Protected>
        } />

        {/* default → login */}
        <Route path="*" element={<Login />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
