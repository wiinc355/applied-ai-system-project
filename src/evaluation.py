from itertools import combinations
from typing import Dict, List, Tuple

from .recommender import recommend_songs


# (feature_name, max_distance) used to normalize distances into [0, 1].
NUMERIC_FEATURES: List[Tuple[str, float]] = [
    ("energy", 1.0),
    ("tempo_bpm", 80.0),
    ("valence", 1.0),
    ("danceability", 1.0),
    ("acousticness", 1.0),
]


def _top_k_song_ids(user_prefs: Dict, songs: List[Dict], k: int) -> List[int]:
    recommendations = recommend_songs(user_prefs, songs, k=k)
    return [song["id"] for song, _, _ in recommendations]


def top_k_consistency_across_runs(user_prefs: Dict, songs: List[Dict], k: int = 5, runs: int = 5) -> float:
    """Return average pairwise Jaccard overlap between top-k result sets across runs."""
    if runs < 2:
        raise ValueError("runs must be at least 2")

    run_sets = [set(_top_k_song_ids(user_prefs, songs, k=k)) for _ in range(runs)]
    pair_scores: List[float] = []

    for left, right in combinations(run_sets, 2):
        union = left | right
        if not union:
            pair_scores.append(1.0)
        else:
            pair_scores.append(len(left & right) / len(union))

    return sum(pair_scores) / len(pair_scores)


def genre_diversity_score(user_prefs: Dict, songs: List[Dict], k: int = 5) -> float:
    """Return ratio of unique genres in the top-k list."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    if not recommendations:
        return 0.0

    genres = {song["genre"].lower() for song, _, _ in recommendations}
    return len(genres) / len(recommendations)


def mood_alignment_score(user_prefs: Dict, songs: List[Dict], k: int = 5) -> float:
    """Return fraction of top-k songs whose mood matches requested mood."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    if not recommendations:
        return 0.0

    target_mood = str(user_prefs.get("mood", "")).lower()
    if not target_mood:
        return 0.0

    matches = sum(1 for song, _, _ in recommendations if str(song.get("mood", "")).lower() == target_mood)
    return matches / len(recommendations)


def feature_distance_score(user_prefs: Dict, songs: List[Dict], k: int = 5) -> float:
    """Return average normalized feature distance in top-k; lower is better."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    if not recommendations:
        return 0.0

    song_distances: List[float] = []

    for song, _, _ in recommendations:
        per_feature: List[float] = []
        for feature_name, max_distance in NUMERIC_FEATURES:
            if feature_name not in user_prefs or feature_name not in song:
                continue

            distance = abs(float(user_prefs[feature_name]) - float(song[feature_name])) / max_distance
            per_feature.append(min(1.0, max(0.0, distance)))

        if per_feature:
            song_distances.append(sum(per_feature) / len(per_feature))

    if not song_distances:
        return 0.0

    return sum(song_distances) / len(song_distances)


def evaluate_profile(user_prefs: Dict, songs: List[Dict], k: int = 5, runs: int = 5) -> Dict:
    """Compute all core evaluation metrics for one profile."""
    top_recs = recommend_songs(user_prefs, songs, k=k)
    return {
        "top_k_consistency": top_k_consistency_across_runs(user_prefs, songs, k=k, runs=runs),
        "genre_diversity": genre_diversity_score(user_prefs, songs, k=k),
        "mood_alignment": mood_alignment_score(user_prefs, songs, k=k),
        "feature_distance": feature_distance_score(user_prefs, songs, k=k),
        "top_titles": [song["title"] for song, _, _ in top_recs],
    }


def evaluate_profiles(profiles: Dict[str, Dict], songs: List[Dict], k: int = 5, runs: int = 5) -> Dict[str, Dict]:
    """Compute evaluation metrics for multiple named profiles."""
    return {
        name: evaluate_profile(user_prefs, songs, k=k, runs=runs)
        for name, user_prefs in profiles.items()
    }


def format_evaluation_report(results: Dict[str, Dict]) -> str:
    """Create a readable CLI report for evaluation metrics."""
    lines: List[str] = []
    lines.append("\n" + "=" * 72)
    lines.append("Evaluation Metrics")

    for profile_name, metrics in results.items():
        lines.append("\n" + "-" * 72)
        lines.append(f"Profile: {profile_name}")
        lines.append(f"Top-5 consistency across runs: {metrics['top_k_consistency']:.2f}")
        lines.append(f"Genre diversity in top-5:      {metrics['genre_diversity']:.2f}")
        lines.append(f"Mood alignment score:          {metrics['mood_alignment']:.2f}")
        lines.append(f"Feature-distance score:        {metrics['feature_distance']:.2f} (lower is better)")
        lines.append(f"Top songs: {', '.join(metrics['top_titles'])}")

    return "\n".join(lines)