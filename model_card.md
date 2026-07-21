# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Vibecheck 1.0**  

---

## 2. Intended Use  

Vibecheck is a music recommender. It is built for classroom exploration, not for real users.

You tell it what you like: a favorite genre, a favorite mood, an energy level, and whether you like acoustic songs. It looks at a small list of songs and gives you the 5 that fit best. Each pick comes with a short reason for why it was chosen.

It makes a few assumptions about you:

- You can name your taste up front.
- Your taste stays the same during a session.

It does not learn from your listening history. It does not compare you to other people. It does not read lyrics or understand context. It is a tool for learning how a scoring rule turns taste into recommendations.

---

## 3. How the Model Works  

Vibecheck looks at four things about each song: its genre, its mood, its energy (how loud and lively it is), and how acoustic it is.

For each song, it gives out points. A song earns points for matching each aspect mentioned above. All the points are added up into one score. Then it sorts every song by score and hands you the top 5.

---

## 4. Data  

The catalog has 18 songs. Each song has a genre, a mood, an energy level, a tempo, and a few other traits.

There are 15 genres, like pop, lofi, rock, jazz, hip hop, metal, and edm. There are lots of moods too, like happy, chill, intense, and nostalgic.

Some parts of musical taste are missing. Most genres only have one song, so there is not much to pick from. The list is small and leans toward western pop and electronic styles. There is no way to say you like more than one genre at once.

---

## 5. Strengths  

Vibecheck works best for people with clear, strong taste.

When someone knows their favorite genre and mood, and those songs exist in the catalog, the #1 pick is spot on. This was true for all three test listeners: the pop fan, the lofi fan, and the rock fan each got a perfect top song.

It is good at matching energy. If you want loud and lively songs, it finds loud and lively songs. If you want quiet and mellow, it finds those too.

Every pick also comes with a short reason. So you can see why a song was chosen, not just that it was chosen.

---

## 6. Limitations and Bias 

When a user has only mild or mixed preferences, the genre and mood terms pay out almost nothing, so the energy term is left to decide the ranking. But energy acts as a near-flat baseline given to every song, so the scores bunch into near-ties and the list collapses to whatever sits closest to the middle energy (~0.5) — like Velvet Hours and Dusty Roads Home in the All-Neutral output. So an eclectic listener isn't served their own taste; they just get the catalog's average.

---

## 7. Evaluation  

### The three test listeners

I set up three make-believe listeners and gave each one a top-5 list of song suggestions:

- **High-Energy Pop** — loves upbeat pop and wants loud, lively songs.
- **Chill Lofi** — loves quiet, mellow study music.
- **Deep Intense Rock** — loves hard, high-energy rock.

### What I found

**The good news:** each listener's #1 pick was exactly right. The pop fan's top song was a bright pop song, the lofi fan's was a mellow study track, and the rock fan's was a driving rock song. When someone's taste is clear, the app nails the first pick.

**The surprise:** the lists fall apart fast after the first pick or two. Once the app runs out of songs that truly fit, it fills the remaining slots with songs that only happen to have about the right loudness — and it still labels them "top picks." So the pop fan ends up with an EDM song and a rock song in their list, even though those aren't pop at all.

Two smaller quirks stood out:

- The app only counts a genre if the label matches *word for word*. A song tagged "indie pop" scores zero for a "pop" fan, even though anyone would call it a pop song.
- A song from the "wrong" genre can still beat the right ones if it matches the listener's mood and energy — so a pop song slipped into the rock fan's list ahead of actual rock tracks.

### How the listeners compared

- **Pop vs. Lofi:** total opposites — loud vs. quiet, energetic vs. mellow. Their lists had *no songs in common*, which makes sense: they want opposite things.
- **Pop vs. Rock:** both want loud, high-energy songs and only differ on style. So their #1 picks were different, but the bottoms of their lists overlapped — several loud songs showed up for *both*. That's expected, since they agree on the "loud and lively" part.
- **Lofi vs. Rock:** the cleanest split. One wants soft and quiet, the other loud and intense, so again no shared songs.

The pattern: two listeners overlap only when they agree on loudness. When they disagree on that, even the leftover filler songs don't match.

---

## 8. Future Work  

There are two main things I would improve next.

First, I would make the catalog much bigger. Right now most genres only have one song. With more songs, there would be real choices for every kind of listener, and the lists would not fill up with filler.

Second, I would handle more complex tastes. Right now you can only pick one genre and one mood. I would let people like more than one genre, or blend styles, so the app can serve people whose taste is mixed instead of just people with one clear favorite.

---

## 9. Personal Reflection  

I enjoyed learning how apps like YouTube and Spotify recommend content. They use scoring algorithms and other methods to rank songs and videos for each user. Building a small version of this helped me see how those apps turn simple data about your taste into a ranked list.

The surprising part was how easily a simple scoring rule can go wrong. My app nailed the top pick every time, but the rest of the list often filled up with songs that did not really fit. It made me realize that the recommendations I see every day are just numbers being added up, and small choices about how you weight those numbers can change a lot.
