import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Wallet,
  Bell,
  NotebookPen,
  Target,
} from "lucide-react";

const items = [
  { label: "Dashboard", to: "/", icon: LayoutDashboard },
  { label: "Wydatki", to: "/expenses", icon: Wallet },
  { label: "Przypomnienia", to: "/reminders", icon: Bell },
  { label: "Dziennik", to: "/journal", icon: NotebookPen },
  { label: "Cele", to: "/goals", icon: Target },
];

export default function Sidebar() {
  return (
    <aside className="w-full border-b bg-white p-4 md:h-screen md:w-72 md:border-b-0 md:border-r">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">MyLife</h1>
        <p className="mt-1 text-sm text-gray-500">Twoje życie w jednym miejscu</p>
      </div>

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
                  isActive
                    ? "bg-gray-900 text-white"
                    : "text-gray-700 hover:bg-gray-100",
                ].join(" ")
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}