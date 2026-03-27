# ScrapX ♻️
### AI-Powered Scrap Classification & Price Estimation

ScrapX is a modern, high-performance platform designed to revolutionize the scrap recycling industry. Using advanced machine learning, ScrapX allows users to classify different types of scrap materials (metals, plastics, paper, etc.) from images and get real-time price estimations, making the recycling process efficient and transparent.

---

## 📽️ Project Overview
ScrapX provides a seamless interface for users to identify their scrap materials and book pickups. It integrates a robust management system for administrators to track orders and dispatch delivery personnel, creating a complete end-to-end recycling ecosystem.

### Key Features:
- **AI Classification**: Identify scrap materials instantly using computer vision.
- **Dynamic Pricing**: Get up-to-date market rates for various scrap types.
- **Order Management**: Schedule and track scrap pickups effortlessly.
- **Admin Control**: Centralized dashboard for managing users, orders, and deliveries.
- **Delivery App**: Dedicated interface for delivery personnel to manage tasks and update statuses.

---

## 🔄 Full Project Flow
1. **User Side**:
    - **Upload & Identify**: User uploads an image of the scrap material.
    - **AI Processing**: The PyTorch-based CNN model identifies the material (e.g., Aluminum, Iron, Plastic).
    - **Estimate**: Based on current market prices and estimated weight, a price is suggested.
    - **Booking**: User creates an order for pickup and provides location details.
2. **Admin Side**:
    - **Order Review**: Admin reviews incoming orders.
    - **Assignment**: Admin assigns the order to an available delivery partner.
    - **Tracking**: Monitors the entire lifecycle from "Pending" to "Completed".
3. **Delivery Side**:
    - **Pick-up**: Delivery partner sees assigned tasks and proceeds to the user's location.
    - **Verification**: Verifies the scrap and updates the status via the delivery panel.
    - **Completion**: Marks the order as completed once the scrap is collected.

---

## 🖥️ System Panels

### 1. User Panel
A clean and intuitive dashboard for general users.
- **Home**: Quick access to scrap classification.
- **Predict**: Image upload and AI-driven identification.
- **My Orders**: Track the status of current and past scrap sales.
- **Profile**: Manage personal information and addresses.

### 2. Admin Panel
A comprehensive management interface for hospital/system administrators.
- **Analytics Dashboard**: Real-time stats on orders, users, and revenue.
- **User Management**: Control over user accounts and roles.
- **Order Pipeline**: Full control over the order lifecycle (Verify -> Assign -> Complete).
- **Delivery Management**: Assigning and monitoring delivery personnel tasks.
- **Payments**: Tracking financial transactions and payouts.

### 3. Delivery Panel
Streamlined for on-the-field delivery partners.
- **Assignments**: View all currently assigned scrap pickups.
- **Active Tasks**: Real-time status updates (In Progress, Picked Up).
- **History**: Log of all successfully completed deliveries.
- **Profile**: Personal availability and performance stats.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | React.js (Vite), Tailwind CSS v4, Lucide React, Framer Motion |
| **Backend** | FastAPI (Python), SQLAlchemy |
| **AI / Machine Learning** | PyTorch, XGBoost, Scikit-learn, OpenCV, PIL |
| **Database** | SQLite / PostgreSQL |
| **Development Tools** | ESLint, Git, NPM |

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/omsatardekar/ScrapX.git
   cd ScrapX
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 📧 Contact & Support
For any queries, suggestions, or reports, feel free to reach out:

📩 **Email**: [omkarsatardekar4002@gmail.com](mailto:omkarsatardekar4002@gmail.com)

---
*Developed with ❤️ by the ScrapX Team.*
