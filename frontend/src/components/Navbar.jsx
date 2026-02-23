import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path
      ? "text-cyan-400"
      : "text-gray-300 hover:text-white transition";

  return (
    <nav className="sticky top-0 z-50 bg-[#0b0f1a]/90 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">

        {/* LOGO */}
        <Link
          to="/"
          className="text-2xl font-extrabold tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400"
        >
          ScrapX
        </Link>

        {/* NAV LINKS */}
        <div className="flex items-center gap-8 text-sm font-medium">

          {!user && (
            <>
              <Link to="/about" className={isActive("/about")}>
                About
              </Link>
              <Link to="/features" className={isActive("/features")}>
                Features
              </Link>
              <Link to="/contact" className={isActive("/contact")}>
                Contact
              </Link>
              <Link to="/predict" className={isActive("/predict")}>
                Predict
              </Link>

              <Link
                to="/login"
                className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:opacity-90 transition shadow-md"
              >
                <span className="material-icons-outlined text-base">
                  login
                </span>
                Login
              </Link>
            </>
          )}

          {user && (
            <>
              <Link to="/predict" className={isActive("/predict")}>
                Predict
              </Link>

              {user.role === "user" && (
                <Link to="/dashboard" className={isActive("/dashboard")}>
                  Dashboard
                </Link>
              )}
              {user.role === "admin" && (
                <Link to="/admin" className={isActive("/admin")}>
                  Admin
                </Link>
              )}
              {user.role === "delivery" && (
                <Link to="/delivery" className={isActive("/delivery")}>
                  Delivery
                </Link>
              )}

              <button
                onClick={logout}
                className="flex items-center gap-2 text-red-400 hover:text-red-500 transition"
              >
                <span className="material-icons-outlined text-base">
                  logout
                </span>
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
