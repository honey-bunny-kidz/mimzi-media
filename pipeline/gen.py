"""Generate Mimzi episodes 02-30 (scripts + YouTube metadata) from the channel plan."""
import json, datetime

M, MW, T, N = "mimzi", "mimzi_wave", "teddy", "narrator"
NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
SHARE = "Share Mimzi with a friend, and subscribe for more learning fun!"


def L(who, text, pause=None, **kw):
    d = {"who": who, "text": text}
    if pause is not None:
        d["pause"] = pause
    d.update(kw)
    return d


def clap(who=MW):
    return {"who": who, "sfx": "clap", "text": "", "dur": 1.0, "pause": 0.3}


def S(bg, cast, lines, **kw):
    d = {"bg": bg, "cast": cast, "lines": lines, "lead": kw.pop("lead", 0.35) + 0.15, "tail": kw.pop("tail", 0.45) + 0.2}
    d.update(kw)
    return d


def trio(card, wide=False):
    return [{"id": M, "x": 0.13 if wide else 0.18}, {"id": card, "x": 0.52, "pop": True}, {"id": T, "x": 0.89 if wide else 0.85}]


def duo():
    return [{"id": MW, "x": 0.3}, {"id": T, "x": 0.7}]


def intro(bg, banner, lines, prop=None):
    cast = duo() if not prop else [{"id": MW, "x": 0.2}, {"id": prop, "x": 0.52, "pop": True}, {"id": T, "x": 0.85}]
    return S(bg, cast, lines, banner=banner, lead=0.3)


def outro(bg, teaser, extra=None, prop=None):
    cast = duo() if not prop else [{"id": MW, "x": 0.18}, {"id": prop, "x": 0.52, "pop": True}, {"id": T, "x": 0.86}]
    if prop == "abc_strip":
        cast[1].update(x=0.5, y=0.48, scale=0.88)
    lines = (extra or []) + [L(T, "Great job, little learner!"), L(N, SHARE), L(MW, teaser + " Bye bye!", 1.0)]
    return S(bg, cast, lines, fade=True)


EPS = []


CHEERS = ["Yes! Well done!", "That's right!", "Great job!", "You got it!", "Super!", "Hooray!"]


def review_q(cid, mode):
    p = cid.split(":")
    k = p[0]
    if cid.startswith("card_"):
        return "What letter is this?", f"{cid[5]}!"
    if k == "w":
        lab = (p[2] if len(p) > 2 else p[1]).replace("teddy_i", "teddy").replace("_", " ")
        q = "What happened here?" if mode == "story" else "What is this?"
        return q, f"{lab[0].upper() + lab[1:]}!"
    if k == "n":
        return "How many? Let's count!", ", ".join(NUMW[i] for i in range(1, int(p[1]) + 1)).capitalize() + "!" if int(p[1]) <= 6 else f"{NUMW[int(p[1])].capitalize()}!"
    if k == "c":
        return "What color is this?", f"{p[1].capitalize()}!"
    if k == "s":
        return "What shape is this?", f"{'An' if p[1][0] in 'aeiou' else 'A'} {p[1]}!"
    if k == "t":
        return "What do we say?", p[1]
    if k == "o":
        return f"Can you find {p[1]} and {p[2]}?", f"{p[1].capitalize()} and {p[2]}!"
    return None


def add_review(scenes, mode, extra_q=None):
    """Second half of the video: a gentle memory game over the cards just learned (or story questions)."""
    bg = scenes[-1]["bg"] if scenes[-1]["bg"] != "mz_bedroom_night" else scenes[-2]["bg"]
    ids, bgs = [], {}
    for sc in scenes[1:-1]:
        for c in sc["cast"]:
            if c.get("pop") and c["id"] not in ids and review_q(c["id"], mode):
                ids.append(c["id"]); bgs[c["id"]] = sc["bg"]
    if len(ids) > 12:
        ids = [ids[round(i * (len(ids) - 1) / 11)] for i in range(12)]
    if not ids and not extra_q:
        return scenes
    rev = [S(bg, duo(), [L(MW, "Now let's play a memory game!" if mode != "story" else "Did you like the story? Let's remember it together!"),
                         L(T, "Do you remember? Let's see!")], fade=True)]
    for i, cid in enumerate(ids):
        q, a = review_q(cid, mode)
        wide = cid.startswith("o:") or cid.startswith("seq:")
        rev.append(S(bgs[cid], trio(cid, wide), [L(N, q, 2.2), L(M, a), L(T, CHEERS[i % len(CHEERS)])]))
    for q, a, card in (extra_q or []):
        rev.append(S(bg, trio(card) if card else duo(), [L(N, q, 2.2), L(M, a), L(T, CHEERS[len(rev) % len(CHEERS)])]))
    rev.append(S(bg, duo(), [L(MW, "Wow! You remembered everything!"), clap(T), L(T, "You are a super learner!")]))
    return scenes[:-1] + rev + scenes[-1:]


def ep(num, slug, title, desc, tags, thumb, scenes, review="quiz", extra_q=None, **kw):
    if review:
        scenes = add_review(scenes, review, extra_q)
    e = {"num": num, "slug": slug, "title": title, "desc": desc, "tags": tags, "thumbnail": thumb, "scenes": scenes}
    e.update(kw)
    EPS.append(e)


def th(text, badge, card, bg="mz_playroom"):
    return {"text": text, "badge": badge, "bg": bg, "cast": [{"id": M, "mouth": 2, "x": 0.6}, {"id": card, "scale": 0.72, "x": 0.86}, {"id": T, "x": 0.95}]}


# ------------------------------------------------------------------ 02 Letters A B C
def ep02():
    bg = "mz_playroom"
    sc = [intro(bg, "Letters A, B, C!", [L(MW, "Hi friends! It's me, Mimzi, and my friend Teddy!"), L(T, "Hello!"),
                                          L(MW, "Today we'll learn three letters. A, B and C!")], prop="seq:A,B,C")]
    groups = [("A", [("apple", "apple"), ("ant", "ant"), ("alligator", None)]), ("B", [("ball", "ball"), ("banana", "banana"), ("book", "book"), ("bee", "bee")]),
              ("C", [("cat", "cat"), ("car", "car"), ("cup", "cup"), ("cow", "cow")])]
    for Lt, words in groups:
        sc.append(S(bg, trio("card_" + Lt), [L(N, f"This is the letter {Lt}.", 0.6), L(M, f"{Lt}! Can you say {Lt}?", 1.6), L(T, f"{Lt}!")]))
        for wd, ic in words:
            if ic is None:
                continue
            sc.append(S(bg, trio("w:" + ic), [L(N, f"{wd.capitalize()} starts with {Lt}.", 0.5), L(M, f"{Lt}, {Lt}, {wd}!")]))
    for wd, Lt in (("ball", "B"), ("cat", "C"), ("apple", "A")):
        sc.append(S(bg, trio("w:" + wd), [L(N, f"Which letter does {wd} start with?", 2.2), L(M, f"{Lt}! {wd.capitalize()} starts with {Lt}!"), clap(M)]))
    sc.append(outro(bg, "Next time, let's learn our first ten words.", [L(MW, "Yay! We learned A, B and C!")], prop="seq:A,B,C"))
    ep(2, "abc_letters", "Learn Letter A, B, C | First Words and Alphabet Sounds for Toddlers",
       "Mimzi and Teddy learn the letters A, B and C with first words: apple, ball, banana, cat, car and more. Little ones guess which letter each word starts with.",
       ["LetterA", "ABC", "AlphabetForToddlers", "FirstWords", "ToddlerLearning", "Mimzi"], th("A B C!", "First Letters", "card_B"), sc)


# ------------------------------------------------------------------ word-list videos (03, 06, 09)
def wordlist(num, slug, title, desc, tags, thumb, bg, banner, hello, words, teaser, quick=False, recap=True):
    sc = [intro(bg, banner, [L(MW, "Hi friends! I'm Mimzi, and this is Teddy!"), L(T, "Hi, hi!"), L(MW, hello)])]
    for i, (ic, wd, art_) in enumerate(words):
        a = f"{art_} {wd}" if art_ else wd
        if quick:
            lines = [L(N, f"{wd.capitalize()}.", 0.6), L(M, f"{wd.capitalize()}!")]
        elif i % 3 == 2:
            lines = [L(N, "What is this?", 1.8), L(M, f"It's {a}! {wd.capitalize()}!"), L(T, f"{wd.capitalize()}!")]
        else:
            lines = [L(N, f"This is {a}.", 0.5), L(M, f"{wd.capitalize()}! Can you say {wd}?", 1.5)]
        sc.append(S(bg, trio(f"w:{ic}:{wd}"), lines))
        if (i + 1) % 5 == 0 and i + 1 < len(words):
            sc.append(S(bg, duo(), [L(MW, "You're doing so well! Give Teddy a clap!"), clap(T)]))
    if recap:
        sc.append(S(bg, duo(), [L(N, "Let's say them all again, nice and fast!"), L(MW, ", ".join(w[1] for w in words) + "!", 0.6)]))
    sc.append(outro(bg, teaser, [L(MW, "Hooray! We learned so many words!")]))
    ep(num, slug, title, desc, tags, thumb, sc)


def ep03():
    words = [("ball", "ball", "a"), ("book", "book", "a"), ("cup", "cup", "a"), ("car", "car", "a"), ("cat", "cat", "a"),
             ("dog", "dog", "a"), ("shoe", "shoe", "a"), ("spoon", "spoon", "a"), ("bed", "bed", "a"), ("teddy_i", "teddy", "a")]
    wordlist(3, "first_10_words", "First 10 English Words for Toddlers | Early Vocabulary Learning",
             "Ten first words for toddlers with Mimzi and Teddy: ball, book, cup, car, cat, dog, shoe, spoon, bed and teddy. Clear words, pictures and time to say each one.",
             ["FirstWords", "ToddlerVocabulary", "LearnEnglish", "BabyFirstWords", "ToddlerLearning", "Mimzi"], th("First Words!", "10 Easy Words", "w:ball"),
             "mz_playroom", "My First 10 Words", "Let's learn ten first words. Ready? Let's go!", words, "Next time, let's meet some animals and hear their sounds.")


def ep06():
    words = [("chair", "chair", "a"), ("table", "table", "a"), ("bed", "bed", "a"), ("door", "door", "a"), ("window", "window", "a"),
             ("lamp", "lamp", "a"), ("sofa", "sofa", "a"), ("clock", "clock", "a"), ("cup", "cup", "a"), ("spoon", "spoon", "a")]
    wordlist(6, "home_objects", "Learn Everyday Objects in English | Toddler Vocabulary",
             "Things around my home! Mimzi and Teddy name everyday objects: chair, table, bed, door, window, lamp, sofa, clock, cup and spoon.",
             ["EverydayObjects", "ToddlerVocabulary", "LearnEnglishWords", "FirstWords", "ToddlerLearning", "Mimzi"], th("At Home!", "Everyday Words", "w:sofa"),
             "mz_kitchen", "Things Around My Home", "Let's find things around our home!", words, "Next time, let's practice hello, goodbye and thank you.")


def ep09():
    words = [("apple", "apple", "an"), ("banana", "banana", "a"), ("ball", "ball", "a"), ("book", "book", "a"), ("cup", "cup", "a"),
             ("car", "car", "a"), ("cat", "cat", "a"), ("dog", "dog", "a"), ("duck", "duck", "a"), ("fish", "fish", "a"),
             ("shoe", "shoe", "a"), ("hat", "hat", "a"), ("bed", "bed", "a"), ("chair", "chair", "a"), ("sun", "sun", "the"),
             ("moon", "moon", "the"), ("star", "star", "a"), ("tree", "tree", "a"), ("balloon", "balloon", "a"), ("clock", "clock", "a")]
    sc_words = words
    bg = "mz_playroom"
    sc = [intro(bg, "My First Picture Dictionary", [L(MW, "Hi friends! Let's open our picture dictionary."), L(T, "Twenty words! Ready?")], prop="i:book:0.3")]
    for i, (ic, wd, a) in enumerate(sc_words):
        sc.append(S(bg, trio(f"w:{ic}:{wd}"), [L(N, f"{wd.capitalize()}.", 0.4), L(M, f"{wd.capitalize()}.", 0.4), L(N, f"{a.capitalize()} {wd}.")], lead=0.3, tail=0.35))
        if i in (9,):
            sc.append(S(bg, duo(), [L(MW, "Ten words already! Wow!"), clap(T), L(T, "Ten more!")]))
    sc.append(outro(bg, "Next time, let's play a guessing game. What is this?", [L(MW, "We read our whole picture dictionary!")], prop="i:book:0.3"))
    ep(9, "picture_dictionary", "20 First English Words for Toddlers | Picture Vocabulary Book",
       "A gentle picture dictionary for toddlers: 20 first English words with clear pictures and repetition, read by Mimzi and Teddy.",
       ["PictureDictionary", "FirstWords", "ToddlerVocabulary", "LearnEnglish", "BabyLearning", "Mimzi"], th("20 Words!", "Picture Dictionary", "w:balloon"), sc)


# ------------------------------------------------------------------ 04 animal names and sounds
def animals(num, slug, title, desc, tags, thumb, bg, banner, hello, items, teaser, closing):
    sc = [intro(bg, banner, [L(MW, "Hi friends! I'm Mimzi, and this is Teddy!"), L(T, "Hello!"), L(MW, hello)])]
    for i, (ic, name, sound, fact) in enumerate(items):
        lines = [L(N, f"Look! It's {name}." if i % 3 != 1 else "Who is this?", 0.5 if i % 3 != 1 else 1.8)]
        if i % 3 == 1:
            lines.append(L(M, f"It's {name}!"))
        else:
            lines.append(L(M, f"{name.split()[-1].capitalize()}!"))
        if sound:
            lines += [L(N, f"What does the {name.split()[-1]} say?", 1.4), L(T, sound)]
        if fact:
            lines.append(L(N, fact))
        sc.append(S(bg, trio(f"w:{ic}:{name.split()[-1]}"), lines))
    sc.append(outro(bg, teaser, [L(MW, closing)]))
    ep(num, slug, title, desc, tags, thumb, sc)


def ep04():
    items = [("cat", "a cat", "Meow, meow!", None), ("dog", "a dog", "Woof, woof!", None), ("cow", "a cow", "Moo!", None), ("duck", "a duck", "Quack, quack!", None),
             ("sheep", "a sheep", "Baa, baa!", None), ("pig", "a pig", "Oink, oink!", None), ("horse", "a horse", "Neigh!", None), ("lion", "a lion", "Roar!", None),
             ("bee", "a bee", "Buzz, buzz!", None), ("chick", "a chick", "Cheep, cheep!", None)]
    animals(4, "animal_names_sounds", "Learn Animal Names and Sounds | First Animal Words for Toddlers",
            "Meet the animals with Mimzi and Teddy! Toddlers learn animal names and sounds: cat, dog, cow, duck, sheep, pig, horse, lion, bee and chick.",
            ["AnimalSounds", "AnimalNames", "FirstWords", "ToddlerLearning", "BabyAnimals", "Mimzi"], th("Animal Sounds!", "Moo! Woof! Quack!", "w:cow", "mz_garden"),
            "mz_garden", "Animal Names and Sounds", "Let's meet some animals and hear what they say!", items,
            "Next time, let's learn our body parts.", "Yay! We met so many animals!")


def ep17():
    items = [("cow", "a cow", "Moo!", "The cow gives us milk."), ("sheep", "a sheep", "Baa, baa!", "The sheep has soft, fluffy wool."),
             ("pig", "a pig", "Oink, oink!", "The pig loves to roll in the mud."), ("horse", "a horse", "Neigh!", "The horse can run very fast."),
             ("duck", "a duck", "Quack, quack!", "The duck swims in the pond."), ("hen", "a hen", "Cluck, cluck!", "The hen lays eggs."),
             ("chick", "a little chick", "Cheep, cheep!", None), ("dog", "a dog", "Woof, woof!", "The dog helps on the farm.")]
    animals(17, "farm_animals", "Farm Animals and Their Sounds for Toddlers",
            "Let's visit the farm! Mimzi and Teddy meet a cow, sheep, pig, horse, duck, hen, chick and dog, and hear every animal sound.",
            ["FarmAnimals", "AnimalSounds", "FarmAnimalsForKids", "ToddlerLearning", "Farm", "Mimzi"], th("On the Farm!", "Farm Animal Sounds", "w:cow", "mz_farm"),
            "mz_farm", "Farm Animals!", "Today we're visiting the farm!", items, "Next time, let's meet the wild animals.", "We met all the farm animals!")


def ep18():
    items = [("lion", "a lion", "Roar!", "The lion is the king of the jungle."), ("elephant", "an elephant", "Toot, toot!", "The elephant has a long trunk."),
             ("giraffe", "a giraffe", None, "The giraffe has a long, long neck."), ("zebra", "a zebra", None, "The zebra has black and white stripes."),
             ("monkey", "a monkey", "Ooh, ooh, ah, ah!", "The monkey loves bananas.")]
    animals(18, "wild_animals", "Wild Animals for Toddlers | Lion, Elephant, Giraffe and Zebra",
            "Mimzi and Teddy go on a safari to meet wild animals: lion, elephant, giraffe, zebra and monkey, with fun animal facts for toddlers.",
            ["WildAnimals", "SafariAnimals", "AnimalSounds", "ToddlerLearning", "ZooAnimals", "Mimzi"], th("Wild Animals!", "Safari Fun", "w:lion", "mz_savanna"),
            "mz_savanna", "Wild Animals!", "Let's go on a safari and meet the wild animals!", items, "Next time, let's dive under the sea.", "Wow! The wild animals are amazing!")


def ep19():
    items = [("fish", "a fish", None, "The fish swims with its little fins."), ("dolphin", "a dolphin", "Click, click, squeak!", "The dolphin loves to jump and play."),
             ("turtle", "a turtle", None, "The turtle has a hard shell."), ("whale", "a whale", None, "The whale is very, very big."),
             ("crab", "a crab", None, "The crab walks sideways. Pinch, pinch!"), ("octopus", "an octopus", None, "The octopus has eight arms!")]
    animals(19, "ocean_animals", "Ocean Animals for Toddlers | Fish, Dolphin, Turtle and Whale",
            "Splash! Mimzi and Teddy meet ocean animals: fish, dolphin, turtle, whale, crab and octopus, with easy facts for toddlers.",
            ["OceanAnimals", "SeaAnimals", "UnderTheSea", "ToddlerLearning", "Dolphin", "Mimzi"], th("Under the Sea!", "Ocean Animals", "w:dolphin", "mz_ocean"),
            "mz_ocean", "Ocean Animals!", "Let's dive under the sea! Splash!", items, "Next time, let's learn yummy fruits.", "Bye bye, ocean friends!")


# ------------------------------------------------------------------ 05 body parts
def ep05():
    bg = "mz_playroom"
    parts = [("eye", "eyes", "These are my eyes. I see with my eyes.", "Blink, blink!"), ("nose", "nose", "This is my nose. I smell with my nose.", "Sniff, sniff!"),
             ("mouth", "mouth", "This is my mouth. I eat and talk with my mouth.", "Yum, yum!"), ("ear", "ears", "These are my ears. I hear with my ears.", "Listen!"),
             ("hand", "hands", "These are my hands. I clap with my hands.", None), ("foot", "feet", "These are my feet. I walk and jump with my feet.", "Stomp, stomp!")]
    sc = [intro(bg, "My Body Parts!", [L(MW, "Hi friends! Let's learn about our bodies!"), L(T, "Point with me!")])]
    for ic, nm, line, act in parts:
        lines = [L(N, f"Point to your {nm}!", 1.6), L(M, line)]
        if nm == "hands":
            lines.append(clap(M))
        elif act:
            lines.append(L(T, act))
        sc.append(S(bg, trio(f"w:{ic}:{nm}"), lines))
    sc.append(S(bg, duo(), [L(N, "Now let's sing it!"), L(MW, "Eyes and nose, and mouth and ears. Hands and feet, hooray, hooray!"),
                            L(MW, "Eyes and nose, and mouth and ears. Wiggle, wiggle, shake away!", 0.6)]))
    for ic, nm in (("nose", "nose"), ("foot", "feet"), ("ear", "ears")):
        sc.append(S(bg, trio(f"w:{ic}:{nm}"), [L(N, "What is this?", 1.8), L(M, f"My {nm}!")], lead=0.3))
    sc.append(outro(bg, "Next time, let's find things around our home."))
    ep(5, "body_parts", "Body Parts Song for Toddlers | Eyes, Nose, Mouth and Ears",
       "Point and learn with Mimzi! Toddlers learn body parts: eyes, nose, mouth, ears, hands and feet, with a fun body chant.",
       ["BodyParts", "BodyPartsSong", "ToddlerSongs", "FirstWords", "ToddlerLearning", "Mimzi"], th("My Body!", "Eyes, Nose, Mouth", "w:nose:nose"), sc)


# ------------------------------------------------------------------ 07 greetings
def ep07():
    bg = "mz_playroom"
    items = [("Hello!", "wave", "We say hello when we see a friend.", [L(MW, "Hello, Teddy!"), L(T, "Hello, Mimzi!")]),
             ("Good morning!", "sun", "We say good morning when we wake up.", [L(M, "Good morning, sunshine!")]),
             ("Please", "gift", "We say please when we want something.", [L(T, "Can I have a cookie, please?")]),
             ("Thank you!", "heart", "We say thank you when someone helps us.", [L(T, "Thank you, Mimzi!"), L(M, "You're welcome, Teddy!")]),
             ("Sorry", "sad", "We say sorry when we make a mistake.", [L(M, "Oops! I'm sorry, Teddy."), L(T, "That's okay!")]),
             ("Goodbye!", "wave", "We say goodbye when a friend goes home.", [L(MW, "Goodbye, Teddy! See you soon!")]),
             ("Good night!", "moon", "We say good night at bedtime.", [L(M, "Good night, Teddy. Sweet dreams.")])]
    sc = [intro(bg, "Hello, Goodbye and Thank You!", [L(MW, "Hi friends! Let's learn kind words to say."), L(T, "Hello, everyone!")])]
    for word, ic, explain, skit in items:
        say = word.strip("!")
        sc.append(S(bg, trio(f"t:{word}:{ic}"), [L(N, explain, 0.5), L(N, f"Can you say {say.lower()}?", 1.6)] + skit))
    sc.append(S(bg, duo(), [L(N, "Let's say them all together!"), L(MW, "Hello! Good morning! Please! Thank you! Sorry! Goodbye! Good night!", 0.6)]))
    sc.append(outro(bg, "Next time, let's play find the missing letter."))
    ep(7, "hello_goodbye", "First English Words for Toddlers | Hello, Goodbye and Thank You",
       "Kind words for little ones: hello, good morning, please, thank you, sorry, goodbye and good night, with Mimzi and Teddy.",
       ["Greetings", "HelloSong", "PleaseAndThankYou", "GoodManners", "ToddlerLearning", "Mimzi"], th("Hello!", "Kind Words", "t:Hello!:wave"), sc)


# ------------------------------------------------------------------ 08 missing letter
def ep08():
    bg = "mz_playroom"
    rounds = [("A,B,_", "C"), ("D,E,_", "F"), ("_,H,I", "G"), ("J,_,L", "K"), ("M,N,_", "O"), ("_,Q,R", "P"), ("S,T,_", "U"), ("V,_,X", "W"), ("X,Y,_", "Z")]
    sc = [intro(bg, "Find the Missing Letter!", [L(MW, "Hi friends! Let's play a letter game!"), L(T, "One letter is hiding. Can you find it?")], prop="q")]
    for i, (seq, ans) in enumerate(rounds):
        said = ", ".join("what" if x == "_" else x for x in seq.split(","))
        sc.append(S(bg, trio("seq:" + seq, wide=True), [L(N, said + "?", 0.4), L(N, "Which letter is missing?", 2.6)]))
        sc.append(S(bg, trio("card_" + ans), [L(M, f"It's {ans}!"), L(T, f"{seq.replace('_', ans).replace(',', ', ')}!"), clap(M) if i % 3 == 2 else L(N, "Well done!")], lead=0.25))
    sc.append(outro(bg, "Next time, let's read my picture dictionary.", [L(MW, "You found every missing letter!")], prop="abc_strip"))
    ep(8, "missing_letter", "ABC Learning Game for Toddlers | Find the Missing Letter",
       "An easy ABC game for toddlers! Mimzi and Teddy show three letters with one missing. Little ones pause, think and say the missing letter.",
       ["ABCGame", "AlphabetGame", "LetterRecognition", "Preschool", "ToddlerLearning", "Mimzi"], th("Missing Letter?", "ABC Game", "q"), sc)


# ------------------------------------------------------------------ 10 what is this
def ep10():
    bg = "mz_playroom"
    rounds = [("cow", "a cow", "It says moo!"), ("banana", "a banana", "It is yellow and yummy."), ("car", "a car", "It goes beep, beep!"),
              ("fish", "a fish", "It swims in the water."), ("sun", "the sun", "It shines in the sky."), ("ball", "a ball", "You can bounce it and roll it."),
              ("duck", "a duck", "It says quack, quack!"), ("toothbrush", "a toothbrush", "We brush our teeth with it."), ("star", "a star", "It twinkles at night."),
              ("bed", "a bed", "We sleep in it at night.")]
    sc = [intro(bg, "What Is This? Guessing Game", [L(MW, "Hi friends! Let's play a guessing game!"), L(T, "Listen to the clue, then guess!")], prop="q")]
    for ic, nm, clue in rounds:
        sc.append(S(bg, trio("q"), [L(N, clue, 0.4), L(N, "What is this?", 2.4)]))
        sc.append(S(bg, trio(f"w:{ic}:{nm.split()[-1]}"), [L(M, f"It's {nm}!"), L(T, "You got it!")], lead=0.25))
    sc.append(outro(bg, "Next time, let's count from one to ten.", [L(MW, "You are a super guesser!")]))
    ep(10, "what_is_this", "Learn English Words for Toddlers | What Is This? Guessing Game",
       "A gentle guessing game for toddlers! Hear a clue, pause, guess, then see the answer: cow, banana, car, fish, sun and more.",
       ["GuessingGame", "WhatIsThis", "LearnEnglishWords", "ToddlerGames", "ToddlerLearning", "Mimzi"], th("What Is This?", "Guessing Game", "q"), sc)


# ------------------------------------------------------------------ 11 numbers 1-10, 12 counting 1-20
def ep11():
    bg = "mz_playroom"
    objs = [("ball", "ball"), ("block", "block"), ("duck", "duck"), ("star", "star"), ("apple", "apple"), ("car", "car"), ("balloon", "balloon"),
            ("heart", "heart"), ("fish", "fish"), ("teddy_i", "teddy")]
    sc = [intro(bg, "Numbers 1 to 10!", [L(MW, "Hi friends! Let's count our toys from one to ten!"), L(T, "Count with us!")], prop="nn:1")]
    for n, (ic, nm) in enumerate(objs, 1):
        pl = nm if n == 1 or nm == "fish" else (nm + "s" if nm != "teddy" else "teddies")
        count = ", ".join(NUMW[k].capitalize() for k in range(1, n + 1))
        lines = [L(N, f"Number {NUMW[n]}.", 0.5), L(M, f"{count}!", 0.3), L(N, f"{NUMW[n].capitalize()} {pl}!")]
        if n in (3, 6, 9):
            lines.append(clap(M))
        sc.append(S(bg, trio(f"n:{n}:{ic}"), lines))
    sc.append(S(bg, trio("nn:10"), [L(N, "Let's count to ten together!"), L(MW, "One, two, three, four, five, six, seven, eight, nine, ten!", 0.6)]))
    sc.append(outro(bg, "Next time, let's count to twenty with cute animals."))
    ep(11, "numbers_1_10", "Learn Numbers 1–10 for Toddlers | Count with Mimzi",
       "Count from one to ten with Mimzi and Teddy! Toddlers count colourful toys: balls, blocks, ducks, stars and more.",
       ["Numbers", "Counting", "Count1To10", "NumberSong", "ToddlerLearning", "Mimzi"], th("Count to 10!", "Numbers 1–10", "n:3:duck"), sc)


def ep12():
    bg = "mz_garden"
    ani = ["chick", "ladybug", "fish", "bee", "butterfly", "duck", "rabbit", "turtle", "sheep", "chick"]
    names = {"chick": "chicks", "ladybug": "ladybugs", "fish": "fish", "bee": "bees", "butterfly": "butterflies", "duck": "ducks", "rabbit": "bunnies", "turtle": "turtles", "sheep": "sheep"}
    sc = [intro(bg, "Counting 1 to 20!", [L(MW, "Hi friends! Let's count cute animals, all the way to twenty!"), L(T, "Wow, that's a lot!")], prop="nn:20")]
    for n in range(1, 21):
        a = ani[(n - 1) % 10]
        nm = names[a] if n > 1 else a.replace("butterfly", "butterfly")
        if n <= 5:
            lines = [L(N, f"{NUMW[n].capitalize()}.", 0.3), L(M, ", ".join(NUMW[k] for k in range(1, n + 1)).capitalize() + "!", 0.3), L(N, f"{NUMW[n].capitalize()} {nm}!")]
        else:
            lines = [L(N, f"{NUMW[n].capitalize()}!", 0.4), L(M, f"{NUMW[n].capitalize()} {nm}!")]
        if n in (10, 20):
            lines.append(clap(M))
        sc.append(S(bg, trio(f"n:{n}:{a}"), lines, lead=0.3, tail=0.35))
    sc.append(S(bg, trio("nn:20"), [L(N, "Now let's count to twenty together!"),
                                    L(MW, "One, two, three, four, five, six, seven, eight, nine, ten. Eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty!", 0.6)]))
    sc.append(outro(bg, "Next time, let's learn colors."))
    ep(12, "counting_1_20", "Counting 1–20 with Cute Animals | Numbers for Toddlers",
       "Count from one to twenty with Mimzi, Teddy and cute animals: chicks, ladybugs, fish, bees, butterflies and more.",
       ["Counting", "Count1To20", "Numbers", "NumberSong", "ToddlerLearning", "Mimzi"], th("Count to 20!", "Cute Animal Counting", "n:5:ladybug", "mz_garden"), sc)


# ------------------------------------------------------------------ 13 colors
def ep13():
    bg = "mz_playroom"
    cols = [("red", "apple", "a red apple"), ("blue", "ball", "a blue ball"), ("yellow", "sun", "the yellow sun"), ("green", "leaf", "a green leaf"),
            ("orange", "orange", "an orange orange"), ("purple", "grapes", "purple grapes"), ("pink", "pig", "a pink pig"), ("brown", "teddy_i", "a brown teddy")]
    sc = [intro(bg, "Learn Colors with Mimzi!", [L(MW, "Hi friends! Let's learn colors!"), L(T, "Colors are everywhere!")], prop="s:heart")]
    for cn, ic, phrase in cols:
        sc.append(S(bg, trio(f"c:{cn}:{ic}"), [L(N, f"This is {cn}.", 0.5), L(M, f"{cn.capitalize()}! Look, {phrase}!"), L(T, f"{cn.capitalize()}!")]))
    for ic, wd, cn in (("banana", "banana", "yellow"), ("strawberry", "strawberry", "red"), ("broccoli", "broccoli", "green"), ("whale", "whale", "blue")):
        sc.append(S(bg, trio(f"w:{ic}:{wd}"), [L(N, f"What color is the {wd}?", 2.2), L(M, f"{cn.capitalize()}! The {wd} is {cn}!")]))
    sc.append(outro(bg, "Next time, let's sing about shapes.", [L(MW, "Red, blue, yellow, green, orange, purple, pink and brown! We know so many colors!")]))
    ep(13, "colors", "Learn Colors with Mimzi | Colors for Toddlers",
       "Learn colors with Mimzi and Teddy: red, blue, yellow, green, orange, purple, pink and brown, with a fun color quiz.",
       ["LearnColors", "ColorsForKids", "ColorsSong", "ColorRecognition", "ToddlerLearning", "Mimzi"], th("Colors!", "Learn Colors", "c:red:apple"), sc)


# ------------------------------------------------------------------ 14 shapes
def ep14():
    bg = "mz_playroom"
    shapes = [("circle", "A circle is round, like a ball."), ("square", "A square has four sides, all the same."), ("triangle", "A triangle has three sides."),
              ("star", "A star twinkles in the sky."), ("heart", "A heart means love."), ("rectangle", "A rectangle looks like a door."),
              ("oval", "An oval looks like an egg."), ("diamond", "A diamond looks like a kite.")]
    sc = [intro(bg, "Shapes Song!", [L(MW, "Hi friends! Let's sing and learn shapes!"), L(T, "Shapes, shapes, shapes!")], prop="s:star")]
    for i, (s, fact) in enumerate(shapes):
        art_ = "an" if s[0] in "aeiou" else "a"
        sc.append(S(bg, trio(f"s:{s}"), [L(N, f"This is {art_} {s}.", 0.4), L(M, f"{s.capitalize()}, {s}, I see {art_} {s}!"), L(N, fact)]))
        if i == 3:
            sc.append(S(bg, duo(), [L(MW, "Circle, square, triangle, star. Shapes are fun, wherever you are!"), clap(T)]))
    for a, b, ans in (("circle", "square", "circle"), ("triangle", "star", "star"), ("heart", "oval", "heart")):
        sc.append(S(bg, trio(f"o:{a}:{b}:shape_{a}:shape_{b}", wide=True), [L(N, f"Where is the {ans}?", 2.2), L(M, f"There it is! The {ans}!")]))
    sc.append(outro(bg, "Next time, let's learn big and small.", [L(MW, "Circle, square, triangle, star, heart, rectangle, oval and diamond!")]))
    ep(14, "shapes_song", "Shapes Song for Toddlers | Circle, Square, Triangle and Star",
       "Sing and learn shapes with Mimzi! Circle, square, triangle, star, heart, rectangle, oval and diamond, plus a find-the-shape game.",
       ["ShapesSong", "LearnShapes", "ShapesForKids", "Preschool", "ToddlerLearning", "Mimzi"], th("Shapes!", "Shapes Song", "s:triangle"), sc)


# ------------------------------------------------------------------ 15 big and small, 16 opposites
def ep15():
    bg = "mz_playroom"
    pairs = [("ball", "ball"), ("teddy_i", "teddy"), ("apple", "apple"), ("car", "car"), ("balloon", "balloon"), ("star", "star")]
    sc = [intro(bg, "Big and Small!", [L(MW, "Hi friends! Let's learn big and small!"), L(T, "I am small. Mimzi is big!")])]
    for i, (ic, nm) in enumerate(pairs):
        lines = [L(N, f"This {nm} is big.", 0.4), L(N, f"This {nm} is small.", 0.5), L(M, f"Big {nm}, small {nm}!")]
        if i % 2 == 1:
            lines = [L(N, f"Which {nm} is big?", 2.0), L(M, f"This one! The big {nm}!"), L(T, f"And this is the small {nm}.")]
        sc.append(S(bg, trio(f"o:big:small:{ic}:{ic}:size", wide=True), lines))
    sc.append(S(bg, trio("o:big:small:elephant:ladybug", wide=True), [L(N, "An elephant is big. A ladybug is small.", 0.5), L(M, "Big elephant, tiny ladybug!"), L(T, "Stomp, stomp! Buzz, buzz!")]))
    sc.append(S(bg, duo(), [L(N, "Make yourself big!", 1.4), L(MW, "Big, big, big! Stretch up high!", 0.6), L(N, "Now make yourself small!", 1.4), L(T, "Small, small, small! Curl up tiny!", 0.6)]))
    sc.append(outro(bg, "Next time, let's learn opposites."))
    ep(15, "big_small", "Big and Small for Toddlers | Learn Sizes with Mimzi",
       "Big or small? Mimzi and Teddy compare toys and animals so toddlers learn sizes, with a fun stretch-big, curl-small game.",
       ["BigAndSmall", "Sizes", "Opposites", "Preschool", "ToddlerLearning", "Mimzi"], th("Big or Small?", "Learn Sizes", "o:big:small:ball:ball:size"), sc)


def ep16():
    bg = "mz_playroom"
    ops = [("up", "down", "balloon", "ball", "The balloon goes up, up, up!", "The ball falls down, down, down!"),
           ("hot", "cold", "cocoa", "snowman", "The cocoa is hot.", "The snowman is cold. Brrr!"),
           ("happy", "sad", "happy", "sad", "This face is happy.", "This face is sad."),
           ("open", "closed", "box_open", "box_closed", "The box is open.", "The box is closed."),
           ("full", "empty", "cup_full", "cup_empty", "The cup is full.", "The cup is empty."),
           ("day", "night", "sun", "moon", "In the day, the sun shines.", "At night, the moon glows."),
           ("fast", "slow", "car", "snail", "The car is fast. Zoom!", "The snail is slow.")]
    sc = [intro(bg, "Learn Opposites!", [L(MW, "Hi friends! Let's learn opposites!"), L(T, "Up and down! Hot and cold!")])]
    for a, b, ia, ib, la, lb in ops:
        sc.append(S(bg, trio(f"o:{a}:{b}:{ia}:{ib}", wide=True), [L(N, la, 0.4), L(N, lb, 0.4), L(M, f"{a.capitalize()} and {b}! They are opposites!")]))
    for a, b, ia, ib in (("hot", "cold", "cocoa", "snowman"), ("fast", "slow", "car", "snail")):
        sc.append(S(bg, trio(f"o:{a}:{b}:{ia}:{ib}", wide=True), [L(N, f"What is the opposite of {a}?", 2.2), L(M, f"{b.capitalize()}!")]))
    sc.append(outro(bg, "Next time, let's visit the farm animals."))
    ep(16, "opposites", "Learn Opposites for Toddlers | Up and Down, Hot and Cold, Happy and Sad",
       "Mimzi and Teddy learn opposites: up and down, hot and cold, happy and sad, open and closed, full and empty, day and night, fast and slow.",
       ["Opposites", "OppositesForKids", "Preschool", "EarlyLearning", "ToddlerLearning", "Mimzi"], th("Opposites!", "Up & Down, Hot & Cold", "o:hot:cold:cocoa:snowman"), sc)


# ------------------------------------------------------------------ 20 fruits, 21 vegetables
def food(num, slug, title, desc, tags, thumb, banner, hello, items, teaser, closing):
    bg = "mz_kitchen"
    sc = [intro(bg, banner, [L(MW, "Hi friends! I'm Mimzi, and this is Teddy!"), L(T, "I'm hungry!"), L(MW, hello)])]
    for i, (ic, nm, fact) in enumerate(items):
        if i % 3 == 2:
            lines = [L(N, "What is this?", 1.8), L(M, f"{nm.capitalize()}!"), L(N, fact), L(T, "Yum, yum!")]
        else:
            lines = [L(N, f"This is {('an' if nm[0] in 'aeiou' else 'a')} {nm}." if nm not in ("grapes", "peas") else f"These are {nm}.", 0.4), L(M, f"{nm.capitalize()}! Can you say {nm}?", 1.4), L(N, fact)]
        sc.append(S(bg, trio(f"w:{ic}:{nm}"), lines))
    sc.append(outro(bg, teaser, [L(MW, closing)]))
    ep(num, slug, title, desc, tags, thumb, sc)


def ep20():
    items = [("apple", "apple", "It is red, round and crunchy."), ("banana", "banana", "It is yellow. Peel it first!"), ("orange", "orange", "It is orange and juicy."),
             ("strawberry", "strawberry", "It is red and sweet."), ("grapes", "grapes", "They are small and purple."), ("watermelon", "watermelon", "It is green outside and red inside."),
             ("pear", "pear", "It is green and sweet.")]
    food(20, "fruits", "Learn Fruits for Toddlers | Apple, Banana, Orange and Strawberry",
         "Yummy fruits with Mimzi and Teddy: apple, banana, orange, strawberry, grapes, watermelon and pear, with colors and easy facts.",
         ["Fruits", "LearnFruits", "FruitNames", "HealthyEating", "ToddlerLearning", "Mimzi"], th("Yummy Fruits!", "Learn Fruits", "w:strawberry", "mz_kitchen"),
         "Yummy Fruits!", "Let's learn yummy fruits!", items, "Next time, let's learn vegetables.", "Fruits are yummy and healthy!")


def ep21():
    items = [("carrot", "carrot", "It is orange and crunchy."), ("potato", "potato", "It is brown and grows in the ground."), ("tomato", "tomato", "It is red and round."),
             ("broccoli", "broccoli", "It looks like a little tree!"), ("corn", "corn", "It is yellow and sweet."), ("peas", "peas", "They are small, round and green.")]
    food(21, "vegetables", "Learn Vegetables for Toddlers | Carrot, Potato, Tomato and Broccoli",
         "Healthy vegetables with Mimzi and Teddy: carrot, potato, tomato, broccoli, corn and peas, with colors and simple facts.",
         ["Vegetables", "LearnVegetables", "HealthyEating", "FirstWords", "ToddlerLearning", "Mimzi"], th("Veggies!", "Learn Vegetables", "w:carrot", "mz_kitchen"),
         "Healthy Vegetables!", "Let's learn healthy vegetables!", items, "Next time, let's sing a good morning song.", "Vegetables make us big and strong!")


# ------------------------------------------------------------------ songs 22-26 (spoken, rhythmic chants)
def song(num, slug, title, desc, tags, thumb, bg, banner, hello, verses, chorus, teaser, **kw):
    sc = [intro(bg, banner, [L(MW, hello), L(T, "Sing along with us!")])]
    for rnd in range(2):
        if rnd == 1:
            sc.append(S(bg, duo(), [L(MW, "That was fun! Let's sing it one more time, all together!"), clap(T), L(T, "Ready? Here we go!")]))
        for i, (prop, lines) in enumerate(verses):
            sc.append(S(bg, trio(prop) if prop else duo(), [L(M if prop else MW, ln, 0.4) for ln in lines], **kw.get("scene_kw", {})))
            if chorus and i % 2 == 1:
                sc.append(S(bg, duo(), [L(MW, c, 0.4) for c in chorus], **kw.get("scene_kw", {})))
    sc.append(outro(bg, teaser))
    ep(num, slug, title, desc, tags, thumb, sc, review=None, **{k: v for k, v in kw.items() if k != "scene_kw"})


def ep22():
    verses = [("w:sun", ["Good morning, sun, shining bright!", "Good morning, sky, so blue and light!"]),
              ("w:wave:hello", ["Good morning, Teddy, wave hi, hi, hi!", "Good morning, friends, reach up high!"]),
              ("w:water", ["Splash, splash, wash my face.", "Fresh and clean, a happy face!"]),
              ("w:toothbrush", ["Brush, brush, brush my teeth.", "Top and bottom, nice and neat!"]),
              ("w:banana:breakfast", ["Yum, yum, breakfast time.", "Banana, toast, and milk is fine!"]),
              ("w:toybox:play", ["Now we're ready, one, two, three.", "A happy day for you and me!"])]
    chorus = ["Good morning, good morning, it's a brand new day!", "Good morning, good morning, let's go out and play!"]
    song(22, "good_morning_song", "Good Morning Song for Toddlers | Start Your Day with Mimzi",
         "Start the day with Mimzi and Teddy! A cheerful good morning song: say hello to the sun, wash your face, brush your teeth, eat breakfast and play.",
         ["GoodMorningSong", "MorningRoutine", "ToddlerSongs", "KidsSongs", "NurseryRhymes", "Mimzi"], th("Good Morning!", "Morning Song", "w:sun", "mz_bedroom"),
         "mz_bedroom", "Good Morning Song!", "Good morning, friends! Time to wake up!", verses, chorus, "Next time, let's sing the clean up song.")


def ep23():
    verses = [("i:ball:0.25", ["Here's my ball, it's on the floor.", "Into the box, and then one more!"]), ("i:block:0.22", ["Blocks, blocks, stack them high.", "Into the box, wave them bye-bye!"]),
              ("i:teddy_i:0.25", ["Little teddy, time to rest.", "Into the box, you're the best!"]), ("i:car:0.22", ["Zoom, zoom, my little car.", "Into the box, you're a star!"]),
              ("i:book:0.25", ["Books go back up on the shelf.", "I can do it by myself!"]), ("i:toybox:0.3", ["Look how tidy, look how neat!", "Clean up time is now complete!"])]
    chorus = ["Clean up, clean up, everybody clean up!", "Clean up, clean up, put your toys away!"]
    song(23, "clean_up_song", "Clean Up Song for Toddlers | Let's Put Our Toys Away",
         "Tidy time with Mimzi and Teddy! A clean up song that helps toddlers put away balls, blocks, teddies, cars and books.",
         ["CleanUpSong", "TidyUp", "ToddlerSongs", "GoodHabits", "KidsSongs", "Mimzi"], th("Clean Up!", "Tidy-Up Song", "w:toybox:toys"),
         "mz_playroom", "Clean Up Song!", "Uh oh, our toys are everywhere! Let's clean up!", verses, chorus, "Next time, let's do the animal dance!")


def ep24():
    verses = [("w:rabbit:hop", ["Hop like a bunny, hop, hop, hop!", "Hop like a bunny, now we stop!"]), ("w:duck:waddle", ["Waddle like a duck, quack, quack, quack!", "Waddle forward, waddle back!"]),
              ("w:elephant:stomp", ["Stomp like an elephant, big and slow!", "Stomp, stomp, stomp, here we go!"]), ("w:fish:swim", ["Swim like a fish, swish, swish, swish!", "Wiggle your arms like a little fish!"]),
              ("w:butterfly:flap", ["Flap like a butterfly, fly up high!", "Flutter, flutter, in the sky!"]), ("w:lion:roar", ["Roar like a lion, loud and proud!", "Roar, roar, roar, nice and loud!"])]
    chorus = ["Dance, dance, the animal dance!", "Move your body, take a chance!"]
    song(24, "animal_dance", "Animal Dance Song for Toddlers | Move and Learn",
         "Get moving with Mimzi! Hop like a bunny, waddle like a duck, stomp like an elephant, swim like a fish, flap like a butterfly and roar like a lion.",
         ["AnimalDance", "MovementSong", "DanceSong", "ToddlerSongs", "KidsSongs", "Mimzi"], th("Animal Dance!", "Move & Learn", "w:rabbit:hop", "mz_garden"),
         "mz_garden", "Animal Dance Song!", "Stand up, friends! Let's dance like animals!", verses, chorus, "Next time, let's sing the brush your teeth song.")


def ep25():
    verses = [("w:toothbrush", ["Here's my toothbrush, here's my paste.", "A tiny bit, not too much waste!"]), ("w:toothpaste", ["Squeeze a dot, as small as a pea.", "Ready to brush, one, two, three!"]),
              ("w:mouth:teeth", ["Brush the top teeth, up and down.", "Brush the bottom, round and round!"]), ("w:happy:smile", ["Brush the front and brush the back.", "Shiny teeth, that's a fact!"]),
              ("w:water:rinse", ["Spit it out and rinse away.", "Clean teeth for a happy day!"]), ("w:happy:smile", ["Now give me a great big smile!", "Brush two times a day, every day!"])]
    chorus = ["Brush, brush, brush your teeth!", "Brush, brush, sparkly clean!"]
    song(25, "brush_teeth_song", "Brush Your Teeth Song for Toddlers | Healthy Habits",
         "Brush, brush, brush! Mimzi and Teddy sing a fun tooth-brushing song: a pea-size dot of toothpaste, up and down, round and round, spit and smile.",
         ["BrushYourTeeth", "ToothBrushingSong", "HealthyHabits", "ToddlerSongs", "KidsSongs", "Mimzi"], th("Brush Teeth!", "Healthy Habits Song", "w:toothbrush", "mz_bathroom"),
         "mz_bathroom", "Brush Your Teeth Song!", "It's time to brush our teeth!", verses, chorus, "Next time, a sweet bedtime lullaby.")


def ep26():
    bg = "mz_bedroom_night"
    verses = [("i:moon:0.3", ["The moon is up, the sky is deep.", "It's time for little ones to sleep."]), ("i:star:0.28", ["Little stars, they twinkle bright.", "They softly whisper, sleep tight."]),
              (None, ["Close your eyes, my little one.", "Our busy, happy day is done."]), ("i:teddy_i:0.3", ["Teddy's here, so warm and near.", "Hush now, darling, have no fear."]),
              ("i:heart:0.28", ["You are loved, so very much.", "Mommy's kiss and Daddy's touch."]), (None, ["Sweet dreams, sweet dreams, sleep so deep.", "Good night, good night, now go to sleep."])]
    chorus = ["Lullaby, lullaby, soft and slow.", "Lullaby, lullaby, off to dreamland we go."]
    sc = [S(bg, [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}], [L(M, "Shh, it's bedtime, friends."), L(T, "Let's sing a sleepy song.", 0.8)], banner="Bedtime Lullaby", lead=0.4)]
    for rnd in range(2):
        if rnd == 1:
            sc.append(S(bg, [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}], [L(M, "One more time, softly, softly.", 1.0)], lead=0.6, tail=0.8))
        for i, (prop, lines) in enumerate(verses):
            cast = [{"id": M, "x": 0.22}, {"id": prop, "x": 0.52, "y": 0.62, "pop": True}, {"id": T, "x": 0.82}] if prop else [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}]
            sc.append(S(bg, cast, [L(N, ln, 0.8) for ln in lines], lead=0.7, tail=0.9))
            if i % 2 == 1:
                sc.append(S(bg, [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}], [L(N, c, 0.8) for c in chorus], lead=0.7, tail=0.9))
    sc.append(S(bg, [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}], [L(N, SHARE, 0.8), L(M, "Good night, friends. Sweet dreams.", 2.0)], fade=True, tail=1.5))
    ep(26, "bedtime_lullaby", "Bedtime Lullaby for Toddlers | Sweet Dreams Little One",
       "A calm, gentle bedtime lullaby with Mimzi and Teddy. Soft music box tune and quiet words to help little ones wind down for sleep.",
       ["Lullaby", "BedtimeSong", "SleepMusic", "BabySleep", "ToddlerSongs", "Mimzi"], th("Sweet Dreams!", "Bedtime Lullaby", "w:moon", "mz_bedroom_night"), sc,
       music="lullaby", speed=0.9, review=None)


# ------------------------------------------------------------------ stories 27-30
def ep27():
    bg = "mz_playroom"
    sc = [S(bg, [{"id": MW, "x": 0.25}, {"id": "i:ball:0.2", "x": 0.5}, {"id": T, "x": 0.8}], [L(N, "Mimzi has a new red ball."), L(MW, "Look at my bouncy ball! Boing, boing!")], banner="Mimzi Learns to Share"),
          S(bg, [{"id": M, "x": 0.25}, {"id": "i:ball:0.2", "x": 0.4}, {"id": T, "x": 0.8}], [L(T, "Can I play with the ball too, Mimzi?"), L(M, "No! It's mine!"), L(N, "Oh no. Teddy feels sad.", 1.0)]),
          S(bg, [{"id": M, "x": 0.25}, {"id": "i:sad:0.22", "x": 0.55, "pop": True}, {"id": T, "x": 0.8}], [L(T, "I just want to play.", 0.8), L(N, "How do you think Teddy feels?", 2.0), L(N, "Teddy feels sad.")]),
          S(bg, [{"id": M, "x": 0.25}, {"id": "i:heart:0.2", "x": 0.55, "pop": True}, {"id": T, "x": 0.8}], [L(N, "Mimzi thinks for a moment.", 0.8), L(M, "Hmm. Playing alone is not much fun."), L(M, "Teddy, do you want to play with me?")]),
          S(bg, [{"id": MW, "x": 0.25}, {"id": "i:ball:0.2", "x": 0.55}, {"id": T, "x": 0.8}], [L(T, "Yes, please! Thank you, Mimzi!"), L(N, "Mimzi rolls the ball to Teddy. Roll, roll!"), L(T, "And I roll it back to you!")]),
          S(bg, [{"id": MW, "x": 0.25}, {"id": "i:happy:0.22", "x": 0.55, "pop": True}, {"id": T, "x": 0.8}], [L(M, "Taking turns is so much fun!"), L(N, "Now Mimzi and Teddy are both happy."), clap(M)]),
          S(bg, [{"id": MW, "x": 0.25}, {"id": "t:Sharing is caring!:heart", "x": 0.55, "pop": True}, {"id": T, "x": 0.82}],
            [L(N, "When we share, our friends feel happy, and we do too."), L(M, "Sharing is caring!"), L(T, "Sharing is caring!")]),
          outro(bg, "Next time, watch me brush my teeth.")]
    ep(27, "sharing_story", "Sharing Is Caring | A Short Educational Story for Toddlers",
       "Mimzi has a new ball, but Teddy wants to play too. A gentle story about feelings, taking turns and sharing with friends.",
       ["SharingIsCaring", "KidsStories", "Kindness", "BedtimeStory", "ToddlerLearning", "Mimzi"], th("Let's Share!", "Kindness Story", "i:heart"), sc, review="story",
       extra_q=[("What did Mimzi have?", "A red ball!", "w:ball"), ("How did Teddy feel when Mimzi said no?", "Sad.", "w:sad"),
                ("What did Mimzi do?", "She shared her ball with Teddy!", "w:ball:sharing"), ("How did they feel after sharing?", "Happy!", "w:happy")])


def ep28():
    sc = [S("mz_bedroom", [{"id": MW, "x": 0.3}, {"id": T, "x": 0.6}], [L(N, "Good morning! Mimzi wakes up and stretches."), L(MW, "Good morning, Teddy! Yawn!"), L(T, "Good morning! Time to brush your teeth!")], banner="Mimzi Brushes Her Teeth"),
          S("mz_bathroom", trio("w:toothbrush"), [L(N, "Mimzi goes to the bathroom and gets her toothbrush."), L(M, "Here's my blue toothbrush!")]),
          S("mz_bathroom", trio("w:toothpaste"), [L(N, "She squeezes a tiny dot of toothpaste. As small as a pea."), L(M, "Just a little bit!")]),
          S("mz_bathroom", trio("w:mouth:teeth"), [L(N, "Brush, brush, brush. Up and down on the top teeth.", 0.3), {"who": M, "sfx": "brush", "text": "", "dur": 2.0, "pause": 0.3},
                                                   L(N, "Brush, brush, brush. Round and round on the bottom teeth.", 0.3), {"who": M, "sfx": "brush", "text": "", "dur": 2.0, "pause": 0.3}]),
          S("mz_bathroom", trio("w:happy:smile"), [L(N, "Don't forget the back teeth, and the front teeth too!"), L(T, "Let's count while we brush. One, two, three, four, five!")]),
          S("mz_bathroom", trio("w:water:rinse"), [L(N, "Spit, then rinse with a little water."), L(M, "Spit, splash, all clean!")]),
          S("mz_bathroom", trio("w:happy:smile"), [L(M, "Look at my shiny teeth!"), L(T, "Wow! Sparkly clean!"), L(N, "We brush our teeth in the morning, and at night before bed.")]),
          outro("mz_bathroom", "Next time, let's wash our hands together.")]
    ep(28, "brushing_story", "Brushing Teeth for Toddlers | Fun Daily Routine Story",
       "Mimzi wakes up and brushes her teeth: toothbrush, a pea-size dot of toothpaste, up and down, round and round, spit, rinse and smile.",
       ["BrushingTeeth", "MorningRoutine", "HealthyHabits", "KidsStories", "ToddlerLearning", "Mimzi"], th("Brush Teeth!", "Daily Routine Story", "w:toothbrush", "mz_bathroom"), sc, review="story",
       extra_q=[("When do we brush our teeth?", "In the morning, and at night before bed!", None)])


def ep29():
    bg = "mz_bathroom"
    steps = [("w:water", "First, turn on the water and wet your hands.", "Splash, splash!"), ("w:soap", "Then add some soap.", "Bubbly soap!"),
             ("w:hand:rub", "Rub your hands together. Rub, rub, rub!", "Rub the fronts and backs!"), ("w:bubbles", "Wash between your fingers, and make lots of bubbles.", "So many bubbles!"),
             ("w:water:rinse", "Rinse the bubbles away.", "Bye bye, bubbles!"), ("w:towel", "Dry your hands with a towel.", "Pat, pat, all dry!")]
    chorus = ["Wash, wash, wash your hands!", "Scrub away the germs!"]
    sc = [intro(bg, "Wash Your Hands with Mimzi!", [L(MW, "Hi friends! Let's wash our hands!"), L(T, "Clean hands keep us healthy!")])]
    for i, (card, n_, m_) in enumerate(steps):
        sc.append(S(bg, trio(card), [L(N, n_, 0.4), L(M, m_)]))
        if i in (1, 3):
            sc.append(S(bg, duo(), [L(MW, c, 0.3) for c in chorus]))
    sc.append(S(bg, trio("w:sandwich:eating") if False else trio("w:apple:before eating"), [L(N, "When do we wash our hands?", 0.4), L(M, "Before we eat!")]))
    sc.append(S(bg, trio("w:soap:after the potty"), [L(M, "After we use the potty!"), L(T, "And after we play outside!")]))
    sc.append(outro(bg, "Next time, it's my bedtime routine.", [L(MW, "Look, my hands are squeaky clean!")]))
    ep(29, "hand_washing", "Hand Washing Song for Toddlers | Learn Good Hygiene Habits",
       "Wash your hands with Mimzi! Water, soap, rub, scrub between fingers, rinse and dry. Plus when to wash: before eating and after the potty.",
       ["HandWashing", "WashYourHands", "HealthyHabits", "Hygiene", "ToddlerSongs", "Mimzi"], th("Wash Hands!", "Healthy Habits", "w:soap", "mz_bathroom"), sc)


def ep30():
    sc = [S("mz_bedroom", [{"id": MW, "x": 0.3}, {"id": T, "x": 0.65}], [L(N, "The sun is going down. It's almost bedtime for Mimzi."), L(MW, "Teddy, is it bedtime already?"), L(T, "Yes! Let's get ready!")], banner="Mimzi's Bedtime Routine"),
          S("mz_bedroom", trio("w:toybox:toys away"), [L(N, "First, Mimzi puts her toys away."), L(M, "Good night, toys!")]),
          S("mz_bedroom", trio("w:pajamas"), [L(N, "Next, she puts on her cozy pajamas."), L(M, "My pajamas have little stars!")]),
          S("mz_bathroom", trio("w:toothbrush"), [L(N, "Then she brushes her teeth. Brush, brush, brush!"), {"who": M, "sfx": "brush", "text": "", "dur": 1.8, "pause": 0.3}]),
          S("mz_bedroom_night", trio("w:book:story time"), [L(N, "Now it's story time. Mimzi picks her favorite book."), L(T, "Read it again, please!")]),
          S("mz_bedroom_night", trio("w:heart:hugs"), [L(N, "A big hug and a kiss good night."), L(M, "I love you, Teddy."), L(T, "I love you too, Mimzi.")]),
          S("mz_bedroom_night", trio("w:moon:lights off"), [L(N, "Lights off. The moon is shining. The stars are twinkling."), L(M, "Good night, moon. Good night, stars.", 0.8)]),
          S("mz_bedroom_night", [{"id": M, "x": 0.3}, {"id": T, "x": 0.7}], [L(N, "Toys away, pajamas on, brush teeth, story, hugs, and sleep."), L(N, SHARE, 0.6),
                                                                            L(M, "Good night, friends. See you tomorrow!", 1.5)], fade=True, tail=1.2)]
    ep(30, "bedtime_routine", "Bedtime Routine for Toddlers | A Sweet Good Night Story",
       "Mimzi gets ready for bed: toys away, pajamas on, brush teeth, a bedtime story, hugs and lights off. A calm routine story for toddlers.",
       ["BedtimeRoutine", "BedtimeStory", "GoodNight", "KidsStories", "ToddlerLearning", "Mimzi"], th("Good Night!", "Bedtime Story", "w:moon", "mz_bedroom_night"), sc,
       speed=0.95, review="story", extra_q=[("What do we put on at bedtime?", "Our cozy pajamas!", "w:pajamas")])


for f in (ep02, ep03, ep04, ep05, ep06, ep07, ep08, ep09, ep10, ep11, ep12, ep13, ep14, ep15, ep16, ep17, ep18, ep19, ep20, ep21, ep22, ep23, ep24, ep25, ep26, ep27, ep28, ep29, ep30):
    f()

# schedule: one per day from Sun 22 Nov 2026; weekends 13:00 UTC, weekdays 14:00 UTC
day0 = datetime.date(2026, 11, 22)
EPS.sort(key=lambda e: e["num"])
for i, e in enumerate(EPS):
    d = day0 + datetime.timedelta(days=i)
    hr = 13 if d.weekday() >= 5 else 14
    e["schedule"] = f"{d.isoformat()}T{hr:02d}:00:00Z"
    e["file"] = f"mz{e['num']:03d}_{e['slug']}"
    out = {k: e[k] for k in ("title", "scenes", "thumbnail")}
    for k in ("music", "speed"):
        if k in e:
            out[k] = e[k]
    json.dump(out, open(f"episodes/{e['file']}.json", "w"), indent=1, ensure_ascii=False)
meta = [{k: e[k] for k in ("num", "file", "title", "desc", "tags", "schedule")} for e in EPS]
json.dump(meta, open("episodes/schedule.json", "w"), indent=1, ensure_ascii=False)
print(len(EPS), "episodes;", EPS[0]["schedule"], "->", EPS[-1]["schedule"])
