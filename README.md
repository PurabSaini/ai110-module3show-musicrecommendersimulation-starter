# 🎵 Music Recommender Simulation

## Project Summary

This project is a small content-based music recommender I built to explore how a
scoring rule turns someone's taste into a ranked list of songs. You describe what
you like (a favorite genre, a favorite mood, a target energy level, and whether
you prefer acoustic songs), and the system scores every song in a small catalog
against those preferences and returns the top 5, each with a short reason for why
it was picked.

Under the hood, each feature acts as a weighted "judge" that returns a sub-score
between 0 and 1, and the weighted sub-scores are added into a single score
(genre matters most, then mood, then energy, then acousticness). It does not
learn from listening history or compare you to other users. It is a deliberately
simple, transparent model for seeing how feature weights shape the
recommendations you get.

---

## How The System Works

From my understanding, streaming platforms like Youtube and Spotify rely on collaborative-filtering and content-based filtering. The former compares users with similar likes and makes suggestions based on those similarities. The latter simply shows the user options that are similar in type/content based on what the user has liked before. For this project I plan on foucsing on content-based filtering.

- What features does each `Song` use in your system
  The features each `Song` uses in my system are genre, mood, energy, acousticness
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

---

## Experiments You Tried

### Reweighting: doubled energy, halved genre

I doubled the importance of energy (weight `1.5 → 3.0`) and halved the
importance of genre (weight `3.0 → 1.5`), leaving mood (2.0) and acoustic (1.0)
alone. This flips energy into the single most important feature and drops genre
to tie with mood for second.

How the system behaved:

- **The #1 pick didn't change** for any of the three built-in profiles. A song
  that already matched genre, mood, *and* energy still maxed out every term, so
  reweighting couldn't dislodge it.
- **The lower ranks reordered around energy instead of genre.** For *High-Energy
  Pop*, indie-pop "Rooftop Lights" jumped above same-genre "Gym Hero," and
  hip-hop "Concrete Dreams" pushed into the top 5 — genre no longer gate-kept the
  list.
- **A wrong-genre song overtook a right-genre one.** For *Chill Lofi*, ambient
  "Spacewalk Thoughts" rose above lofi "Focus Flow," because its energy was
  closer to the target and genre was no longer heavy enough to protect the lofi
  track.
- **Overall the recommendations clustered by energy level.** Songs with similar
  energy bunched together regardless of genre, and scores compressed (the gap
  between ranks shrank), making the list feel more "same-tempo" and less
  "same-style."

### Adversarial / edge-case profiles

To probe where the scoring rule produces surprising-but-valid results, I added
several deliberately awkward profiles to `USER_PROFILES` in `src/main.py`. Each
is well-formed input; the interesting part is the output. Running
`python -m src.main` produces:

**Conflict: Lofi + Intense** — genre and mood are scored independently, and no
song is both lofi *and* intense, so the `intense` request scores 0 and is
silently dropped. The results are all lofi chill/focused tracks:

```
Top recommendations for Conflict: Lofi + Intense:

Midnight Coding - Score: 4.67
Because: matches your favorite genre (lofi), energy (0.42) is close to your target

Focus Flow - Score: 4.57
Because: matches your favorite genre (lofi), energy (0.40) is close to your target

Library Rain - Score: 4.42
Because: matches your favorite genre (lofi), energy (0.35) is close to your target

Gym Hero - Score: 3.80
Because: matches your favorite mood (intense), not too acoustic

Storm Runner - Score: 3.78
Because: matches your favorite mood (intense), not too acoustic
```

**Ghost Mood: Sad** — no song has the mood `sad`, so the entire 2.0 mood weight
zeroes out and a mood=*intense* song wins for a "sad" user:

```
Top recommendations for Ghost Mood: Sad:

Gym Hero - Score: 5.41
Because: matches your favorite genre (pop), energy (0.93) is close to your target, not too acoustic

Sunrise City - Score: 5.20
Because: matches your favorite genre (pop), energy (0.82) is close to your target, not too acoustic

Neon Ascent - Score: 2.41
Because: energy (0.88) is close to your target, not too acoustic

Storm Runner - Score: 2.38
Because: energy (0.91) is close to your target, not too acoustic

Iron Verdict - Score: 2.37
Because: energy (0.97) is close to your target, not too acoustic
```

**Impossible: Loud + Acoustic** — high energy and a preference for acoustic
tracks pull in opposite directions (loud songs aren't acoustic). The genre/mood
match carries the winner, then the score cliffs hard to a runner-up that scores
1.54 yet reports "no strong matches" (score and explanation disagree):

```
Top recommendations for Impossible: Loud + Acoustic:

Iron Verdict - Score: 6.53
Because: matches your favorite genre (metal), matches your favorite mood (aggressive), energy (0.97) is close to your target

Rooftop Lights - Score: 1.54
Because: no strong matches

Storm Runner - Score: 1.51
Because: energy (0.91) is close to your target

Gym Hero - Score: 1.49
Because: energy (0.93) is close to your target

Coffee Shop Stories - Score: 1.49
Because: acoustic
```

**Niche Genre: Country** — country has only one song in the catalog, so it locks
slot #1 and the rest of the top-5 is filler that matches nothing on genre yet is
still presented as a "top pick":

```
Top recommendations for Niche Genre: Country:

Dusty Roads Home - Score: 7.18
Because: matches your favorite genre (country), matches your favorite mood (nostalgic), energy (0.45) is close to your target

Coffee Shop Stories - Score: 2.27
Because: energy (0.37) is close to your target, acoustic

Paper Boats - Score: 2.22
Because: energy (0.33) is close to your target, acoustic

Library Rain - Score: 2.21
Because: energy (0.35) is close to your target, acoustic

Focus Flow - Score: 2.21
Because: energy (0.40) is close to your target, acoustic
```

**Genre Loses: Jazz** — genre has the highest weight (3.0), but it's smaller
than mood + energy + acoustic combined (4.5), so the favorite-genre (jazz) song
ranks #3, behind two wrong-genre pop songs:

```
Top recommendations for Genre Loses: Jazz:

Sunrise City - Score: 4.32
Because: matches your favorite mood (happy), energy (0.82) is close to your target, not too acoustic

Rooftop Lights - Score: 4.06
Because: matches your favorite mood (happy), energy (0.76) is close to your target

Coffee Shop Stories - Score: 3.94
Because: matches your favorite genre (jazz)

Concrete Dreams - Score: 2.35
Because: energy (0.80) is close to your target, not too acoustic

Neon Ascent - Score: 2.35
Because: energy (0.88) is close to your target, not too acoustic
```

**All-Neutral** — with only `energy` set, every song clusters near the same
score and the ranking collapses to whoever sits nearest energy 0.5, with
identical reasons:

```
Top recommendations for All-Neutral:

Velvet Hours - Score: 1.50
Because: energy (0.50) is close to your target

Dusty Roads Home - Score: 1.42
Because: energy (0.45) is close to your target

Island Time - Score: 1.38
Because: energy (0.58) is close to your target

Midnight Coding - Score: 1.38
Because: energy (0.42) is close to your target

Focus Flow - Score: 1.35
Because: energy (0.40) is close to your target
```

---

## Limitations and Risks

- **Tiny catalog with thin coverage.** There are only 18 songs, and most genres
  have just one. Once the few real matches run out, the top 5 fills with songs
  that only happen to have the right energy, yet they are still labeled "top
  picks." A niche request like country locks slot #1 and then pads the list with
  unrelated filler.
- **Exact, word-for-word matching.** Genre and mood only count on an exact
  string match, so a song tagged "indie pop" scores zero for a "pop" fan even
  though a person would call it pop. A mood no song has (like "sad") silently
  zeroes out that whole term.
- **It understands none of the music itself.** No lyrics, language, artist
  similarity, or listening history are considered, and the catalog leans toward
  western pop and electronic styles, so it can quietly favor those listeners
  over others.

---

## Reflection

[**Model Card**](model_card.md)

