import { useState } from "react";
import { useAuth } from "../../context/useAuth";

const API_BASE = "http://127.0.0.1:8000";

export default function AdminProfile() {
  const { user } = useAuth();

  const [email, setEmail] = useState(user?.email || "");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    if (!currentPassword) {
      setError("Current password is required");
      return;
    }

    if (newPassword && newPassword.length < 6) {
      setError("New password must be at least 6 characters");
      return;
    }

    if (newPassword && newPassword !== confirmPassword) {
      setError("New passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/users/profile`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.access_token}`,
        },
        body: JSON.stringify({
          email,
          current_password: currentPassword,
          new_password: newPassword || null,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Update failed");
      }

      setMessage("Admin profile updated successfully");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#0b0f1a] text-white overflow-hidden">

      {/* Background Glow */}
      <div className="absolute -top-40 -left-40 w-[420px] h-[420px] bg-blue-600/25 blur-[140px] rounded-full" />
      <div className="absolute bottom-[-200px] right-[-200px] w-[420px] h-[420px] bg-cyan-500/25 blur-[140px] rounded-full" />

      <section className="relative z-10 max-w-4xl mx-auto px-6 pt-20 pb-24">

        {/* Header */}
        <div className="mb-14">
          <h1 className="text-5xl font-extrabold mb-3">
            Admin Profile Settings
          </h1>
          <p className="text-gray-400 text-lg">
            Update your administrator credentials securely
          </p>
        </div>

        {/* Profile Card */}
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-10">

          <form onSubmit={handleUpdateProfile} className="space-y-8">

            {/* Email */}
            <div>
              <label className="block mb-2 text-sm text-gray-300">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white focus:border-cyan-400 outline-none"
              />
            </div>

            {/* Current Password */}
            <div>
              <label className="block mb-2 text-sm text-gray-300">
                Current Password <span className="text-red-400">*</span>
              </label>
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Required to confirm changes"
                className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white focus:border-cyan-400 outline-none"
              />
            </div>

            {/* Password Change */}
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block mb-2 text-sm text-gray-300">
                  New Password
                </label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white focus:border-cyan-400 outline-none"
                />
              </div>

              <div>
                <label className="block mb-2 text-sm text-gray-300">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white focus:border-cyan-400 outline-none"
                />
              </div>
            </div>

            {/* Messages */}
            {error && (
              <p className="text-red-400 text-sm">{error}</p>
            )}

            {message && (
              <p className="text-green-400 text-sm">{message}</p>
            )}

            {/* Submit */}
            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className={`px-10 py-4 rounded-xl font-semibold transition ${
                  loading
                    ? "bg-gray-600 cursor-not-allowed"
                    : "bg-gradient-to-r from-blue-500 to-cyan-500 hover:opacity-90"
                }`}
              >
                {loading ? "Updating..." : "Save Changes"}
              </button>
            </div>

          </form>
        </div>
      </section>
    </div>
  );
}
