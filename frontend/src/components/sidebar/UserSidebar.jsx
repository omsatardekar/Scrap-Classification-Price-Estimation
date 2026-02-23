import { NavLink } from "react-router-dom";

export default function UserSidebar({ onLogout }) {
  return (
    <div className="h-full flex flex-col">

      {/* LOGO */}
      <div className="px-6 py-6 text-2xl font-extrabold tracking-wide text-cyan-400">
        ScrapX
      </div>

      {/* NAVIGATION */}
      <nav className="flex-1 px-4 space-y-2">

        <NavLink
          to="/dashboard"
          end
          className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              isActive
                ? "bg-cyan-500/15 text-cyan-400"
                : "text-gray-400 hover:bg-white/5 hover:text-white"
            }`
          }
        >
          <span className="material-icons-outlined text-xl">dashboard</span>
          Dashboard
        </NavLink>

        <NavLink
          to="/dashboard/predict"
          className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              isActive
                ? "bg-cyan-500/15 text-cyan-400"
                : "text-gray-400 hover:bg-white/5 hover:text-white"
            }`
          }
        >
          <span className="material-icons-outlined text-xl">psychology</span>
          Predict
        </NavLink>

        <NavLink
          to="/dashboard/orders"
          className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              isActive
                ? "bg-cyan-500/15 text-cyan-400"
                : "text-gray-400 hover:bg-white/5 hover:text-white"
            }`
          }
        >
          <span className="material-icons-outlined text-xl">inventory_2</span>
          Orders
        </NavLink>

        <NavLink
          to="/dashboard/profile"
          className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              isActive
                ? "bg-cyan-500/15 text-cyan-400"
                : "text-gray-400 hover:bg-white/5 hover:text-white"
            }`
          }
        >
          <span className="material-icons-outlined text-xl">person</span>
          Profile
        </NavLink>

      </nav>

      {/* LOGOUT (BOTTOM FIXED) */}
      <div className="p-4 border-t border-white/10">
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-500/10 transition"
        >
          <span className="material-icons-outlined text-xl">logout</span>
          Logout
        </button>
      </div>

    </div>
  );
}
