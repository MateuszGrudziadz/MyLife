import { useEffect, useState } from "react";
import api from "../api/client";

export default function Journal() {
  const [entries, setEntries] = useState([]);
  const [summary, setSummary] = useState(null);
  const [editId, setEditId] = useState(null);

  const emptyForm = {
    log_date: new Date().toISOString().slice(0, 10),
    sleep_hours: "",
    energy_level: "",
    mood_level: "",
    productivity_level: "",
    calories_eaten: "",
    caffeine_mg: "",
    journal_text: "",
    gratitude_text: "",
    notes: "",
  };

  const [form, setForm] = useState(emptyForm);
  const [editForm, setEditForm] = useState(emptyForm);

  const fetchData = async () => {
    try {
      const [entriesRes, summaryRes] = await Promise.all([
        api.get("/journal"),
        api.get("/journal/stats/summary"),
      ]);
      setEntries(entriesRes.data);
      setSummary(summaryRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const parseNumber = (value) => {
    if (value === "" || value === null || value === undefined) return null;
    return Number(value);
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await api.post("/journal", {
        ...form,
        sleep_hours: parseNumber(form.sleep_hours),
        energy_level: parseNumber(form.energy_level),
        mood_level: parseNumber(form.mood_level),
        productivity_level: parseNumber(form.productivity_level),
        calories_eaten: parseNumber(form.calories_eaten),
        caffeine_mg: parseNumber(form.caffeine_mg),
      });
      setForm(emptyForm);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się dodać wpisu");
    }
  };

  const startEdit = (entry) => {
    setEditId(entry.id);
    setEditForm({
      log_date: entry.log_date,
      sleep_hours: entry.sleep_hours ?? "",
      energy_level: entry.energy_level ?? "",
      mood_level: entry.mood_level ?? "",
      productivity_level: entry.productivity_level ?? "",
      calories_eaten: entry.calories_eaten ?? "",
      caffeine_mg: entry.caffeine_mg ?? "",
      journal_text: entry.journal_text ?? "",
      gratitude_text: entry.gratitude_text ?? "",
      notes: entry.notes ?? "",
    });
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditForm(emptyForm);
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/journal/${editId}`, {
        ...editForm,
        sleep_hours: parseNumber(editForm.sleep_hours),
        energy_level: parseNumber(editForm.energy_level),
        mood_level: parseNumber(editForm.mood_level),
        productivity_level: parseNumber(editForm.productivity_level),
        calories_eaten: parseNumber(editForm.calories_eaten),
        caffeine_mg: parseNumber(editForm.caffeine_mg),
      });
      cancelEdit();
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się edytować wpisu");
    }
  };

  const removeEntry = async (id) => {
    if (!confirm("Usunąć wpis z dziennika?")) return;
    try {
      await api.delete(`/journal/${id}`);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się usunąć wpisu");
    }
  };

  const statCards = [
    { title: "Wpisy", value: summary?.total_entries ?? 0 },
    { title: "Średni sen", value: `${(summary?.avg_sleep ?? 0).toFixed(1)} h` },
    { title: "Średnia energia", value: `${(summary?.avg_energy ?? 0).toFixed(1)} / 10` },
    { title: "Średni nastrój", value: `${(summary?.avg_mood ?? 0).toFixed(1)} / 10` },
    { title: "Średnia produktywność", value: `${(summary?.avg_productivity ?? 0).toFixed(1)} / 10` },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dziennik / samopoczucie</h1>
        <p className="mt-1 text-gray-500">
          Zapisuj sen, energię, nastrój, kofeinę i krótkie notatki z dnia.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        {statCards.map((card) => (
          <div key={card.title} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">{card.title}</p>
            <h2 className="mt-2 text-2xl font-semibold text-gray-900">{card.value}</h2>
          </div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <form onSubmit={handleAdd} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Dodaj wpis</h2>

          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm text-gray-600">Data</label>
              <input
                type="date"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.log_date}
                onChange={(e) => setForm((prev) => ({ ...prev, log_date: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Sen (h)</label>
              <input
                type="number"
                step="0.1"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.sleep_hours}
                onChange={(e) => setForm((prev) => ({ ...prev, sleep_hours: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Energia (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.energy_level}
                onChange={(e) => setForm((prev) => ({ ...prev, energy_level: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Nastrój (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.mood_level}
                onChange={(e) => setForm((prev) => ({ ...prev, mood_level: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Produktywność (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.productivity_level}
                onChange={(e) => setForm((prev) => ({ ...prev, productivity_level: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Kofeina (mg)</label>
              <input
                type="number"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.caffeine_mg}
                onChange={(e) => setForm((prev) => ({ ...prev, caffeine_mg: e.target.value }))}
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Kalorie zjedzone</label>
              <input
                type="number"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.calories_eaten}
                onChange={(e) => setForm((prev) => ({ ...prev, calories_eaten: e.target.value }))}
              />
            </div>

            <div className="md:col-span-2">
              <label className="mb-1 block text-sm text-gray-600">Dziennik</label>
              <textarea
                rows="4"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.journal_text}
                onChange={(e) => setForm((prev) => ({ ...prev, journal_text: e.target.value }))}
                placeholder="Co się dziś wydarzyło?"
              />
            </div>

            <div className="md:col-span-2">
              <label className="mb-1 block text-sm text-gray-600">Wdzięczność</label>
              <textarea
                rows="3"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.gratitude_text}
                onChange={(e) => setForm((prev) => ({ ...prev, gratitude_text: e.target.value }))}
                placeholder="Za co jesteś dziś wdzięczny?"
              />
            </div>

            <div className="md:col-span-2">
              <label className="mb-1 block text-sm text-gray-600">Notatki</label>
              <textarea
                rows="3"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={form.notes}
                onChange={(e) => setForm((prev) => ({ ...prev, notes: e.target.value }))}
                placeholder="Dodatkowe uwagi"
              />
            </div>
          </div>

          <button className="mt-4 rounded-xl bg-gray-900 px-4 py-3 font-medium text-white transition hover:bg-gray-800">
            Dodaj wpis
          </button>
        </form>

        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Edytuj wpis</h2>

          {editId ? (
            <form onSubmit={handleEdit} className="mt-4 space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <input
                  type="date"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  value={editForm.log_date}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, log_date: e.target.value }))}
                />

                <input
                  type="number"
                  step="0.1"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Sen"
                  value={editForm.sleep_hours}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, sleep_hours: e.target.value }))}
                />

                <input
                  type="number"
                  min="1"
                  max="10"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Energia"
                  value={editForm.energy_level}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, energy_level: e.target.value }))}
                />

                <input
                  type="number"
                  min="1"
                  max="10"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Nastrój"
                  value={editForm.mood_level}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, mood_level: e.target.value }))}
                />

                <input
                  type="number"
                  min="1"
                  max="10"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Produktywność"
                  value={editForm.productivity_level}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, productivity_level: e.target.value }))}
                />

                <input
                  type="number"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Kofeina"
                  value={editForm.caffeine_mg}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, caffeine_mg: e.target.value }))}
                />

                <input
                  type="number"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                  placeholder="Kalorie"
                  value={editForm.calories_eaten}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, calories_eaten: e.target.value }))}
                />
              </div>

              <textarea
                rows="4"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={editForm.journal_text}
                onChange={(e) => setEditForm((prev) => ({ ...prev, journal_text: e.target.value }))}
                placeholder="Dziennik"
              />

              <textarea
                rows="3"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={editForm.gratitude_text}
                onChange={(e) => setEditForm((prev) => ({ ...prev, gratitude_text: e.target.value }))}
                placeholder="Wdzięczność"
              />

              <textarea
                rows="3"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={editForm.notes}
                onChange={(e) => setEditForm((prev) => ({ ...prev, notes: e.target.value }))}
                placeholder="Notatki"
              />

              <div className="flex gap-2">
                <button className="rounded-xl bg-gray-900 px-4 py-3 font-medium text-white">
                  Zapisz
                </button>
                <button
                  type="button"
                  onClick={cancelEdit}
                  className="rounded-xl border border-gray-300 px-4 py-3 font-medium text-gray-700"
                >
                  Anuluj
                </button>
              </div>
            </form>
          ) : (
            <p className="mt-4 text-sm text-gray-500">
              Kliknij „Edytuj” przy wpisie, aby otworzyć formularz.
            </p>
          )}
        </div>
      </div>

      <div className="space-y-4">
        {entries.map((entry) => (
          <div key={entry.id} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {new Date(entry.log_date).toLocaleDateString("pl-PL")}
                </h3>
                <p className="mt-1 text-sm text-gray-600">
                  Sen: {entry.sleep_hours ?? "-"} h | Energia: {entry.energy_level ?? "-"} | Nastrój: {entry.mood_level ?? "-"} | Produktywność: {entry.productivity_level ?? "-"}
                </p>
                <p className="mt-1 text-sm text-gray-600">
                  Kalorie: {entry.calories_eaten ?? "-"} | Kofeina: {entry.caffeine_mg ?? "-"} mg
                </p>

                {entry.journal_text && (
                  <p className="mt-3 text-sm text-gray-700">
                    <span className="font-semibold">Dziennik:</span> {entry.journal_text}
                  </p>
                )}

                {entry.gratitude_text && (
                  <p className="mt-2 text-sm text-gray-700">
                    <span className="font-semibold">Wdzięczność:</span> {entry.gratitude_text}
                  </p>
                )}

                {entry.notes && (
                  <p className="mt-2 text-sm text-gray-700">
                    <span className="font-semibold">Notatki:</span> {entry.notes}
                  </p>
                )}
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => startEdit(entry)}
                  className="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-700"
                >
                  Edytuj
                </button>
                <button
                  onClick={() => removeEntry(entry.id)}
                  className="rounded-lg border border-red-300 px-3 py-1 text-sm text-red-700"
                >
                  Usuń
                </button>
              </div>
            </div>
          </div>
        ))}

        {entries.length === 0 && (
          <p className="text-sm text-gray-500">Brak wpisów w dzienniku.</p>
        )}
      </div>
    </div>
  );
}