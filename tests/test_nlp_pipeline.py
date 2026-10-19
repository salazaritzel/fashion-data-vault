import pytest
import spacy
from backend.services.nlp.nlp_pipeline import MergeVocabPhrases

class TestNLPPipeline:

    def test_merge_vocab_phrases(self):
        nlp = spacy.blank("en")
        merger = MergeVocabPhrases(nlp)
        doc = merger(nlp("a wide-leg jean"))

        assert [token.text for token in doc] == ["a", "wide-leg", "jean"]
        assert doc[1].lemma_ == "wide-leg"

    def test_variant_spelling_maps_to_canonical(self):
        nlp = spacy.blank("en")
        merger = MergeVocabPhrases(nlp)
        doc = merger(nlp("a high waisted jean"))

        assert [token.text for token in doc] == ["a", "high waisted", "jean"]
        assert doc[1].lemma_ == "high-rise"

    @pytest.mark.parametrize("text", [
    "a faux fur coat",
    "a faux-fur coat",
    "a faux - fur coat",
])
    
    def test_faux_fur_spellings(self, text):
        nlp = spacy.blank("en")
        merger = MergeVocabPhrases(nlp)
        doc = merger(nlp(text))

        assert len(doc) == 3
        assert doc[1].lemma_ == "faux fur"