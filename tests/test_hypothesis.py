import pytest
from synapse_wong.hypothesis import BayesianHypothesisCompetition, audio_scorer, meme_scorer


def test_bayesian_update_simple():
    priors = {"audio": 0.5, "meme": 0.5}
    scorers = {"audio": audio_scorer, "meme": meme_scorer}
    updater = BayesianHypothesisCompetition(priors, scorers)
    evidence = [{"metric": {"audio_energy": 0.8, "growth_pct": 120, "shares": 50}, "source": {"name":"YouTube"}}]
    post = updater.update(evidence)
    assert 'audio' in post and 'meme' in post
    # audio should have higher posterior in this synthetic case
    assert post['audio'] > post['meme']
