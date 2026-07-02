export default function StatCard({ title, value, subtitle }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm border border-gray-200">
      <p className="text-sm text-gray-500">{title}</p>
      <h2 className="mt-2 text-2xl font-semibold text-gray-900">{value}</h2>
      {subtitle && <p className="mt-1 text-sm text-gray-400">{subtitle}</p>}
    </div>
  );
}