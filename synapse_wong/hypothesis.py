from __future__ import annotations
from typing import List, Dict, Callable
import math

# Hypothesis competition: simple Bayesian updater in log-space

Scorer = Callable[[Dict], float]

class BayesianHypothesisCompetition:
    """
    Each hypothesis has a prior P(H). For evidence items, each hypothesis has a scorer that returns P(e | H).
    We compute posterior P(H | E) ∝ P(H) * Π P(ei | H).
    Scorers must return values in (0,1].
    """
    def __init__(self, priors: Dict[str, float], scorers: Dict[str, Scorer]):
        # priors: name -> prior probability
        # scorers: name -> function(evidence) -> likelihood
        self.priors = priors.copy()
        self.scorers = scorers.copy()

    def update(self, evidences: List[Dict]) -> Dict[str, float]:
        # returns posterior distribution over hypotheses
        log_scores = {}
        for h, p in self.priors.items():
            if p <= 0:
                log_scores[h] = float('-inf')
            else:
                log_scores[h] = math.log(p)
        for e in evidences:
            for h in self.priors.keys():
                scorer = self.scorers.get(h)
                if scorer is None:
                    # neutral likelihood
                    continue
                lik = scorer(e)
                # guard
                lik = max(min(lik, 1.0), 1e-9)
                log_scores[h] += math.log(lik)
        # normalize
        max_log = max(log_scores.values())
        exp_scores = {h: math.exp(log_scores[h] - max_log) for h in log_scores}
        s = sum(exp_scores.values())
        posteriors = {h: (exp_scores[h] / s) for h in exp_scores}
        return posteriors

# Example scorers

def audio_scorer(evidence: Dict) -> float:
    # heuristic: if evidence.metric.get('audio_energy') high -> higher likelihood
    metric = evidence.get('metric', {})
    energy = metric.get('audio_energy', 0)
    growth = metric.get('growth_pct', 0)
    # simple mapping to (0,1]
    score = 0.5
    if energy > 0.7:
        score += 0.25
    if growth > 50:
        score += 0.2
    return min(score, 0.999)


def meme_scorer(evidence: Dict) -> float:
    metric = evidence.get('metric', {})
    shares = metric.get('shares', 0)
    tiktok = evidence.get('source', {}).get('name','').lower().find('tiktok') >= 0
    score = 0.2 + min(shares / 1000.0, 0.5)
    if tiktok:
        score += 0.15
    return min(score, 0.999)
