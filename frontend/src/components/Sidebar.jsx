import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function Sidebar({ role }) {
  const { logout } = useAuth();
  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path
      ? "bg-white/10 text-cyan-400"
      : "text-gray-400 hover:text-white";

  const userMenu = [
    { label: "Dashboard", path: "/dashboard", icon: "dashboard" },
    { label: "Predict", path: "/dashboard/predict", icon: "psychology" },
    { label: "Orders", path: "/dashboard/orders", icon: "receipt_long" },
    { label: "Profile", path: "/dashboard/profile", icon: "person" },
  ];

  const menu = role === "user" ? userMenu : [];

  return (
    <aside className="w-64 bg-black/40 border-r border-white/10 flex flex-col">
      <div className="p-6 text-2xl font-bold text-cyan-400">
        ScrapX
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {menu.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${isActive(
              item.path
            )}`}
          >
            <span className="material-icons-outlined">
              {item.icon}
            </span>
            {item.label}
          </Link>
        ))}
      </nav>

      <button
        onClick={logout}
        className="m-4 flex items-center gap-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-500/10 transition"
      >
        <span className="material-icons-outlined">logout</span>
        Logout
      </button>
    </aside>
  );
}
