"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
from .evaluation import evaluate_profiles, format_evaluation_report


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for one user profile in a readable CLI layout."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 72)
    print(f"Profile: {profile_name}")
    print(
        "Prefs: "
        f"genre={user_prefs.get('genre')}, "
        f"mood={user_prefs.get('mood')}, "
        f"energy={user_prefs.get('energy')}, "
        f"tempo_bpm={user_prefs.get('tempo_bpm')}, "
        f"valence={user_prefs.get('valence')}, "
        f"danceability={user_prefs.get('danceability')}, "
        f"acousticness={user_prefs.get('acousticness')}"
    )
    print("Top 5 recommendations:\n")

    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.split(", ") if explanation else []

        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "tempo_bpm": 124,
            "valence": 0.85,
            "danceability": 0.85,
            "acousticness": 0.15,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 78,
            "valence": 0.58,
            "danceability": 0.60,
            "acousticness": 0.85,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "tempo_bpm": 145,
            "valence": 0.40,
            "danceability": 0.55,
            "acousticness": 0.10,
        },
        # Edge/adversarial profiles for stress testing.
        "Conflict: High Energy + Sad": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.90,
            "tempo_bpm": 70,
            "valence": 0.20,
            "danceability": 0.75,
            "acousticness": 0.20,
        },
        "Conflict: Acoustic Techno": {
            "genre": "techno",
            "mood": "serene",
            "energy": 0.90,
            "tempo_bpm": 130,
            "valence": 0.45,
            "danceability": 0.90,
            "acousticness": 0.95,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)

    evaluation_results = evaluate_profiles(profiles, songs, k=5, runs=5)
    print(format_evaluation_report(evaluation_results))


if __name__ == "__main__":
    main()
