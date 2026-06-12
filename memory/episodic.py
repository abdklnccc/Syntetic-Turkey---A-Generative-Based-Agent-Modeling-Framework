# synthetic_turkey/memory/episodic.py
"""
Episodic memory — file-based for test mode, Qdrant-ready for production.
Implements Smallville triple-score retrieval (Park et al., 2023).
ACT-R-inspired forgetting: memories decay rather than hard-cut.
"""

import json
import math
from pathlib import Path
from config import DB_DIR, TOP_K_RETRIEVAL, RECENCY_DECAY


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Minimal cosine similarity without numpy dependency."""
    dot  = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _simple_embed(text: str) -> list[float]:
    """
    Deterministic word-overlap embedding for test mode.
    Production: replace with Gemini Embedding 2 call.
    Maps unique word set to a fixed 64-dim binary vector.
    """
    words = set(text.lower().split())
    vocab = [
        "ekonomi", "para", "dolar", "enflasyon", "işsizlik", "fiyat",
        "seçim", "oy", "parti", "cumhurbaşkanı", "belediye", "başkan",
        "akp", "chp", "mhp", "hdp", "ysp", "dem", "erdoğan", "kılıçdaroğlu", "imamoglu",
        "oğan", "ogan", "ince", "deprem", "mülteci", "sığınmacı", "runoff",
        "istanbul", "ankara", "izmir", "konya", "gaziantep",
        "güvenlik", "terör", "pkk", "ordu", "suriye", "nato",
        "demokrasi", "hukuk", "yargı", "özgürlük", "baskı",
        "dini", "laiklik", "atatürk", "cumhuriyet", "millet",
        "aile", "çocuk", "eğitim", "sağlık", "konut",
        "protesto", "gösteri", "sokak", "vatandaş", "halk",
        "korku", "umut", "öfke", "gurur", "çaresizlik",
        "iptali", "ypk", "ysk", "sandık", "oy_sayımı", "mazbata",
        "seçim_iptali", "yenileme", "kampanya", "miting", "aday",
    ]
        
    vec = [1.0 if w in words else 0.0 for w in vocab]
    return vec


class EpisodicMemory:
    """
    File-backed episodic memory store.
    Production: swap _store/_retrieve for Qdrant calls.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.store_path = DB_DIR / f"{agent_id}_episodic_2023.json"
        self.memories: list[dict] = self._load()
        self.current_tick = 0

    def _load(self) -> list[dict]:
        if self.store_path.exists():
            return json.loads(self.store_path.read_text(encoding="utf-8"))
        return []

    def _save(self):
        self.store_path.write_text(
            json.dumps(self.memories, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def observe(self, content: str, importance: float, sim_tick: int,
                source_type: str = "shock", affective_multiplier: float = 1.0):
        """
        Add an observation to episodic memory.
        importance is boosted by affective_multiplier (emotion-salience encoding).
        """
        effective_importance = min(10.0, importance * affective_multiplier)
        entry = {
            "id":           f"{self.agent_id}_{sim_tick}_{len(self.memories)}",
            "content":      content,
            "importance":   round(effective_importance, 2),
            "sim_tick":     sim_tick,
            "source_type":  source_type,
            "retrieval_count": 0,
            "vector":       _simple_embed(content),  # swap for Gemini in prod
        }
        self.memories.append(entry)
        self._save()
        return entry["id"]

    def retrieve(self, query: str, n: int = TOP_K_RETRIEVAL) -> list[dict]:
        """
        Smallville triple-score retrieval:
        score = recency_score + importance_score + relevance_score
        Hard temporal filter: sim_tick <= current_tick
        """
        if not self.memories:
            return []

        query_vec = _simple_embed(query)

        scored = []
        for mem in self.memories:
            # Hard temporal filter
            if mem["sim_tick"] > self.current_tick:
                continue

            tick_age     = self.current_tick - mem["sim_tick"]
            recency      = RECENCY_DECAY ** tick_age
            importance   = mem["importance"] / 10.0
            relevance    = _cosine_similarity(query_vec, mem["vector"])
            total        = recency + importance + relevance

            # ACT-R activation: penalise very old, rarely retrieved memories
            actr_age     = max(1, tick_age)
            actr_boost   = math.log(1 + mem["retrieval_count"] + 1)
            actr_penalty = -0.5 * math.log(actr_age)
            actr_activation = actr_boost + actr_penalty

            # Block memories with very low activation (effective forgetting)
            if actr_activation < -3.0:
                continue

            scored.append((total, mem))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:n]

        # Update retrieval counts
        for _, mem in top:
            mem["retrieval_count"] += 1
        self._save()

        return [mem for _, mem in top]

    def summary(self) -> dict:
        return {
            "agent_id":      self.agent_id,
            "total_memories": len(self.memories),
            "current_tick":  self.current_tick,
        }
