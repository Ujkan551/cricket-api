# 🏏 Cricket Data API

A clean, monetizable Cricket REST API built with Python + FastAPI.
List it on RapidAPI to earn passive income!

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/live-scores` | All live match scores right now |
| GET | `/matches` | Upcoming & recent matches |
| GET | `/match/{match_id}` | Full scorecard for a match |
| GET | `/player/search?name=Kohli` | Search for a player |
| GET | `/player/{player_id}` | Detailed player career stats |
| GET | `/series?type=league` | Ongoing/upcoming series list |

---

## Setup (Local)

### Step 1 — Get your FREE API key
1. Go to https://cricapi.com
2. Sign up for free (100 calls/day free)
3. Copy your API key from the dashboard

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Set your API key
Create a `.env` file in this folder:
```
CRICAPI_KEY=your_actual_key_here
```

### Step 4 — Run the server
```bash
uvicorn main:app --reload
```

### Step 5 — Test it
Open your browser and go to:
- http://localhost:8000 — health check
- http://localhost:8000/docs — interactive API docs (Swagger UI)
- http://localhost:8000/live-scores — live scores

---

## Deploy for Free on Render.com

1. Push this folder to a GitHub repo
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `CRICAPI_KEY = your_key`
6. Deploy → you get a free public URL like `https://your-api.onrender.com`

---

## List on RapidAPI (Earn Money!)

1. Go to https://rapidapi.com/provider
2. Click "Add New API"
3. Set your base URL (your Render URL)
4. Add each endpoint from the table above
5. Set pricing tiers:
   - **Free**: 50 requests/day
   - **Basic ($9/mo)**: 1,000 requests/day
   - **Pro ($29/mo)**: 10,000 requests/day
   - **Ultra ($79/mo)**: Unlimited
6. Publish → developers can find and subscribe to your API

---

## Tips to Earn More

- Write a clear description on RapidAPI mentioning IPL, live scores, and player stats
- Add "Cricket" and "IPL" as tags
- Keep the free tier generous so developers try it
- Reply fast to any issues — good ratings = more subscribers
