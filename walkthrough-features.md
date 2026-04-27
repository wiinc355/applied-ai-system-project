Perfect project for this. Here is a ready-to-record walkthrough plan that maps directly to all 4 requirements.

1) End-to-End System Run (2–3 inputs)
Record this in your Streamlit app so viewers can see input → AI process → output.

1.	Start app
Command: streamlit run web_app.py
Then open the local URL shown in terminal.

2. Input Case A (normal profile)
Use the existing “High-Energy Pop” profile behavior.

Show output highlights:
•	Top songs: Sunrise City, Gym Hero, Rooftop Lights, Afterglow Circuit, Neon Bazaar
•	Metrics: consistency 1.00, mood alignment 0.40, feature-distance 0.07

3.	Input Case B (normal but different vibe)
Use “Chill Lofi”.

Show output highlights:
•	Top songs: Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories
•	Metrics: consistency 1.00, mood alignment 0.60, feature-distance 0.06

4.	Input Case C (adversarial/conflicting)
Use “Conflict: Acoustic Techno” in Custom Profile Playground.
Show output highlights:
•	Top songs: Gym Hero, Afterglow Circuit, Storm Runner, Rooftop Lights, Night Drive Loop
•	Metrics: consistency 1.00, mood alignment 0.00, feature-distance 0.27
•	Explain: this proves the system still runs, but reveals a known limitation when catalog coverage is missing.

2) AI Feature Behavior (what your AI is actually doing)
Say this clearly in video:

•	“This is a content-based recommender AI. It scores each song against a user profile using genre, mood, energy, tempo, valence, danceability, and acousticness.”

•	“It returns ranked recommendations plus score explanations, so the AI behavior is inspectable.”
•	“It is not RAG; instead, its AI feature is transparent scoring and ranking.”
If you want to point to code:

•	Recommender logic: recommender.py
•	Evaluation logic: evaluation.py
•	Demo UI: web_app.py

3) Reliability / Guardrail or Evaluation Behavior
Show both automated and human-style checks.

1.	Automated reliability
Command: pytest -v
Say: “All 10 tests pass, including adversarial and edge-case checks.”

2.	Evaluation guardrails
Click “Show Evaluation Metrics” in app and explain:

•	Consistency across runs
•	Genre diversity
•	Mood alignment
•	Feature-distance (lower is better)

3.	Human evaluation
Say: “I manually review whether top songs match expected vibe and use the metric table to catch silent failures.”

4) Clear Outputs for Each Case
Use this format on screen each time:

•	Input profile values
•	Top 5 output songs
•	3 metric numbers minimum (consistency, mood alignment, feature-distance)
•	One sentence interpretation

Example interpretation lines:

•	“Case A: low feature-distance means strong profile match.”
•	“Case B: mood alignment improved versus Case A.”
•	“Case C: mood alignment 0.00 shows catalog limitation, not a crash.”
