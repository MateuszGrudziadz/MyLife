export default function TransactionTable({ transactions }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900">Ostatnie transakcje</h3>

      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b text-sm text-gray-500">
              <th className="py-3">ID</th>
              <th>Typ</th>
              <th>Kwota</th>
              <th>Opis</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id} className="border-b last:border-b-0 text-sm">
                <td className="py-3">{t.id}</td>
                <td>{t.transaction_type}</td>
                <td>{Number(t.amount).toFixed(2)} zł</td>
                <td>{t.description || "-"}</td>
                <td>{new Date(t.created_at).toLocaleString("pl-PL")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}