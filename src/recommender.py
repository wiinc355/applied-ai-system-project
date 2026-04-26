import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of typed dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs


def _similarity_points(target: float, actual: float, weight: float, max_distance: float) -> float:
    """Convert feature distance into weighted similarity points."""
    distance = abs(target - actual)
    similarity = max(0.0, 1.0 - (distance / max_distance))
    return weight * similarity

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return score with reasons."""
    score = 0.0
    reasons: List[str] = []

    user_genre = user_prefs.get("genre")
    if user_genre and song.get("genre", "").lower() == str(user_genre).lower():
        score += 1.0
        reasons.append("genre match (+1.00)")

    user_mood = user_prefs.get("mood")
    if user_mood and song.get("mood", "").lower() == str(user_mood).lower():
        score += 1.0
        reasons.append("mood match (+1.00)")

    numeric_features = [
        ("energy", 3.0, 1.0),
        ("tempo_bpm", 1.0, 80.0),
        ("valence", 1.0, 1.0),
        ("danceability", 0.75, 1.0),
        ("acousticness", 0.75, 1.0),
    ]

    for feature_name, weight, max_distance in numeric_features:
        if feature_name not in user_prefs or feature_name not in song:
            continue

        points = _similarity_points(
            float(user_prefs[feature_name]),
            float(song[feature_name]),
            weight,
            max_distance,
        )
        score += points
        reasons.append(f"{feature_name} similarity (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by preference score and return the top k with explanations."""
    ranked_songs: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general similarity match"
        ranked_songs.append((song, score, explanation))

    ranked_songs.sort(key=lambda item: item[1], reverse=True)
    return ranked_songs[:k]
