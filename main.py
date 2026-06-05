from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
import os

app = FastAPI(
    title="Cricket Data API",
    description="Live scores, match schedules, and player stats for cricket fans and developers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# You get a FREE API key from https://cricapi.com (100 calls/day free)
# Sign up → copy your key → paste it below OR set env variable
# -------------------------------------------------------------------
CRICAPI_KEY = os.getenv("CRICAPI_KEY", "YOUR_FREE_API_KEY_HERE")
BASE_URL = "https://api.cricapi.com/v1"


def cricapi_get(endpoint: str, extra_params: dict = {}):
    """Helper: call CricAPI and return JSON data."""
    params = {"apikey": CRICAPI_KEY, "offset": 0, **extra_params}
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get("status") != "success":
            raise HTTPException(status_code=502, detail=data.get("reason", "API error"))
        return data
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Cricket data source timed out.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


# ───────────────────────────────────────────────
# ENDPOINT 1: Live Scores
# ───────────────────────────────────────────────
@app.get(
    "/live-scores",
    summary="Get live cricket match scores",
    tags=["Scores"],
)
def live_scores():
    """
    Returns all **currently live** cricket matches with real-time scores.

    - International matches (Test, ODI, T20I)
    - IPL and other T20 leagues
    - Each match includes teams, current score, and match status
    """
    data = cricapi_get("currentMatches")
    matches = []
    for m in data.get("data", []):
        matches.append({
            "match_id": m.get("id"),
            "name": m.get("name"),
            "status": m.get("status"),
            "venue": m.get("venue"),
            "date": m.get("date"),
            "teams": m.get("teams", []),
            "score": m.get("score", []),
            "match_type": m.get("matchType"),
        })
    return {
        "success": True,
        "count": len(matches),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "matches": matches,
    }


# ───────────────────────────────────────────────
# ENDPOINT 2: Upcoming & Recent Matches
# ───────────────────────────────────────────────
@app.get(
    "/matches",
    summary="Get upcoming and recent cricket matches",
    tags=["Matches"],
)
def matches(limit: int = Query(default=10, le=50, description="Max number of matches to return")):
    """
    Returns a list of **upcoming and recently completed** cricket matches.

    Useful for building match calendars, notifications, or preview pages.
    """
    data = cricapi_get("matches")
    all_matches = data.get("data", [])[:limit]
    result = []
    for m in all_matches:
        result.append({
            "match_id": m.get("id"),
            "name": m.get("name"),
            "status": m.get("status"),
            "venue": m.get("venue"),
            "date": m.get("date"),
            "teams": m.get("teams", []),
            "match_type": m.get("matchType"),
            "series": m.get("series_id"),
        })
    return {
        "success": True,
        "count": len(result),
        "matches": result,
    }


# ───────────────────────────────────────────────
# ENDPOINT 3: Match Details by ID
# ───────────────────────────────────────────────
@app.get(
    "/match/{match_id}",
    summary="Get detailed scorecard for a specific match",
    tags=["Matches"],
)
def match_details(match_id: str):
    """
    Returns **full scorecard and details** for a specific match.

    Pass the `match_id` from `/live-scores` or `/matches`.
    Includes batting/bowling figures, partnerships, and fall of wickets.
    """
    data = cricapi_get("match_scorecard", {"id": match_id})
    return {
        "success": True,
        "data": data.get("data", {}),
    }


# ───────────────────────────────────────────────
# ENDPOINT 4: Player Search & Stats
# ───────────────────────────────────────────────
@app.get(
    "/player/search",
    summary="Search for a cricket player",
    tags=["Players"],
)
def search_player(name: str = Query(..., description="Player name to search, e.g. 'Virat Kohli'")):
    """
    Search for a player by name and get their **basic profile and stats**.

    Returns player ID, country, role, and batting/bowling averages.
    """
    data = cricapi_get("players", {"search": name})
    players = []
    for p in data.get("data", []):
        players.append({
            "player_id": p.get("id"),
            "name": p.get("name"),
            "country": p.get("country"),
            "player_img": p.get("playerImg"),
        })
    return {
        "success": True,
        "count": len(players),
        "players": players,
    }


@app.get(
    "/player/{player_id}",
    summary="Get detailed player stats",
    tags=["Players"],
)
def player_stats(player_id: str):
    """
    Returns **detailed career statistics** for a player.

    Includes Test, ODI, and T20 batting and bowling averages,
    centuries, wickets, and more.
    """
    data = cricapi_get("players_info", {"id": player_id})
    return {
        "success": True,
        "data": data.get("data", {}),
    }


# ───────────────────────────────────────────────
# ENDPOINT 5: Series List
# ───────────────────────────────────────────────
@app.get(
    "/series",
    summary="Get list of cricket series",
    tags=["Series"],
)
def series_list(
    type: str = Query(
        default="all",
        description="Filter: 'international', 'league', 'domestic', or 'all'",
    )
):
    """
    Returns a list of **ongoing and upcoming cricket series**.

    Filter by `type` to get international tours, IPL/leagues, or domestic competitions.
    """
    data = cricapi_get("series", {"type": type})
    series = []
    for s in data.get("data", []):
        series.append({
            "series_id": s.get("id"),
            "name": s.get("name"),
            "start_date": s.get("startDate"),
            "end_date": s.get("endDate"),
            "odi": s.get("odi"),
            "t20": s.get("t20"),
            "test": s.get("test"),
            "matches": s.get("matches"),
        })
    return {
        "success": True,
        "count": len(series),
        "series": series,
    }


# ───────────────────────────────────────────────
# Health check
# ───────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Cricket API is running 🏏",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": ["/live-scores", "/matches", "/match/{id}", "/player/search", "/player/{id}", "/series"],
    }
