def goes_to_twenty_then_stays_there(t):
    if t < 20:
        return t
    return 20


racers = [
    Pod("Solid Performer", lambda t: t if t < 20 else 20),
    Pod("Slow Starter", lambda t: 0 if t < 30 else max(25, (t - 30) / 2)),
    Pod("To Infinity and Beyond", lambda t: t * 0.75),
    Pod("Jerky", lambda t: 15 if (t // 10) % 2 == 0 else -5)
]
