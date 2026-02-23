import { useEffect, useState } from "react";
import { useAuth } from "../../context/useAuth";
import { saveLocation } from "../../services/api";

export default function DeliveryDashboard() {
  const { user } = useAuth();
  const [locationStatus, setLocationStatus] = useState("Detecting location...");
  const [error, setError] = useState("");

  // -----------------------------
  // SAVE DELIVERY LOCATION
  // -----------------------------
  useEffect(() => {
    if (!user?.access_token) return;

    if (!navigator.geolocation) {
      setError("Geolocation not supported by browser");
      return;
    }

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

          setLocationStatus("Live location synced");
        } catch (err) {
          setError("Failed to save location");
        }
      },
      () => {
        setError("Location permission denied");
        setLocationStatus("Location access required");
      },
      {
        enableHighAccuracy: true,
      }
    );
  }, [user]);

  return (
    <div className="relative min-h-screen text-white">

      {/* BACKGROUND GLOWS */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-[420px] h-[420px] bg-blue-600/25 blur-[140px] rounded-full" />
        <div className="absolute bottom-[-200px] right-[-200px] w-[420px] h-[420px] bg-cyan-500/25 blur-[140px] rounded-full" />

      <div className="relative z-10 max-w-7xl mx-auto space-y-10">

        {/* HEADER */}
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
          <h1 className="text-3xl font-extrabold mb-2">
            Delivery Dashboard
          </h1>
          <p className="text-gray-400">
            Manage assigned pickups and track your delivery status in real time.
          </p>
        </div>

        {/* STATUS CARDS */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">

          {/* LOCATION */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-6">
            <p className="text-sm text-gray-400 mb-1">
              Location Status
            </p>
            <p className="text-lg font-semibold text-cyan-400">
              {locationStatus}
            </p>
          </div>

          {/* AVAILABILITY */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-6">
            <p className="text-sm text-gray-400 mb-1">
              Availability
            </p>
            <p className="text-lg font-semibold text-green-400">
              Online
            </p>
          </div>

          {/* ASSIGNED ORDERS */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-6">
            <p className="text-sm text-gray-400 mb-1">
              Assigned Pickups
            </p>
            <p className="text-lg font-semibold">
              0
            </p>
          </div>

          {/* COMPLETED */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-6">
            <p className="text-sm text-gray-400 mb-1">
              Completed Today
            </p>
            <p className="text-lg font-semibold">
              0
            </p>
          </div>
        </div>

        {/* INFO / NOTE */}
        <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-white/10 rounded-xl p-6">
          <p className="text-sm text-gray-300">
            Your live location helps ScrapX assign nearby pickups efficiently.
            Location data is used strictly for delivery optimization.
          </p>
        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-sm text-red-400">
            {error}
          </div>
        )}
      </div>
    </div>
    </div>
  );
}
