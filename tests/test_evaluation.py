from src.evaluation import (
    evaluate_profile,
    feature_distance_score,
    genre_diversity_score,
    mood_alignment_score,
    top_k_consistency_across_runs,
)
from src.recommender import load_songs, recommend_songs


def make_test_songs():
    return [
        {
            "id": 1,
            "title": "Pop Happy A",
            "artist": "A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "tempo_bpm": 120,
            "valence": 0.85,
            "danceability": 0.85,
            "acousticness": 0.10,
        },
        {
            "id": 2,
            "title": "Pop Happy B",
            "artist": "B",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "tempo_bpm": 122,
            "valence": 0.80,
            "danceability": 0.83,
            "acousticness": 0.12,
        },
        {
            "id": 3,
            "title": "Rock Intense",
            "artist": "C",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "tempo_bpm": 145,
            "valence": 0.45,
            "danceability": 0.60,
            "acousticness": 0.08,
        },
        {
            "id": 4,
            "title": "Lofi Chill",
            "artist": "D",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 80,
            "valence": 0.60,
            "danceability": 0.58,
            "acousticness": 0.86,
        },
        {
            "id": 5,
            "title": "Jazz Relaxed",
            "artist": "E",
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.40,
            "tempo_bpm": 90,
            "valence": 0.70,
            "danceability": 0.50,
            "acousticness": 0.88,
        },
    ]


def make_profile():
    return {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "tempo_bpm": 120,
        "valence": 0.85,
        "danceability": 0.85,
        "acousticness": 0.10,
    }


def test_top_k_consistency_is_1_for_deterministic_recommender():
    songs = make_test_songs()
    prefs = make_profile()

    score = top_k_consistency_across_runs(prefs, songs, k=5, runs=5)
    assert score == 1.0


def test_genre_diversity_score_in_range():
    songs = make_test_songs()
    prefs = make_profile()

    score = genre_diversity_score(prefs, songs, k=5)
    assert 0.0 <= score <= 1.0


def test_mood_alignment_score_in_range():
    songs = make_test_songs()
    prefs = make_profile()

    score = mood_alignment_score(prefs, songs, k=5)
    assert 0.0 <= score <= 1.0


def test_feature_distance_lower_for_closer_profile():
    songs = make_test_songs()

    close_prefs = make_profile()
    far_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.10,
        "tempo_bpm": 60,
        "valence": 0.10,
        "danceability": 0.10,
        "acousticness": 0.95,
    }

    close_distance = feature_distance_score(close_prefs, songs, k=5)
    far_distance = feature_distance_score(far_prefs, songs, k=5)

    assert close_distance < far_distance


def test_evaluate_profile_returns_all_metrics():
    songs = make_test_songs()
    prefs = make_profile()

    results = evaluate_profile(prefs, songs, k=5, runs=5)

    assert "top_k_consistency" in results
    assert "genre_diversity" in results
    assert "mood_alignment" in results
    assert "feature_distance" in results
    assert "top_titles" in results
    assert len(results["top_titles"]) == 5


def test_standard_profiles_return_relevant_top_results():
    songs = load_songs("data/songs.csv")

    standard_profiles = [
        {
            "name": "pop",
            "prefs": {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.90,
                "tempo_bpm": 124,
                "valence": 0.85,
                "danceability": 0.85,
                "acousticness": 0.15,
            },
        },
        {
            "name": "lofi",
            "prefs": {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "tempo_bpm": 78,
                "valence": 0.58,
                "danceability": 0.60,
                "acousticness": 0.85,
            },
        },
        {
            "name": "rock",
            "prefs": {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.92,
                "tempo_bpm": 145,
                "valence": 0.40,
                "danceability": 0.55,
                "acousticness": 0.10,
            },
        },
    ]

    for profile in standard_profiles:
        recommendations = recommend_songs(profile["prefs"], songs, k=5)
        assert len(recommendations) == 5

        top_genres = {song["genre"].lower() for song, _, _ in recommendations}
        assert profile["name"] in top_genres


def test_adversarial_profiles_still_return_stable_metrics():
    songs = load_songs("data/songs.csv")

    adversarial_profiles = [
        {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.90,
            "tempo_bpm": 70,
            "valence": 0.20,
            "danceability": 0.75,
            "acousticness": 0.20,
        },
        {
            "genre": "techno",
            "mood": "serene",
            "energy": 0.90,
            "tempo_bpm": 130,
            "valence": 0.45,
            "danceability": 0.90,
            "acousticness": 0.95,
        },
    ]

    for prefs in adversarial_profiles:
        metrics = evaluate_profile(prefs, songs, k=5, runs=5)

        assert len(metrics["top_titles"]) == 5
        assert 0.0 <= metrics["top_k_consistency"] <= 1.0
        assert 0.0 <= metrics["genre_diversity"] <= 1.0
        assert 0.0 <= metrics["mood_alignment"] <= 1.0
        assert 0.0 <= metrics["feature_distance"] <= 1.0


def test_out_of_range_and_rare_inputs_do_not_crash_and_return_top_k():
    songs = load_songs("data/songs.csv")

    rare_profile = {
        "genre": "k-pop",
        "mood": "nostalgic",
        "energy": -0.20,
        "tempo_bpm": 260,
        "valence": 1.60,
        "danceability": -0.30,
        "acousticness": 1.40,
    }

    recommendations = recommend_songs(rare_profile, songs, k=5)
    assert len(recommendations) == 5

    for song, score, explanation in recommendations:
        assert "title" in song
        assert isinstance(score, float)
        assert score >= 0.0
        assert isinstance(explanation, str)
        assert explanation.strip() != ""
