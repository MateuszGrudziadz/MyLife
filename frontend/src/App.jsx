import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 md:flex">
      <Sidebar />
      <main className="flex-1 p-6 md:p-8">
        <Dashboard />
      </main>
    </div>
  );
}