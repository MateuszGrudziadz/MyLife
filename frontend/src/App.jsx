import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Expenses from "./pages/Expenses";
import Reminders from "./pages/Reminders";
import Journal from "./pages/Journal";

function Placeholder({ title }) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
      <p className="mt-2 text-gray-500">Work in progress</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route path="/journal" element={<Journal />} />
          <Route path="/goals" element={<Placeholder title="Cele" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}