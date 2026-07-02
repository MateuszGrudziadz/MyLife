import { useEffect, useState } from "react";
import api from "../api/client";
import StatCard from "../components/StatCard";
import TransactionTable from "../components/TransactionTable";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/summary")
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-gray-500">Ładowanie dashboardu...</div>;
  }

  if (!data) {
    return <div className="p-8 text-red-500">Nie udało się pobrać danych.</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">MyLife Dashboard</h1>
        <p className="mt-1 text-gray-500">
          Podsumowanie finansów i aktywności w jednym miejscu.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Saldo" value={`${data.balance.toFixed(2)} zł`} subtitle="Aktualny stan konta" />
        <StatCard title="Wpływy" value={`${data.income_total.toFixed(2)} zł`} subtitle="Łączne przychody" />
        <StatCard title="Wydatki" value={`${data.expense_total.toFixed(2)} zł`} subtitle="Łączne wydatki" />
        <StatCard title="Top kategoria" value={data.top_category?.name || "-"} subtitle={data.top_category ? `${data.top_category.total.toFixed(2)} zł` : "Brak danych"} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <StatCard
          title="Wydatki w tym miesiącu"
          value={`${data.monthly_expense.toFixed(2)} zł`}
          subtitle="Bieżący miesiąc"
        />
        <StatCard
          title="Wpływy w tym miesiącu"
          value={`${data.monthly_income.toFixed(2)} zł`}
          subtitle="Bieżący miesiąc"
        />
      </div>

      {data.biggest_expense && (
        <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Największy wydatek</h3>
          <p className="mt-2 text-gray-700">
            {data.biggest_expense.amount.toFixed(2)} zł — {data.biggest_expense.description || "bez opisu"}
          </p>
        </div>
      )}

      <TransactionTable transactions={data.recent_transactions || []} />
    </div>
  );
}