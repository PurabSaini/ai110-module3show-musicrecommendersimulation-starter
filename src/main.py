"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


# Distinct user preference profiles. Each dict uses the keys understood by
# score_song: genre, mood, energy (0.0-1.0), and likes_acoustic.
USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---------------------------------
    # These are all well-formed inputs; the point is the surprising output
    # each produces, not invalid data. Each comment names the scoring
    # weakness it probes.

    # genre and mood are independent exact matches with no consistency check:
    # no song is both lofi AND intense, so the intense request scores 0 and is
    # silently dropped -- the top picks are lofi chill/focused tracks.
    "Conflict: Lofi + Intense": {
        "genre": "lofi",
        "mood": "intense",
        "energy": 0.5,
        "likes_acoustic": False,
    },
    # a categorical value no song has ("sad") zeroes out its entire 2.0 weight,
    # so mood vanishes and a mood=intense song wins for a "sad" user.
    "Ghost Mood: Sad": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # energy and acoustic terms pull opposite directions -- loud songs are
    # never acoustic -- so likes_acoustic is effectively inert for the winner,
    # then the score cliffs hard to a "no strong matches" runner-up.
    "Impossible: Loud + Acoustic": {
        "genre": "metal",
        "mood": "aggressive",
        "energy": 0.97,
        "likes_acoustic": True,
    },
    # a single-song genre locks slot #1, then the rest of the top-5 is filler
    # that matches nothing on genre yet is still presented as a top pick.
    "Niche Genre: Country": {
        "genre": "country",
        "mood": "nostalgic",
        "energy": 0.45,
        "likes_acoustic": True,
    },
    # the "most important" 3.0 genre weight is smaller than mood+energy+acoustic
    # combined (4.5), so the favorite-genre (jazz) song ranks below wrong-genre
    # pop songs that match the other three features.
    "Genre Loses: Jazz": {
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.82,
        "likes_acoustic": False,
    },
    # energy is a soft, near-flat term; with nothing else set, every song
    # clusters near the same score and order collapses to whoever sits nearest
    # 0.5, with identical reasons.
    "All-Neutral": {
        "energy": 0.5,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop recommendations for {name}:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
