import { useAuth } from "../../context/useAuth";

export default function UserViewModal({ user, onClose, onActionComplete }) {
  const { user: admin } = useAuth();

  if (!user) return null;

  const roleStyles = {
    admin: "bg-purple-500/20 text-purple-400",
    delivery: "bg-blue-500/20 text-blue-400",
    user: "bg-emerald-500/20 text-emerald-400",
  };

  const disableUser = async () => {
    if (!window.confirm(`Disable ${user.email}?`)) return;

    await fetch(`http://127.0.0.1:8000/users/${user._id}/disable`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${admin.access_token}`,
      },
    });

    onClose();
    onActionComplete();
  };

  const deleteUser = async () => {
    if (
      !window.confirm(
        `⚠️ Permanently delete ${user.email}? This cannot be undone!`
      )
    )
      return;

    await fetch(`http://127.0.0.1:8000/users/${user._id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${admin.access_token}`,
      },
    });

    onClose();
    onActionComplete();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center px-4">
      <div className="w-full max-w-lg bg-[#0b0f1a] border border-white/10 rounded-2xl shadow-2xl p-6 relative">

        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          ✕
        </button>

        <h2 className="text-2xl font-extrabold mb-6">User Profile</h2>

        <div className="space-y-6 text-sm">
          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <p className="text-gray-400">Email</p>
            <p className="text-white">{user.email}</p>
          </div>

          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <p className="text-gray-400 mb-1">Role</p>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold ${roleStyles[user.role]}`}
            >
              {user.role.toUpperCase()}
            </span>
          </div>

          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <p className="text-gray-400">Account Status</p>
            <p
              className={`font-semibold ${
                user.disabled ? "text-red-400" : "text-green-400"
              }`}
            >
              {user.disabled ? "Disabled" : "Active"}
            </p>
          </div>

          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <p className="text-gray-400">Last Known Location</p>
            {user.location?.address ? (
              <p className="text-white">{user.location.address}</p>
            ) : (
              <p className="text-gray-500 italic">Location not available</p>
            )}
          </div>
        </div>

        <div className="mt-8 flex justify-end gap-3">
          {!user.disabled ? (
            <button
              onClick={disableUser}
              className="px-4 py-2 rounded-lg bg-red-500/15 text-red-400 hover:bg-red-500/25 font-semibold"
            >
              Disable User
            </button>
          ) : (
            <button
              onClick={deleteUser}
              className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold"
            >
              Delete Permanently
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
