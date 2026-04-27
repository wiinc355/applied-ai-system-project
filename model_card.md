# 🎧 Model Card: VibeFinder 1.0

## Model Name
VibeFinder 1.0

---

## Required Reflection Questions

**1. What are the limitations or biases in your system?**

The biggest limitation is catalog coverage. With only 18 songs, some genres and moods are missing, so recommendations can look repetitive or forced. The strongest bias is toward high-energy tracks because the current scoring weights give energy a large influence; this can create a filter-bubble effect where songs like Gym Hero appear too often.

**2. Could your AI be misused, and how would you prevent that?**

This system could be misused to make overconfident claims about user preference quality, even though it is a classroom-scale prototype. To prevent misuse, I would:
- Keep explicit scope warnings in the UI and README
- Require explanation output with every recommendation
- Show evaluation metrics by default
- Block any claim that the system is production-ready or suitable for high-stakes personalization

**3. What surprised you while testing your AI's reliability?**

I was surprised that reliability and quality are different. The system was perfectly consistent (top-5 consistency = 1.00 across runs), but still produced weak results on adversarial profiles where catalog coverage was missing. That showed me a model can be stable and still be wrong for some user intents.

**4. Describe your collaboration with AI during this project. Identify one helpful suggestion and one flawed suggestion.**

Helpful suggestion: AI proposed adversarial profiles like Conflict: High Energy + Sad and Acoustic Techno, which exposed weaknesses that normal tests missed.

Flawed suggestion: AI-generated draft output initially included made-up recommendation examples that looked plausible but did not match live runs. I corrected this by replacing them with measured outputs from `python -m src.main` and pytest logs.
