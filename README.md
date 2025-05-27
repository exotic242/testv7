
# Community Service Tracker (Flask + Google Sheets)

This is a Flask-based web application that allows students to log their community service hours and admins to manage and verify logs. It is designed to be deployed on [Render](https://render.com).

---

## ✅ Features
- Student registration, login, goal setting
- Admin dashboard with CSV export
- Smart logging with device/IP/location
- Suspicious activity detection
- Leaderboard and student log viewer
- Dark mode analytics with Chart.js
- Calendar view with FullCalendar.js
- Goal progress bar and future award logic
- Mobile-optimized, modular codebase

---

## ⚙️ Deployment Instructions (Render)

### 1. Upload the Project
- Push to GitHub **OR**
- Upload the ZIP and extract in your Render-connected repo

### 2. Create a New Web Service
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click **New + → Web Service**
- Set the following:

| Setting          | Value               |
|------------------|---------------------|
| Environment      | Python              |
| Build Command    | *(Leave blank)*     |
| Start Command    | `gunicorn app:app`  |
| Runtime          | Python 3.11+        |

---

### 3. Add Environment Variables

Go to **Environment > Add Environment Variable**, and add the following:

```env
SECRET_KEY=devkey
ADMIN_REGISTRATION_CODE=letmein
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_CREDS_JSON=credentials.json
```

---

### 4. Upload Your Credentials JSON

- Go to **Environment > Secret Files**
- Upload your `credentials.json` file there
- Render will inject this securely at runtime

---

### 5. Visit Your App

Once deployed, Render will provide a live URL where your app is running!

---

## 🗂 Folder Structure

```
.
├── app.py
├── .env
├── requirements.txt
├── sheets_api.py
├── logs_api.py
├── utils.py
├── routes/
├── templates/
```

---

## License

MIT — feel free to modify and extend.
