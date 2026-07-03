import { useEffect, useState } from "react";
import api from "../api/client";

export default function Reminders() {
  const [reminders, setReminders] = useState([]);
  const [summary, setSummary] = useState(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    reminder_at: "",
  });

  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({
    title: "",
    description: "",
    reminder_at: "",
    is_done: false,
  });

  const fetchData = async () => {
    try {
      const [remindersRes, summaryRes] = await Promise.all([
        api.get("/reminders"),
        api.get("/reminders/stats/summary"),
      ]);

      setReminders(remindersRes.data);
      setSummary(summaryRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await api.post("/reminders", {
        ...form,
        reminder_at: new Date(form.reminder_at).toISOString(),
      });
      setForm({ title: "", description: "", reminder_at: "" });
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się dodać przypomnienia");
    }
  };

  const startEdit = (reminder) => {
    setEditId(reminder.id);
    setEditForm({
      title: reminder.title,
      description: reminder.description || "",
      reminder_at: reminder.reminder_at.slice(0, 16),
      is_done: reminder.is_done,
    });
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/reminders/${editId}`, {
        ...editForm,
        reminder_at: new Date(editForm.reminder_at).toISOString(),
      });
      setEditId(null);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się edytować przypomnienia");
    }
  };

  const markDone = async (id) => {
    try {
      await api.patch(`/reminders/${id}/done`);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się oznaczyć jako wykonane");
    }
  };

  const removeReminder = async (id) => {
    if (!confirm("Usunąć przypomnienie?")) return;
    try {
      await api.delete(`/reminders/${id}`);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się usunąć przypomnienia");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Przypomnienia</h1>
        <p className="mt-1 text-gray-500">Zarządzaj ważnymi zadaniami i terminami.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">Aktywne przypomnienia</p>
          <h2 className="mt-2 text-3xl font-bold text-gray-900">
            {summary?.active_count ?? 0}
          </h2>
        </div>

        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">Najbliższe przypomnienie</p>
          <h2 className="mt-2 text-xl font-semibold text-gray-900">
            {summary?.next_reminder?.title || "-"}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            {summary?.next_reminder?.reminder_at
              ? new Date(summary.next_reminder.reminder_at).toLocaleString("pl-PL")
              : "Brak danych"}
          </p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <form onSubmit={handleAdd} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Dodaj przypomnienie</h2>

          <div className="mt-4 space-y-4">
            <input
              className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              placeholder="Tytuł"
              value={form.title}
              onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
            />

            <textarea
              className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              placeholder="Opis"
              rows="4"
              value={form.description}
              onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
            />

            <input
              type="datetime-local"
              className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={form.reminder_at}
              onChange={(e) => setForm((prev) => ({ ...prev, reminder_at: e.target.value }))}
            />

            <button className="rounded-xl bg-gray-900 px-4 py-3 font-medium text-white transition hover:bg-gray-800">
              Dodaj przypomnienie
            </button>
          </div>
        </form>

        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Edytuj przypomnienie</h2>

          {editId ? (
            <form onSubmit={handleEdit} className="mt-4 space-y-4">
              <input
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={editForm.title}
                onChange={(e) => setEditForm((prev) => ({ ...prev, title: e.target.value }))}
              />

              <textarea
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                rows="4"
                value={editForm.description}
                onChange={(e) => setEditForm((prev) => ({ ...prev, description: e.target.value }))}
              />

              <input
                type="datetime-local"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={editForm.reminder_at}
                onChange={(e) => setEditForm((prev) => ({ ...prev, reminder_at: e.target.value }))}
              />

              <label className="flex items-center gap-2 text-sm text-gray-700">
                <input
                  type="checkbox"
                  checked={editForm.is_done}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, is_done: e.target.checked }))}
                />
                Wykonane
              </label>

              <div className="flex gap-2">
                <button className="rounded-xl bg-gray-900 px-4 py-3 font-medium text-white">
                  Zapisz
                </button>
                <button
                  type="button"
                  onClick={() => setEditId(null)}
                  className="rounded-xl border border-gray-300 px-4 py-3 font-medium text-gray-700"
                >
                  Anuluj
                </button>
              </div>
            </form>
          ) : (
            <p className="mt-4 text-sm text-gray-500">
              Wybierz „Edytuj” przy przypomnieniu, aby otworzyć formularz.
            </p>
          )}
        </div>
      </div>

      <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900">Lista przypomnień</h2>

        <div className="mt-4 space-y-3">
          {reminders.map((reminder) => (
            <div
              key={reminder.id}
              className={`rounded-xl border p-4 ${
                reminder.is_done ? "border-gray-200 bg-gray-50" : "border-gray-300 bg-white"
              }`}
            >
              <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {reminder.is_done ? "✔ " : ""}
                    {reminder.title}
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">{reminder.description || "Brak opisu"}</p>
                  <p className="mt-2 text-sm text-gray-500">
                    Termin: {new Date(reminder.reminder_at).toLocaleString("pl-PL")}
                  </p>
                </div>

                <div className="flex gap-2">
                  {!reminder.is_done && (
                    <button
                      onClick={() => markDone(reminder.id)}
                      className="rounded-lg border border-green-300 px-3 py-1 text-sm text-green-700"
                    >
                      Wykonane
                    </button>
                  )}
                  <button
                    onClick={() => startEdit(reminder)}
                    className="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-700"
                  >
                    Edytuj
                  </button>
                  <button
                    onClick={() => removeReminder(reminder.id)}
                    className="rounded-lg border border-red-300 px-3 py-1 text-sm text-red-700"
                  >
                    Usuń
                  </button>
                </div>
              </div>
            </div>
          ))}

          {reminders.length === 0 && (
            <p className="text-sm text-gray-500">Brak przypomnień.</p>
          )}
        </div>
      </div>
    </div>
  );
}