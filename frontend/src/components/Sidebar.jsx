import { LayoutDashboard, Wallet, Bell, NotebookPen, Target } from "lucide-react";

export default function Sidebar() {
  const items = [
    { label: "Dashboard", icon: LayoutDashboard },
    { label: "Wydatki", icon: Wallet },
    { label: "Przypomnienia", icon: Bell },
    { label: "Dziennik", icon: NotebookPen },
    { label: "Cele", icon: Target },
  ];

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
            <button
              key={item.label}
              className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-gray-700 hover:bg-gray-100"
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}