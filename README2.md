# VibeFinder 1.0 — Music Recommender System

> A content-based AI music recommender built as an applied AI systems project.
> Designed for clarity, testability, and honest evaluation of how simple scoring rules behave in practice.

---

## Original Project Reference

**Original project:** Music Recommender Simulation (CodePath AI110, Modules 1–3)

The original project established a song catalog stored in `data/songs.csv` and a user taste-profile concept. Its initial goal was to explore how content-based filtering works by assigning numeric scores to songs based on how closely their features matched a single user's preferences. The project built foundational scoring logic for genre, mood, and audio features such as energy, tempo, valence, danceability, and acousticness, and surfaced those scores as ranked top-5 recommendation lists with plain-language explanations.

---

## Title and Summary

**VibeFinder 1.0** is a content-based music recommendation system that scores songs against a user taste profile and returns ranked recommendations with score explanations. It is built entirely in Python, runs from the command line or a Streamlit web app, and includes automated evaluation metrics and a full pytest test suite.

**Why it matters:** Most people interact with AI recommenders every day without understanding how they work. This project makes the scoring process transparent — every recommendation comes with a written reason — so users and developers can inspect, question, and improve the logic. That same philosophy of explainability is what makes AI systems trustworthy and auditable in production settings.

---

## Architecture Overview

```
flowchart TD
    user[Human user or presenter] --> ui[CLI runner or Streamlit web app]
    ui --> profile[User profile input]
    data[(songs.csv catalog)] --> loader[load_songs]
    profile --> recommender[Recommender and scoring logic]
    loader --> recommender
    recommender --> recs[Ranked recommendations with explanations]
    recommender --> evaluator[Evaluation metrics]
    profile --> evaluator
    loader --> evaluator
    evaluator --> report[Metrics report and top-song summaries]
    ui --> tester[Pytest test runner]
    tester --> checks[Test results]
    recs --> humancheck[Human reviews recommendations]
    report --> humancheck
    checks --> humancheck
```

See the full rendered diagram: [assets/system_diagram.svg](assets/system_diagram.svg) | [assets/system_diagram.png](assets/system_diagram.png)

### Component Roles

| Component | File | Role |
|---|---|---|
| Data loader | `src/recommender.py` | Reads `songs.csv` into typed dictionaries |
| Recommender | `src/recommender.py` | Scores every song against the user profile and ranks results |
| Evaluator | `src/evaluation.py` | Computes consistency, diversity, mood alignment, and feature-distance metrics |
| CLI runner | `src/main.py` | Runs all profiles in the terminal and prints the full report |
| Web UI | `src/web_app.py` | Streamlit interface for live demos, custom profiles, and test runs |
| Test suite | `tests/` | Pytest tests covering standard, adversarial, and edge-case profiles |

**Data flow (short form):**
User profile + `songs.csv` → Recommender scores each song → Ranked list with explanations → Evaluator computes metrics → Human reviews output → Tests verify behavior

---

## Setup Instructions

### Prerequisites
- Python 3.10 or later
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/wiinc355/applied-ai-system-project.git
   cd applied-ai-system-project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   .venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the CLI recommender**
   ```bash
   python -m src.main
   ```

5. **Launch the Streamlit web demo** *(optional)*
   ```bash
   streamlit run src/web_app.py
   ```
   Then open: [http://localhost:8501](http://localhost:8501)

6. **Run the test suite**
   ```bash
   pytest -q
   ```

---

## Sample Interactions

> All outputs below are real — captured by running `python -m src.main` against `data/songs.csv`.

### Example 1 — Chill Lofi profile

**Input:**
```python
{
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35,
    "tempo_bpm": 78,
    "valence": 0.58,
    "danceability": 0.60,
    "acousticness": 0.85,
}
```

**Verified output (top 5 from actual run):**
```
Top songs: Library Rain, Midnight Coding, Focus Flow,
           Spacewalk Thoughts, Coffee Shop Stories

Evaluation metrics (measured):
  Top-5 consistency across 5 runs : 1.00  ✓ fully deterministic
  Genre diversity in top-5         : 0.60
  Mood alignment score             : 0.60
  Feature-distance score           : 0.06  (lower is better)
```

**What this proves:** The system is deterministic (consistency = 1.00) and returns low-energy, acoustic songs as expected. Mood alignment of 0.60 means 3 of the 5 songs matched the "chill" mood label exactly — honest, not inflated.

---

### Example 2 — Adversarial profile: Conflict: Acoustic Techno

**Input:**
```python
{
    "genre": "techno",
    "mood": "serene",
    "energy": 0.90,
    "tempo_bpm": 130,
    "valence": 0.45,
    "danceability": 0.90,
    "acousticness": 0.95,
}
```

**Verified output (top 5 from actual run):**
```
Top songs: Gym Hero, Afterglow Circuit, Storm Runner,
           Rooftop Lights, Night Drive Loop

Evaluation metrics (measured):
  Top-5 consistency across 5 runs : 1.00  ✓ stable even on conflicting input
  Genre diversity in top-5         : 1.00  (5 different genres — no catalog match)
  Mood alignment score             : 0.00  ✗ no serene songs in top-5
  Feature-distance score           : 0.27  (higher — numeric mismatch expected)
```

**What this proves:** The system does not crash on impossible inputs. Mood alignment = 0.00 is the honest result — no techno songs exist in the catalog, so the recommender can only return numerically close songs. This is a documented, measurable limitation, not a hidden failure.

---

### Example 3 — High-Energy Pop profile

**Input:**
```python
{
    "genre": "pop",
    "mood": "happy",
    "energy": 0.90,
    "tempo_bpm": 124,
    "valence": 0.85,
    "danceability": 0.85,
    "acousticness": 0.15,
}
```

**Verified output (top 5 from actual run):**
```
Top songs: Sunrise City, Gym Hero, Rooftop Lights,
           Afterglow Circuit, Neon Bazaar

Evaluation metrics (measured):
  Top-5 consistency across 5 runs : 1.00  ✓ fully deterministic
  Genre diversity in top-5         : 0.80  (4 of 5 genres distinct)
  Mood alignment score             : 0.40
  Feature-distance score           : 0.07  (very close to target)
```

**What this proves:** Feature-distance of 0.07 (near-zero) confirms the top songs are genuinely close to the requested audio profile, not just lucky genre matches. Mood alignment of 0.40 reflects that only 2 of 5 catalog songs labeled "happy" ranked in the top 5 — accurate given the 18-song catalog size.

---

## Design Decisions

### Content-based filtering over collaborative filtering
**Decision:** Score each song against one user profile using explicit feature weights.
**Trade-off:** This is transparent and explainable but does not learn from user behavior over time. A collaborative approach would be more accurate at scale but far harder to audit or explain in a classroom context.

### Explicit numeric weights
**Decision:** Hard-coded weights (e.g. genre match = +1.0, energy weight = 3.0).
**Trade-off:** Easy to change and reason about. The downside is that one weight dominates when set too high. The energy weight experiment confirmed this — doubling it from 1.5 to 3.0 caused energetic songs to flood results across almost every profile.

### Small CSV catalog over an external API
**Decision:** Use a local 18-song CSV.
**Trade-off:** Makes the project self-contained, fast, and fully inspectable. But with only 18 songs, niche genres like techno have zero representatives, so adversarial profiles always fall back to nearest-numeric-neighbor behavior.

### Streamlit web UI alongside CLI
**Decision:** Add a browser-based demo interface to the existing CLI script.
**Trade-off:** Makes class demos much smoother (no terminal required). The cost was extra code in `web_app.py` and a dependency on Streamlit's server.

### Four evaluation metrics
**Decision:** Track top-k consistency, genre diversity, mood alignment, and feature distance.
**Trade-off:** These four metrics catch four distinct failure modes (instability, filter bubbles, mood mismatch, numeric drift). Adding more metrics would increase observability but also add noise.

---

## Testing Summary

### Automated tests — pytest

**Result: 10 out of 10 tests passed** (run: `pytest -v`)

```
tests/test_evaluation.py::test_top_k_consistency_is_1_for_deterministic_recommender  PASSED
tests/test_evaluation.py::test_genre_diversity_score_in_range                        PASSED
tests/test_evaluation.py::test_mood_alignment_score_in_range                         PASSED
tests/test_evaluation.py::test_feature_distance_lower_for_closer_profile             PASSED
tests/test_evaluation.py::test_evaluate_profile_returns_all_metrics                  PASSED
tests/test_evaluation.py::test_standard_profiles_return_relevant_top_results         PASSED
tests/test_evaluation.py::test_adversarial_profiles_still_return_stable_metrics      PASSED
tests/test_evaluation.py::test_out_of_range_and_rare_inputs_do_not_crash_and_return_top_k  PASSED
tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score              PASSED
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string      PASSED

10 passed in 0.03s
```

### Confidence scoring — measured evaluation metrics

All five profiles were run with `python -m src.main`. Results measured across 5 independent runs:

| Profile | Consistency | Genre Diversity | Mood Alignment | Feature Distance |
|---|---|---|---|---|
| High-Energy Pop | 1.00 | 0.80 | 0.40 | 0.07 |
| Chill Lofi | 1.00 | 0.60 | 0.60 | 0.06 |
| Deep Intense Rock | 1.00 | 1.00 | 0.40 | 0.14 |
| Conflict: High Energy + Sad | 1.00 | 0.80 | 0.00 | 0.27 |
| Conflict: Acoustic Techno | 1.00 | 1.00 | 0.00 | 0.27 |

**Summary:** Consistency = 1.00 across all profiles — the recommender is fully deterministic. Feature-distance averaged 0.11 across standard profiles (low = close to target). The AI struggled when context was missing: mood alignment dropped to 0.00 for profiles requesting genres (techno) or moods (sad, serene) with no matching songs in the 18-song catalog.

### Human evaluation

All five profile outputs were reviewed manually after each run. Standard profiles (Chill Lofi, High-Energy Pop, Deep Intense Rock) returned results that felt intuitive and matched the requested vibe. Adversarial profiles exposed two documented weaknesses:
- **Mood mismatch:** Conflict: High Energy + Sad returned zero mood-aligned songs because the scoring formula treats energy as a stronger signal than mood.
- **Genre miss:** Conflict: Acoustic Techno returned no techno songs at all — the catalog simply has none, and the system fell back to nearest-numeric-neighbor behavior.

### What worked
- 10/10 automated tests passed on first run, including adversarial and edge-case inputs.
- Consistency = 1.00 on all profiles proves the output is stable and regression-testable.
- Feature-distance = 0.06–0.07 for standard profiles confirms recommendations are numerically close to the requested audio profile.

### What did not work as expected
- **Energy filter bubble:** After doubling energy weight to 3.0, Gym Hero appeared in the top 5 for every profile regardless of genre or mood intent. Genre diversity fell for adversarial profiles.
- **Genre miss:** Techno and serene mood have no catalog representatives, so mood alignment = 0.00 is unavoidable at this catalog size.

### Lessons learned
1. **10/10 tests passed; the AI struggled only when catalog coverage was missing** — not a logic bug, a data gap.
2. Consistency scores of 1.00 confirmed the system is deterministic and safe to regression-test after weight changes.
3. Evaluation metrics made silent failures visible: mood alignment = 0.00 is easy to miss in a manual review but impossible to miss in a metrics table.

---

## Reflection

Building VibeFinder forced me to confront a core truth about AI systems: **the output is only as trustworthy as the logic behind the score.** When I could read every scoring reason line by line, I understood exactly why a surprising recommendation appeared. That transparency is something most real AI systems deliberately hide.

The weight-shift experiment was the most educational moment. A single number change (energy weight 1.5 → 3.0) transformed the system's behavior across every profile. That taught me that AI is not magic — it is math with consequences, and the people who set the weights are making value judgments whether they realize it or not.

Working with AI coding tools throughout this project showed me a new kind of collaboration. The tools were fastest at generating test profiles, suggesting edge cases, and drafting boilerplate. But they could not tell me whether the recommendation *felt right* for a given profile. That judgment required running the system, reading the output, and thinking about what a real user would expect. Human oversight was not optional — it was the most important step in every iteration.

If I continued this project, I would:
1. Expand the catalog to at least 100 songs with balanced genre coverage.
2. Add a diversity rule so the top 5 cannot all come from the same genre.
3. Learn weights per user from feedback rather than using one fixed set.
4. Add a RAG component so users can ask natural language questions like "find me something like Library Rain but more upbeat."

This project taught me that AI and problem-solving are not separate skills. Every design decision was both a technical choice and a question about what matters to the user — and answering that question well is what separates useful AI from impressive-but-unreliable AI.

---

## Project Structure

```
applied-ai-system-project/
├── assets/
│   ├── system_diagram.mmd      # Mermaid source
│   ├── system_diagram.svg      # Rendered SVG
│   └── system_diagram.png      # Rendered PNG
├── data/
│   └── songs.csv               # 18-song catalog
├── docs/
│   └── *.png                   # CLI output screenshots
├── src/
│   ├── recommender.py          # Core scoring and ranking logic
│   ├── evaluation.py           # Metrics: consistency, diversity, alignment, distance
│   ├── main.py                 # CLI runner
│   └── web_app.py              # Streamlit web UI
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── test_recommender.py     # Unit tests for scoring logic
│   └── test_evaluation.py      # Unit tests for evaluation metrics
├── model_card.md               # Model behavior, biases, and intended use
├── reflection.md               # Profile comparison notes
├── recommendation_flowchart.mmd# Scoring algorithm flowchart
├── requirements.txt
└── README2.md                  # This file
```

---

*Built with Python · Streamlit · pytest · Mermaid*
*CodePath AI110 — Applied AI Systems, Unit 9*
