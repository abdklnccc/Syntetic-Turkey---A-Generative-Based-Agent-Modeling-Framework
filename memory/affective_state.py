from dataclasses import dataclass, field


EMOTION_KEYS = ["anger", "fear", "hope", "sadness", "political_fatigue"]


def clamp01(value: float) -> float:
    return round(min(1.0, max(0.0, float(value))), 6)


@dataclass
class AffectiveState:
    baseline: dict[str, float] = field(default_factory=dict)
    anger: float = 0.0
    fear: float = 0.0
    hope: float = 0.0
    sadness: float = 0.0
    political_fatigue: float = 0.0

    def __post_init__(self):
        for key in EMOTION_KEYS:
            setattr(self, key, clamp01(self.baseline.get(key, getattr(self, key))))

    def update_from_decision(self, decision: dict) -> None:
        for key in EMOTION_KEYS:
            if key in decision:
                setattr(self, key, clamp01(decision[key]))

    def to_context_string(self) -> str:
        return (
            "Current affective state: "
            f"anger={self.anger:.2f}, fear={self.fear:.2f}, hope={self.hope:.2f}, "
            f"sadness={self.sadness:.2f}, political_fatigue={self.political_fatigue:.2f}."
        )

    def to_dict(self) -> dict[str, float]:
        return {key: getattr(self, key) for key in EMOTION_KEYS}
