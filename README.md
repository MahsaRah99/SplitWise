# 💸 Splitwise-like Expense Sharing App 💰

Welcome to the **Splitwise-like Expense Sharing App**, a web-based platform to manage group expenses and simplify the process of splitting bills among members. Built with a robust back end in **Django REST** and a dynamic front end powered by **Next.js**, this project aims to deliver an intuitive and efficient expense-sharing experience.

## 🚀 Features

- **👥 Group Management**  
  Create, join, and manage groups with ease. Share expenses with friends, family, or colleagues.

- **🧾 Expense Splitting**  
  Add expenses and split costs among group members automatically.

- **🔄 Simplify Debts**  
  Reduce the number of transactions needed to settle debts with the **Simplify Debts** feature, which offers:  
  - **Detailed Mode**: View all individual transactions and balances.  
  - **Simplified Mode**: Consolidate transactions into a minimal number of settlements.

- **💵 Settle Debts**  
  View total balances owed between members and settle them with a single click.

- **🔒 Secure Group Links**  
  Share group invitation links to allow members to join seamlessly.


## 🛠️ Tech Stack

### Back End
- **🐍 Python**  
- **🌐 Django REST**  
  - Handles core logic, database operations, and APIs.

### Front End
- **⚛️ Next.js**  
  - Provides a responsive and interactive user interface with modern React-based components.

### Database
- **🐘 PostgreSQL**  
  - A reliable and efficient relational database system.

### Deployment
- **🐳 Docker**  
  - Simplified deployment with containerization.

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MahsaRah99/splitwise.git
   cd splitwise

2. **Back End Setup**:
   - Create a virtual environment and install dependencies:
     ```bash
     python -m venv env
     source env/bin/activate  # On Windows: env\Scripts\activate
     pip install -r requirements.txt
     ```
   - Run migrations and start the server:
     ```bash
     python manage.py migrate
     python manage.py runserver
     ```

3. **Front End Setup**:
   - Navigate to the `frontend` directory and install dependencies:
     ```bash
     cd frontend
     npm install
     ```
   - Start the development server:
     ```bash
     npm run dev
     ```


###⭐ If you find this project helpful, consider giving it a star on GitHub! ✨
Happy coding! 😊
