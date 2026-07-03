import { useEffect, useState } from "react";
import api from "../api/client";
import StatCard from "../components/StatCard";
import TransactionTable from "../components/TransactionTable";
import CategoryPieChart from "../components/CategoryPieChart";
import MonthlyLineChart from "../components/MonthlyLineChart";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-gray-500">Ładowanie dashboardu...</div>;
  if (!data) return <div className="p-8 text-red-500">Nie udało się pobrać danych.</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">MyLife Dashboard</h1>
        <p className="mt-1 text-gray-500">
          Podsumowanie finansów, przypomnień, samopoczucia i aktywności w jednym miejscu.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Saldo" value={`${data.balance.toFixed(2)} zł`} subtitle="Aktualny stan konta" />
        <StatCard title="Wpływy" value={`${data.income_total.toFixed(2)} zł`} subtitle="Łączne przychody" />
        <StatCard title="Wydatki" value={`${data.expense_total.toFixed(2)} zł`} subtitle="Łączne wydatki" />
        <StatCard
          title="Top kategoria"
          value={data.top_category?.name || "-"}
          subtitle={data.top_category ? `${data.top_category.total.toFixed(2)} zł` : "Brak danych"}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
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
        <StatCard
          title="Aktywne przypomnienia"
          value={`${data.active_reminders_count ?? 0}`}
          subtitle="Nieukończone zadania"
        />
        <StatCard
          title="Wpisy w dzienniku"
          value={`${data.journal_total_entries ?? 0}`}
          subtitle="Łączna liczba wpisów"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Średni sen"
          value={`${Number(data.avg_sleep ?? 0).toFixed(1)} h`}
          subtitle="Z dziennika"
        />
        <StatCard
          title="Średnia energia"
          value={`${Number(data.avg_energy ?? 0).toFixed(1)} / 10`}
          subtitle="Z dziennika"
        />
        <StatCard
          title="Średni nastrój"
          value={`${Number(data.avg_mood ?? 0).toFixed(1)} / 10`}
          subtitle="Z dziennika"
        />
        <StatCard
          title="Średnia produktywność"
          value={`${Number(data.avg_productivity ?? 0).toFixed(1)} / 10`}
          subtitle="Z dziennika"
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <CategoryPieChart data={data.category_breakdown} />
        <MonthlyLineChart data={data.last_6_months} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Przypomnienia</h3>
          <div className="mt-4 space-y-3">
            {data.next_reminder ? (
              <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
                <p className="font-semibold text-gray-900">{data.next_reminder.title}</p>
                <p className="mt-1 text-sm text-gray-600">
                  Najbliższy termin:{" "}
                  {new Date(data.next_reminder.reminder_at).toLocaleString("pl-PL")}
                </p>
              </div>
            ) : (
              <p className="text-sm text-gray-500">Brak aktywnych przypomnień.</p>
            )}

            <p className="text-sm text-gray-500">
              Aktywnych przypomnień: {data.active_reminders_count ?? 0}
            </p>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Ostatni wpis z dziennika</h3>
          <div className="mt-4 space-y-2">
            {data.latest_journal ? (
              <>
                <p className="text-sm text-gray-700">
                  Data: {new Date(data.latest_journal.log_date).toLocaleDateString("pl-PL")}
                </p>
                <p className="text-sm text-gray-700">
                  Energia: {data.latest_journal.energy_level ?? "-"} / 10
                </p>
                <p className="text-sm text-gray-700">
                  Nastrój: {data.latest_journal.mood_level ?? "-"} / 10
                </p>
                <p className="text-sm text-gray-700">
                  Produktywność: {data.latest_journal.productivity_level ?? "-"} / 10
                </p>
              </>
            ) : (
              <p className="text-sm text-gray-500">Brak wpisów w dzienniku.</p>
            )}
          </div>
        </div>
      </div>

      {data.biggest_expense && (
        <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Największy wydatek</h3>
          <p className="mt-2 text-gray-700">
            {data.biggest_expense.amount.toFixed(2)} zł —{" "}
            {data.biggest_expense.description || "bez opisu"}
          </p>
        </div>
      )}

      <TransactionTable transactions={data.recent_transactions || []} />
    </div>
  );
}