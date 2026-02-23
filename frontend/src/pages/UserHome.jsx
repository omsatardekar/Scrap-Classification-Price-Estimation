import { Link } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { useAuth } from "../context/useAuth";
import { saveLocation } from "../services/api";

const API_BASE = "http://127.0.0.1:8000";

export default function UserHome() {
  const { user } = useAuth();

  const [orders, setOrders] = useState([]);
  const [aiStatus, setAiStatus] = useState("Checking...");
  const [loading, setLoading] = useState(true);

  /* =========================================
     SAVE USER LOCATION (ONCE)
  ========================================= */
  useEffect(() => {
    if (!user?.access_token) return;

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          await saveLocation(
            {
              latitude: pos.coords.latitude,
              longitude: pos.coords.longitude,
            },
            user.access_token
          );
        } catch {
          console.error("Failed to save location");
        }
      },
      () => {
        console.warn("Location permission denied");
      },
      {
        enableHighAccuracy: true,
        maximumAge: 1000 * 60 * 60,
      }
    );
  }, [user]);

  /* =========================================
     FETCH USER ORDERS
  ========================================= */
  const fetchOrders = useCallback(async () => {
    if (!user?.access_token) return;

    try {
      const res = await fetch(`${API_BASE}/orders/my`, {
        headers: {
          Authorization: `Bearer ${user.access_token}`,
        },
      });

      if (!res.ok) throw new Error();
      const data = await res.json();
      setOrders(data);
    } catch {
      console.error("Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  }, [user]);

  /* =========================================
     CHECK AI ENGINE STATUS
  ========================================= */
  const checkAiStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/`);
      if (res.ok) {
        setAiStatus("Online");
      } else {
        setAiStatus("Offline");
      }
    } catch {
      setAiStatus("Offline");
    }
  };

  useEffect(() => {
    fetchOrders();
    checkAiStatus();

    const interval = setInterval(fetchOrders, 5000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  /* =========================================
     DERIVED METRICS
  ========================================= */

  const activeOrders = orders.filter((o) =>
    ["assigned", "collected"].includes(o.status)
  ).length;

  const completedOrders = orders.filter(
    (o) => o.status === "completed"
  ).length;

  const totalEarnings = orders
    .filter((o) => o.status === "completed")
    .reduce((sum, o) => sum + (o.estimated_price || 0), 0);

  const lastPrediction = orders.length
    ? `${orders[0].material} (₹${orders[0].estimated_price})`
    : "—";

  /* ========================================= */

  return (
    <div className="space-y-10">

      {/* ================= WELCOME ================= */}
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
        <h1 className="text-3xl font-extrabold mb-2">
          Welcome back 👋
        </h1>
        <p className="text-gray-400">
          Logged in as{" "}
          <span className="text-cyan-400 font-medium">
            {user?.email}
          </span>
        </p>
      </div>

      {/* ================= QUICK ACTIONS ================= */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Quick Actions
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">

          <Link
            to="/dashboard/predict"
            className="group bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-400 transition"
          >
            <span className="material-icons-outlined text-4xl text-cyan-400 mb-4 block">
              psychology
            </span>
            <h3 className="text-lg font-semibold mb-1">
              Predict Scrap Price
            </h3>
            <p className="text-sm text-gray-400">
              Upload scrap image and estimate value using AI
            </p>
          </Link>

          <Link
            to="/dashboard/orders"
            className="group bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-400 transition"
          >
            <span className="material-icons-outlined text-4xl text-cyan-400 mb-4 block">
              receipt_long
            </span>
            <h3 className="text-lg font-semibold mb-1">
              My Orders
            </h3>
            <p className="text-sm text-gray-400">
              Track status of your scrap pickup orders
            </p>
          </Link>

          <Link
            to="/dashboard/profile"
            className="group bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-400 transition"
          >
            <span className="material-icons-outlined text-4xl text-cyan-400 mb-4 block">
              person
            </span>
            <h3 className="text-lg font-semibold mb-1">
              Profile Settings
            </h3>
            <p className="text-sm text-gray-400">
              Manage your account and payout details
            </p>
          </Link>

        </div>
      </div>

      {/* ================= LIVE STATS ================= */}
      <div className="grid md:grid-cols-4 gap-6">

        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h4 className="text-sm text-gray-400 mb-1">
            AI Engine Status
          </h4>
          <p
            className={`text-xl font-bold ${
              aiStatus === "Online"
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            {aiStatus}
          </p>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h4 className="text-sm text-gray-400 mb-1">
            Active Orders
          </h4>
          <p className="text-xl font-bold text-cyan-400">
            {loading ? "..." : activeOrders}
          </p>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h4 className="text-sm text-gray-400 mb-1">
            Completed Orders
          </h4>
          <p className="text-xl font-bold text-green-400">
            {loading ? "..." : completedOrders}
          </p>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-xl p-6">
          <h4 className="text-sm text-gray-400 mb-1">
            Total Earnings
          </h4>
          <p className="text-xl font-bold text-emerald-400">
            ₹ {loading ? "..." : totalEarnings}
          </p>
        </div>

      </div>

      {/* ================= LAST ACTIVITY ================= */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-6">
        <h4 className="text-sm text-gray-400 mb-2">
          Last Prediction
        </h4>
        <p className="text-lg font-semibold">
          {loading ? "Loading..." : lastPrediction}
        </p>
      </div>

      {/* ================= INFO NOTE ================= */}
      <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-white/10 rounded-xl p-6">
        <p className="text-sm text-gray-300">
          ScrapX uses artificial intelligence and smart logistics to ensure
          transparent pricing and efficient scrap pickup. Your location is used
          only to assign nearby delivery agents and is never shared publicly.
        </p>
      </div>

    </div>
  );
}
