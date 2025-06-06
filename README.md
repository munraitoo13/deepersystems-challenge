# Deeper Systems User Management System

## Overview

A full-stack web application for user management with Flask, MongoDB, and Vue.js 3.

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 5.0+

## Setup Instructions

### Backend Setup

1. Clone the repository
2. Navigate to backend directory
3. Create virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
5. Environment Variables

   Create `.env` files in backend with:
   
   - Database connection string (check .env.example in backend folder)

6. Import initial data

   ```bash
   python parser.py
   ```

7. Run Flask server

   ```bash
   python3 app.py
   ```

### Frontend Setup

In a new terminal window/tab:

1. Navigate to frontend directory
2. Install dependencies

   ```bash
   npm install (or your use favorite package manager)
   ```

3. Run development server

   ```bash
   npm run dev
   ```

After that, just open the URL provided by the script you've just run and you are good to go.

## Technology Stack

- Backend: Python, Flask
- Frontend: Vue.js 3, PrimeVue
- Database: MongoDB, PyMongo
