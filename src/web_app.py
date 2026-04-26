import io
import subprocess
import sys
from contextlib import redirect_stdout
from typing import Dict

import streamlit as st

from src.evaluation import evaluate_profiles, format_evaluation_report
from src.main import print_recommendations
from src.recommender import load_songs


st.set_page_config(page_title="Music Recommender Demo", page_icon="🎵", layout="wide")


DEFAULT_PROFILES: Dict[str, Dict] = {
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


@st.cache_data
def get_songs() -> list[dict]:
    return load_songs("data/songs.csv")


def run_cli_equivalent(songs: list[dict]) -> str:
    output_buffer = io.StringIO()

    with redirect_stdout(output_buffer):
        print(f"Loaded songs: {len(songs)}")
        for profile_name, user_prefs in DEFAULT_PROFILES.items():
            print_recommendations(profile_name, user_prefs, songs, k=5)

        evaluation_results = evaluate_profiles(DEFAULT_PROFILES, songs, k=5, runs=5)
        print(format_evaluation_report(evaluation_results))

    return output_buffer.getvalue()


def run_metrics_only(songs: list[dict]) -> str:
    results = evaluate_profiles(DEFAULT_PROFILES, songs, k=5, runs=5)
    return format_evaluation_report(results)


def run_pytest() -> tuple[int, str]:
    process = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (process.stdout or "") + (process.stderr or "")
    return process.returncode, output.strip()


st.title("🎵 Music Recommender Demo")
st.write("Run your recommender commands from a web interface for class demos.")

songs = get_songs()

st.subheader("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Full Recommender", use_container_width=True):
        with st.spinner("Running full recommender output..."):
            full_output = run_cli_equivalent(songs)
        st.code(full_output, language="text")

with col2:
    if st.button("Show Evaluation Metrics", use_container_width=True):
        with st.spinner("Calculating metrics..."):
            metric_output = run_metrics_only(songs)
        st.code(metric_output, language="text")

with col3:
    if st.button("Run Tests (pytest -q)", use_container_width=True):
        with st.spinner("Running tests..."):
            code, test_output = run_pytest()
        if code == 0:
            st.success("Tests passed")
        else:
            st.error(f"Tests failed (exit code {code})")
        st.code(test_output or "No test output", language="text")

st.divider()
st.subheader("Custom Profile Playground")

custom_genre = st.text_input("Genre", value="pop")
custom_mood = st.text_input("Mood", value="happy")
custom_energy = st.slider("Energy", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
custom_tempo = st.slider("Tempo (BPM)", min_value=40, max_value=200, value=120, step=1)
custom_valence = st.slider("Valence", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
custom_danceability = st.slider("Danceability", min_value=0.0, max_value=1.0, value=0.75, step=0.01)
custom_acousticness = st.slider("Acousticness", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

if st.button("Recommend for Custom Profile"):
    custom_profile = {
        "genre": custom_genre,
        "mood": custom_mood,
        "energy": custom_energy,
        "tempo_bpm": float(custom_tempo),
        "valence": custom_valence,
        "danceability": custom_danceability,
        "acousticness": custom_acousticness,
    }

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        print_recommendations("Custom Profile", custom_profile, songs, k=5)
        custom_eval = evaluate_profiles({"Custom Profile": custom_profile}, songs, k=5, runs=5)
        print(format_evaluation_report(custom_eval))

    st.code(output_buffer.getvalue(), language="text")

st.caption("Tip: Run this app with `streamlit run src/web_app.py`")
