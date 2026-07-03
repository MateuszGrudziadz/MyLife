import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Wallet,
  Bell,
  NotebookPen,
  Target,
  LogOut,
} from "lucide-react";
import { setAuthToken } from "../api/client";

const items = [
  { label: "Dashboard", to: "/", icon: LayoutDashboard },
  { label: "Wydatki", to: "/expenses", icon: Wallet },
  { label: "Przypomnienia", to: "/reminders", icon: Bell },
  { label: "Dziennik", to: "/journal", icon: NotebookPen },
  { label: "Cele", to: "/goals", icon: Target },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setAuthToken(null);
    navigate("/login");
  };

  return (
    <aside className="w-full border-b bg-white p-4 md:flex md:h-screen md:w-72 md:flex-col md:border-b-0 md:border-r">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">MyLife</h1>
        <p className="mt-1 text-sm text-gray-500">Twoje życie w jednym miejscu</p>
      </div>

      {user?.email && (
        <div className="mt-6 rounded-2xl bg-gray-50 p-4 text-sm text-gray-700">
          Zalogowany: <span className="font-semibold">{user.email}</span>
        </div>
      )}

      <nav className="mt-8 space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.label}
              to={item.to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-xl px-4 py-3 text-left transition",
                  isActive ? "bg-gray-900 text-white" : "text-gray-700 hover:bg-gray-100",
                ].join(" ")
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <button
        onClick={handleLogout}
        className="mt-auto flex items-center gap-3 rounded-xl px-4 py-3 text-left text-gray-700 hover:bg-gray-100"
      >
        <LogOut size={18} />
        <span>Wyloguj</span>
      </button>
    </aside>
  );
}