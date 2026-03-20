Restaurant System API
A backend API built with FastAPI for managing a restaurant’s core operations, including product catalog, categories, and inventory control through stock movements.
🚀 Current Features
✔️ Product Management
• 	Create, list, update, and delete products
• 	Each product includes name, price, stock, and category
• 	Fully relational with categories
✔️ Category Management
• 	Create and list categories
• 	One‑to‑many relationship with products
✔️ Inventory Movement System
• 	Register stock entries and exits
• 	Prevents negative stock automatically
• 	Updates product stock in real time
• 	Keeps a full history of movements
• 	Supports movement types (e.g., “in”, “out”) and descriptions
🛠️ Tech Stack
• 	FastAPI
• 	SQLAlchemy ORM
• 	Pydantic
• 	SQLite (easily replaceable with PostgreSQL/MySQL)
• 	Uvicorn
📂 Project Structure

📌 Roadmap (Next Steps)
• 	Implement Orders module (POS / Sales)
• 	Add Order Items
• 	Automatic stock deduction when closing an order
• 	Order history and reporting
• 	Optional: table management (for restaurants)
• 	Optional: user authentication
