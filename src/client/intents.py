from discord import Intents


def load_intents() -> Intents:
    # ---- Build intents ----
    intents = Intents(messages=True)
    return intents
