# Dad's Portfolio - Corporate Leader & Musician Website

A premium, modern portfolio website built for **Gandharba Raj Paudel**, celebrating over twenty-five years of corporate leadership, executive mentorship, and a lifelong musical journey as a folk-rock vocalist and acoustic guitarist.

This application is split into a **FastAPI backend** (incorporating MongoDB and Cloudinary integrations) and a **React+Vite frontend** (with elegant layouts, modern typography, glassmorphism, and a custom audio player).

---

## 🚀 Deployment Guide

### 1. Backend Deployment (Render)

Deploy the Python backend on **[Render.com](https://render.com/)** as a **Web Service**:

1. Log in to Render and click **New > Web Service**.
2. Connect this GitHub repository.
3. Configure the following service settings:
   - **Name**: `dad-portfolio-api` (or any custom name)
   - **Root Directory**: `backend` (very important!)
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **Advanced** and add the following **Environment Variables**:
   - `MONGODB_URI`: 
   - `DATABASE_NAME`: 
   - `CLOUDINARY_CLOUD_NAME`:
   - `CLOUDINARY_API_KEY`: 
   - `CLOUDINARY_API_SECRET`: 
   - `CLOUDINARY_MUSIC_FOLDER`: 
   - `CLOUDINARY_PICTURES_FOLDER`: 
   - `CORS_ORIGINS`: `https://your-frontend-domain.vercel.app` *(update this with your Vercel URL once deployed!)*
5. Click **Deploy Web Service**.

---

### 2. Frontend Deployment (Vercel)

Deploy the React frontend on **[Vercel.com](https://vercel.com/)**:

1. Log in to Vercel and click **Add New > Project**.
2. Import this GitHub repository.
3. Configure the following project settings:
   - **Root Directory**: `frontend` (very important!)
   - **Framework Preset**: `Vite` (automatically detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add the following **Environment Variable**:
   - `VITE_API_URL`: `https://dad-portfolio-api.onrender.com` *(use your actual Render Web Service URL!)*
5. Click **Deploy**.
6. **Important CORS Step**: Copy your new Vercel domain (e.g. `https://dad-portfolio.vercel.app`), go back to your **Render Dashboard > Environment Variables**, and add it to `CORS_ORIGINS`.

---

## 🛠️ Local Development

### Prerequisites
- Python 3.10+
- Node.js LTS

### Backend Setup
1. Open a terminal in the `backend` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will be running at `http://localhost:8000`.

### Frontend Setup
1. Open a terminal in the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will be running at `http://localhost:5173`.
