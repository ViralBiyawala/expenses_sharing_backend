# Daily Expenses Sharing Application

## Overview

This is a backend application built with Django and SQLite for managing daily expenses. Users can create accounts, add expenses, and split them using different methods: equal amounts, exact amounts, and percentages. The application includes API endpoints for user and expense management, along with features to download balance sheets.

## Features

- User Management:
   - Create and manage user accounts.
   - Store user details (email, name, mobile number).
   
- Expense Management:
   - Add expenses with different splitting methods:
      - **Equal Split**: Divide the total equally among participants.
      - **Exact Amounts**: Specify exact amounts each participant owes.
      - **Percentage Split**: Specify percentages owed, ensuring they total 100%.

- Balance Sheet:
   - Track individual and overall expenses.
   - Downloadable balance sheet.

## Tech Stack

- **Framework**: Django
- **Database**: SQLite
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)

## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/viralbiyawala/expenses_sharing_backend.git
    cd expenses_sharing_backend
    ```
    
2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Move to the Expenses Folder**
    ```bash
    cd expenses
    ```

4. **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Start the Development Server**
    ```bash
    python manage.py runserver
    ```

6. **Run Test Cases**
   ```bash
   python manage.py test expenses
   ```

## API Endpoints

### User Management

#### Create User
- **URL:** `/api/users/`
- **Method:** POST
- **Authorization:** Not Required ( ** future work: Can add email or mobile based OTP )
- **Body:**
   ```json
   {
      "username": "johndoe",
      "email": "johndoe@example.com",
      "password": "securepassword123",
      "first_name": "John",
      "last_name": "Doe"
   }
   ```

#### List Users
- **URL:** `/api/users/`
- **Method:** GET
- **Authentication:** Required (Admin Only)

#### Retrieve User
- **URL:** `/api/users/{id}/`
- **Method:** GET
- **Authentication:** Required

#### Update User
- **URL:** `/api/users/{id}/`
- **Method:** PUT
- **Authentication:** Required
- **Body:**
   ```json
   {
      "email": "newemail@example.com",
      "first_name": "Johnny",
      "last_name": "Doe"
   }
   ```

#### Delete User
- **URL:** `/api/users/{id}/`
- **Method:** DELETE
- **Authentication:** Required

### Authentication

#### Obtain Token
- **URL:** `/api/token/`
- **Method:** POST
- **Body:**
   ```json
   {
      "username": "johndoe",
      "password": "securepassword123"
   }
   ```

#### Refresh Token
- **URL:** `/api/token/refresh/`
- **Method:** POST
- **Body:**
   ```json
   {
      "refresh": "your_refresh_token_here"
   }
   ```

### Expense Management

#### Create Expense
- **URL:** `/api/expenses/`
- **Method:** POST
- **Authentication:** Required
- **Body:**
   ```json
   {
      "title": "Dinner",
      "amount": "100.00",
      "split_type": "EQUAL",
      "splits": [
         {"user": 1},
         {"user": 2}
      ]
   }
   ```
   or
   ```json
   {
      "title": "Groceries",
      "amount": "80.00",
      "split_type": "EXACT",
      "splits": [
         {"user": 1, "amount": "50.00"},
         {"user": 2, "amount": "30.00"}
      ]
   }
   ```
   or
   ```json
   {
      "title": "Vacation",
      "amount": "1000.00",
      "split_type": "PERCENTAGE",
      "splits": [
         {"user": 1, "percentage": "60.00"},
         {"user": 2, "percentage": "40.00"}
      ]
   }
   ```

#### List All Expenses
- **URL:** `/api/expenses/overall_expenses/`
- **Method:** GET
- **Authentication:** Required (Admin Only)

#### Retrieve Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** GET
- **Authentication:** Required

#### Update Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** PUT
- **Authentication:** Required
- **Body:** (similar to Create Expense) (Admin Only)

#### Delete Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** DELETE
- **Authentication:** Required (Admin Only)

#### User's Expenses
- **URL:** `/api/expenses/user_expenses/`
- **Method:** GET
- **Authentication:** Required

#### Download Balance Sheet
- **URL:** `/api/expenses/download_balance_sheet/`
- **Method:** GET
- **Authentication:** Required (Admin Only)

## Authentication

All endpoints except for Create User and Obtain Token require authentication using a JWT token. Include the token in the Authorization header as follows:

```
Authorization: Bearer <your_jwt_token>
```

Remember to replace placeholder values (like user IDs, amounts, etc.) with actual values when making requests.

## Admin User

An admin user can be created using the Django admin panel or by running the following command:

```bash
python manage.py createsuperuser
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

