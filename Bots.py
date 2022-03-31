import random


def batman(a, b=None):
    alternatives = ["relax", "play cards", "fight joker.", 'try to catch joker']
    b = random.choice(alternatives)
    res = f"Nahh, {a}ing is an bad option. Or we could {b}."
    return res


def superman(a, b=None):
    if b is None:
        return "im not into {}. can we fly instead... ops forgot batman cant?".format(a + "ing")
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing")


def joker(a, b=None):
    alternatives = ["play chess", "fight Batman..", 'some killing']
    b = random.choice(alternatives)
    res = f"Nahh, {a}ing is an good option. Or maybe we could {b};)."
    return res


def spiderman(a, b=None):
    action = a + "ing"
    bad_things = ["fighting", "sleeping", "killing"]
    good_things = ["singing", "playing", "working", "eating", "sleeping", "playing"]

    if action in bad_things:
        return "yeaahhh!im down for {}, but can we invite Tony Stark?".format(action)
    elif action in good_things:
        return "What the hell? {} seems lame. Not doing that.".format(action)
    return "that seems lame, what about joining the avengers!!?"


suggestions = ["lets go outside and play", "Let's take a walk to Iron man",
               "Let's sleep a little bit!", "I feel like fighting right now", " We can do some eating"]

actions = ["work", "play", "eat", "cry", "sleep",  # List of known actions
           "fight", "sing", "hug", "bicker", "sleep",
           "complain", "walk"]
