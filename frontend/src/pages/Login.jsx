import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { setAuthToken } from "../api/client";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/auth/login", form);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      setAuthToken(data.access_token);
      navigate("/");
    } catch (error) {
      alert(error.response?.data?.detail || "Nie udało się zalogować");
    }
  };

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-gray-50 px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-gray-900">Logowanie</h1>
        <p className="mt-2 text-sm text-gray-500">Zaloguj się do MyLife.</p>

        <div className="mt-6 space-y-4">
          <div>
            <label className="mb-1 block text-sm text-gray-600">E-mail</label>
            <input
              type="email"
              className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={form.email}
              onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm text-gray-600">Hasło</label>
            <input
              type="password"
              className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-gray-900"
              value={form.password}
              onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
            />
          </div>

          <button className="w-full rounded-xl bg-gray-900 px-4 py-3 font-medium text-white hover:bg-gray-800">
            Zaloguj się
          </button>
        </div>

        <p className="mt-4 text-sm text-gray-500">
          Nie masz konta?{" "}
          <Link to="/register" className="font-semibold text-gray-900">
            Zarejestruj się
          </Link>
        </p>
      </form>
    </div>
  );
}