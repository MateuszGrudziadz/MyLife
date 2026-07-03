import { useEffect, useState } from "react";
import api from "../api/client";

const normalizeTypeLabel = (type) => {
  if (type === "wplata" || type === "income") return "Wpłata";
  if (type === "wydatek" || type === "expense") return "Wydatek";
  return type;
};

const isIncomeType = (type) => type === "wplata" || type === "income";
const isExpenseType = (type) => type === "wydatek" || type === "expense";

export default function Expenses() {
  const [categories, setCategories] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState(0);

  const [categoryForm, setCategoryForm] = useState({
    name: "",
    kind: "wydatek",
  });

  const [transactionForm, setTransactionForm] = useState({
    transaction_type: "wydatek",
    amount: "",
    description: "",
    category_id: "",
  });

  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({
    transaction_type: "wydatek",
    amount: "",
    description: "",
    category_id: "",
  });

  const fetchData = async () => {
    try {
      const [catRes, txRes, balanceRes] = await Promise.all([
        api.get("/expenses/categories"),
        api.get("/expenses/transactions"),
        api.get("/expenses/balance"),
      ]);

      setCategories(catRes.data);
      setTransactions(txRes.data);
      setBalance(balanceRes.data.balance);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddCategory = async (e) => {
    e.preventDefault();
    try {
      await api.post("/expenses/categories", categoryForm);
      setCategoryForm({ name: "", kind: "wydatek" });
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się dodać kategorii");
    }
  };

  const handleAddTransaction = async (e) => {
    e.preventDefault();
    try {
      await api.post("/expenses/transactions", {
        ...transactionForm,
        amount: Number(transactionForm.amount),
        category_id: transactionForm.category_id ? Number(transactionForm.category_id) : null,
      });

      setTransactionForm({
        transaction_type: "wydatek",
        amount: "",
        description: "",
        category_id: "",
      });

      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się dodać transakcji");
    }
  };

  const startEdit = (transaction) => {
    setEditId(transaction.id);
    setEditForm({
      transaction_type: isIncomeType(transaction.transaction_type) ? "wplata" : "wydatek",
      amount: String(transaction.amount),
      description: transaction.description || "",
      category_id: transaction.category_id ? String(transaction.category_id) : "",
    });
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditForm({
      transaction_type: "wydatek",
      amount: "",
      description: "",
      category_id: "",
    });
  };

  const handleUpdateTransaction = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/expenses/transactions/${editId}`, {
        ...editForm,
        amount: Number(editForm.amount),
        category_id: editForm.category_id ? Number(editForm.category_id) : null,
      });
      cancelEdit();
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się edytować transakcji");
    }
  };

  const handleDeleteTransaction = async (id) => {
    if (!confirm("Na pewno usunąć transakcję?")) return;

    try {
      await api.delete(`/expenses/transactions/${id}`);
      fetchData();
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się usunąć transakcji");
    }
  };

  const visibleCategories = categories.filter((c) => {
    if (transactionForm.transaction_type === "wplata") {
      return isIncomeType(c.kind);
    }
    return isExpenseType(c.kind);
  });

  const editVisibleCategories = categories.filter((c) => {
    if (editForm.transaction_type === "wplata") {
      return isIncomeType(c.kind);
    }
    return isExpenseType(c.kind);
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Wydatki</h1>
        <p className="mt-1 text-gray-500">Dodawaj kategorie i transakcje oraz śledź saldo.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">Aktualne saldo</p>
          <h2 className="mt-2 text-3xl font-bold text-gray-900">
            {Number(balance).toFixed(2)} zł
          </h2>
        </div>

        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">Liczba kategorii</p>
          <h2 className="mt-2 text-3xl font-bold text-gray-900">{categories.length}</h2>
        </div>

        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">Liczba transakcji</p>
          <h2 className="mt-2 text-3xl font-bold text-gray-900">{transactions.length}</h2>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <form
          onSubmit={handleAddCategory}
          className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"
        >
          <h2 className="text-xl font-semibold text-gray-900">Dodaj kategorię</h2>

          <div className="mt-4 space-y-4">
            <div>
              <label className="mb-1 block text-sm text-gray-600">Nazwa</label>
              <input
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={categoryForm.name}
                onChange={(e) =>
                  setCategoryForm((prev) => ({ ...prev, name: e.target.value }))
                }
                placeholder="np. Jedzenie"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Typ</label>
              <select
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={categoryForm.kind}
                onChange={(e) =>
                  setCategoryForm((prev) => ({ ...prev, kind: e.target.value }))
                }
              >
                <option value="wydatek">Wydatek</option>
                <option value="wplata">Wpłata</option>
              </select>
            </div>

            <button className="rounded-xl bg-gray-900 px-4 py-3 font-medium text-white transition hover:bg-gray-800">
              Dodaj kategorię
            </button>
          </div>
        </form>

        <form
          onSubmit={handleAddTransaction}
          className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"
        >
          <h2 className="text-xl font-semibold text-gray-900">Dodaj transakcję</h2>

          <div className="mt-4 space-y-4">
            <div>
              <label className="mb-1 block text-sm text-gray-600">Typ</label>
              <select
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={transactionForm.transaction_type}
                onChange={(e) =>
                  setTransactionForm((prev) => ({
                    ...prev,
                    transaction_type: e.target.value,
                  }))
                }
              >
                <option value="wydatek">Wydatek</option>
                <option value="wplata">Wpłata</option>
              </select>
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Kwota</label>
              <input
                type="number"
                step="0.01"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={transactionForm.amount}
                onChange={(e) =>
                  setTransactionForm((prev) => ({ ...prev, amount: e.target.value }))
                }
                placeholder="np. 120.50"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Opis</label>
              <input
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={transactionForm.description}
                onChange={(e) =>
                  setTransactionForm((prev) => ({
                    ...prev,
                    description: e.target.value,
                  }))
                }
                placeholder="np. Zakupy spożywcze"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm text-gray-600">Kategoria</label>
              <select
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
                value={transactionForm.category_id}
                onChange={(e) =>
                  setTransactionForm((prev) => ({
                    ...prev,
                    category_id: e.target.value,
                  }))
                }
              >
                <option value="">-- wybierz --</option>
                {visibleCategories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name} ({normalizeTypeLabel(category.kind)})
                  </option>
                ))}
              </select>
            </div>

            <button className="rounded-xl bg-gray-900 px-4 py-3 font-medium text-white transition hover:bg-gray-800">
              Dodaj transakcję
            </button>
          </div>
        </form>
      </div>

      <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900">Kategorie</h2>
        <div className="mt-4 flex flex-wrap gap-2">
          {categories.map((cat) => (
            <span
              key={cat.id}
              className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700"
            >
              {cat.name} ({normalizeTypeLabel(cat.kind)})
            </span>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900">Edytuj transakcję</h2>

        {editId ? (
          <form onSubmit={handleUpdateTransaction} className="mt-4 grid gap-4 lg:grid-cols-5">
            <select
              className="rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={editForm.transaction_type}
              onChange={(e) =>
                setEditForm((prev) => ({ ...prev, transaction_type: e.target.value }))
              }
            >
              <option value="wydatek">Wydatek</option>
              <option value="wplata">Wpłata</option>
            </select>

            <input
              type="number"
              step="0.01"
              className="rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={editForm.amount}
              onChange={(e) =>
                setEditForm((prev) => ({ ...prev, amount: e.target.value }))
              }
            />

            <input
              className="rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={editForm.description}
              onChange={(e) =>
                setEditForm((prev) => ({ ...prev, description: e.target.value }))
              }
            />

            <select
              className="rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={editForm.category_id}
              onChange={(e) =>
                setEditForm((prev) => ({ ...prev, category_id: e.target.value }))
              }
            >
              <option value="">-- wybierz --</option>
              {editVisibleCategories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name} ({normalizeTypeLabel(category.kind)})
                </option>
              ))}
            </select>

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
          <p className="mt-3 text-sm text-gray-500">
            Kliknij „Edytuj” przy transakcji, aby otworzyć formularz.
          </p>
        )}
      </div>

      <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900">Transakcje</h2>

        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b text-sm text-gray-500">
                <th className="py-3">ID</th>
                <th>Typ</th>
                <th>Kwota</th>
                <th>Opis</th>
                <th>Data</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t) => (
                <tr key={t.id} className="border-b last:border-b-0 text-sm">
                  <td className="py-3">{t.id}</td>
                  <td>{normalizeTypeLabel(t.transaction_type)}</td>
                  <td>{Number(t.amount).toFixed(2)} zł</td>
                  <td>{t.description || "-"}</td>
                  <td>{new Date(t.created_at).toLocaleString("pl-PL")}</td>
                  <td className="py-3">
                    <div className="flex gap-2">
                      <button
                        onClick={() => startEdit(t)}
                        className="rounded-lg border border-gray-300 px-3 py-1 text-sm text-gray-700"
                      >
                        Edytuj
                      </button>
                      <button
                        onClick={() => handleDeleteTransaction(t.id)}
                        className="rounded-lg border border-red-300 px-3 py-1 text-sm text-red-700"
                      >
                        Usuń
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}