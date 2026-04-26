# 🎧 Model Card: VibeFinder 1.0

## Model Name
VibeFinder 1.0

## Goal / Task
This recommender suggests songs that match one user's taste profile. It tries to rank songs by how close they are to the user's preferred genre, mood, and audio features.

## Data Used
The catalog has 18 songs from `data/songs.csv`. Each song includes genre, mood, energy, tempo, valence, danceability, and acousticness. I expanded the starter data to include more genres and moods, but the dataset is still small. That means some styles have very few examples, so recommendations can repeat.

## Algorithm Summary
Each song starts at score 0. The system adds points for genre and mood matches, then adds similarity points for numeric features like energy and tempo. Songs that are closer to the user's target values get more points. After scoring all songs, the model sorts them from highest to lowest and returns the top results with reasons.

## Observed Behavior / Biases
I found an energy-based filter bubble during testing. After increasing energy weight, high-energy songs appeared near the top for many different profiles, even when genre intent was different. This can make songs like Gym Hero show up too often. The small catalog makes this worse because there are not enough alternatives for some user types.

## Evaluation Process
I tested five profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflict: High Energy + Sad, and Conflict: Acoustic Techno. I compared whether the top 5 songs felt reasonable for each profile. Chill Lofi looked accurate, but adversarial profiles showed surprises. I also ran a logic experiment by halving genre weight and doubling energy weight, then checked how rankings changed.

## Intended Use and Non-Intended Use
Intended use: classroom exploration of how recommender systems score and rank items. It is useful for learning, debugging, and discussing bias.

Non-intended use: real music product decisions, high-stakes personalization, or any case where fairness and broad user coverage are required. The dataset is too small and the scoring rules are too simple for production use.

## Ideas for Improvement
1. Add more songs with better balance across genres, moods, and energy levels.
2. Add a diversity rule so the top 5 are not all the same vibe.
3. Learn profile weights per user instead of using one fixed weighting scheme.

## Personal Reflection
My biggest learning moment was seeing how a small weight change created a big ranking change. When I doubled energy weight, the system started pushing energetic songs for many profiles, even when genre intent was different. AI tools helped me move faster by generating profile ideas, drafting tests, and suggesting edits, but I had to double-check outputs by running the program and reading the score reasons line by line. I was surprised that a simple scoring formula can still feel like a real recommender when it gives ranked results with explanations. If I extend this project, I want to add more songs, tune weights with feedback, and add a diversity rule so users do not keep seeing the same few tracks.
