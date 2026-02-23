const API_BASE = "http://127.0.0.1:8000";

/* ===============================
   AUTH
================================ */
export async function loginUser(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  return res.json();
}

export async function signupUser(data) {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw await res.json();
  }

  return res.json();
}

/* ===============================
   PUBLIC — AI PREDICTION
================================ */
export async function predictScrap(image, weight) {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("weight", weight);

  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Prediction failed");
  }

  return res.json();
}

/* ===============================
   PLACE ORDER (USER) — WITH IMAGE
================================ */
export async function placeOrder(orderData, token) {
  const formData = new FormData();

  formData.append("material", orderData.material);
  formData.append("weight", orderData.weight);
  formData.append("estimated_price", orderData.estimated_price);
  formData.append("latitude", orderData.latitude);
  formData.append("longitude", orderData.longitude);
  formData.append("image", orderData.image); // 🔥 REQUIRED

  const res = await fetch(`${API_BASE}/orders/place`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // ❌ DO NOT set Content-Type
    },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err);
  }

  return res.json();
}

/* ===============================
   USER — FETCH MY ORDERS
================================ */
export async function fetchMyOrders(token) {
  const res = await fetch(`${API_BASE}/orders/my`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch orders");
  }

  return res.json();
}

/* ===============================
   ADMIN — FETCH ALL ORDERS
================================ */
export async function fetchAllOrders(token) {
  const res = await fetch(`${API_BASE}/orders/all`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch all orders");
  }

  return res.json();
}

/* ===============================
   ADMIN — APPROVE ORDER
================================ */
export async function approveOrder(orderId, token) {
  const res = await fetch(`${API_BASE}/orders/${orderId}/approve`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to approve order");
  }

  return res.json();
}

/* ===============================
   ADMIN — REJECT ORDER
================================ */
export async function rejectOrder(orderId, reason, token) {
  const formData = new FormData();
  formData.append("reason", reason);

  const res = await fetch(`${API_BASE}/orders/${orderId}/reject`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Failed to reject order");
  }

  return res.json();
}

/* ===============================
   USER — SAVE LOCATION (OPTIONAL)
================================ */
export async function saveLocation(coords, token) {
  const res = await fetch(`${API_BASE}/users/location`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(coords),
  });

  if (!res.ok) {
    throw new Error("Failed to save location");
  }

  return res.json();
}
