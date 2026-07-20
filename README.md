# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

From my understanding, streaming platforms like Youtube and Spotify rely on collaborative-filtering and content-based filtering. The former compares users with similar likes and makes suggestions based on those similarities. The latter simply shows the user options that are similar in type/content based on what the user has liked before. For this project I plan on foucsing on content-based filtering.

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  The features each `Song` uses in my system are
    genre, mood, energy, acousticness
- What information does your `UserProfile` store
  Favorite genre, favorite mood, preferred energy, and preferred acousticness.
- How does your `Recommender` compute a score for each song

  Each feature acts as a "judge" that returns a sub-score between 0 and 1. Each
  sub-score is multiplied by a weight and the results are added together:

  ```
  score = 3.0·genre_sub + 2.0·mood_sub + 1.5·energy_sub + 1.0·acoustic_sub
  ```

  Because every sub-score is on the same 0–1 scale, the weights alone decide how
  important each feature is. The maximum possible score is 7.5.

  | Feature | Weight | Match type | Sub-score rule (0–1) |
  |---------|--------|------------|----------------------|
  | genre | 3.0 | Exact | `1.0` if `song.genre == favorite_genre`, else `0.0` |
  | mood | 2.0 | Exact | `1.0` if `song.mood == favorite_mood`, else `0.0` |
  | energy | 1.5 | Closeness | `max(0, 1 - abs(song.energy - target_energy))` |
  | acousticness | 1.0 | Directional | `song.acousticness` if `likes_acoustic`, else `1 - song.acousticness` |

- How do you choose which songs to recommend
  I return the k number of songs with the highest scores. 

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` with the sample user profile `{"genre": "pop", "mood": "happy", "energy": 0.8}` produces:

```
Top recommendations:

Sunrise City - Score: 6.47
Because: matches your favorite genre (pop), matches your favorite mood (happy), energy (0.82) is close to your target

Gym Hero - Score: 4.30
Because: matches your favorite genre (pop), energy (0.93) is close to your target

Rooftop Lights - Score: 3.44
Because: matches your favorite mood (happy), energy (0.76) is close to your target

Concrete Dreams - Score: 1.50
Because: energy (0.80) is close to your target

Night Drive Loop - Score: 1.42
Because: energy (0.75) is close to your target
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



