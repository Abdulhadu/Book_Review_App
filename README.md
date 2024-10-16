# 📚 Book Review Application with Django REST Framework (DRF)

## 🚀 Project Overview
This project is a **Book Review Application** built using **Django** and **Django REST Framework (DRF)**. It allows users to sign up, log in, and perform various actions such as publishing books, leaving reviews, and adding comments to books published by others. The application ensures proper authentication, permissions, and functionality for managing users, books, reviews, and comments.

## 🎯 Key Features
### 1. **User Authentication & Authorization**
- **User Sign-up & Login**: Implemented using **Django REST Framework** (DRF) with secure authentication using **JWT (JSON Web Token)**.
- **Protected Endpoints**: Secured with JWT to allow only authenticated users to perform actions like publishing books or posting reviews/comments.

### 2. **Book Management**
- **Publish a Book**: Authenticated users can publish books by submitting details such as title, author, description, and cover image.
- **List All Books**: Get a list of all books published by users.
- **Retrieve Book by ID**: Fetch details of a specific book by its ID.
- **Update a Book**: Users can update the details of the books they published.
- **Delete a Book**: Users can delete their own books.

### 3. **Review & Comment System**
- **Post a Review/Comment**: Users can leave reviews and comments on books published by others. (Cannot comment on their own books).
- **List Reviews for a Book**: Fetch all reviews for a particular book.
- **Edit a Review/Comment**: Users can edit only their own reviews/comments.
- **Delete a Review/Comment**: Users can delete only their own reviews/comments.

### 4. **Constraints & Rules**
- Users **cannot** comment on their own books.
- Only the user who posted a comment/review can edit or delete it.

## 🛠️ Technology Stack
- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (JSON Web Token)
- **Database**: SQLite (default for development)
- **Media**: ImageField to handle book cover uploads

## ⚙️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/book-review-app.git
   cd book-review-app

2. **Install the requirement deopendecy**:
   ```bash
   pip install -r requirements.txt

3. **Apply the Migration**:
   ```bash
   python manage.py migrate

3. **Run the development Server**:
   ```bash
   python manage.py runserver
