# When we refactor entity_extractor, the nlp pipeline (define_entity_ruler) will be moved here.
from collections import defaultdict
from spacy.matcher import PhraseMatcher
from spacy.language import Language
from spacy.tokens import Span
from spacy.util import filter_spans
from backend.services.nlp.vocabulary import (
    materials, fashion_nouns, fashion_adjectives, variants
)

def is_multi_token(entry):
    return " " in entry or "-" in entry

def build_alias():
    vocab = {entry.lower() for entry in materials + fashion_nouns + fashion_adjectives}
    aliases = {}

    for entry in vocab:
        if is_multi_token(entry):
            aliases[entry] = entry

    for canonical, alternates in variants.items():
        canonical = canonical.lower()
        if canonical not in vocab:
            raise ValueError(f"Variants key {canonical!r} is not in any vocabulary list.")
        for alternate in alternates:
            alternate = alternate.lower()
            if alternate in aliases and aliases[alternate] != canonical:
                raise ValueError(f"{alternate!r} maps to both {aliases[alternate]!r} and {canonical!r}")
            aliases[alternate] = canonical
    return aliases

class MergeVocabPhrases:
    def __init__(self, nlp):

        self.aliases = build_alias()
        self.matcher = PhraseMatcher(nlp.vocab, attr = "LOWER")

        grouped = defaultdict(list) 
        for phrase, canonical in self.aliases.items():
            pattern = nlp.make_doc(phrase)
            grouped[canonical].append(pattern)
   
        for canonical, patterns in grouped.items():
            self.matcher.add(canonical, patterns)


    def __call__(self, doc):

        matches = self.matcher(doc)
        spans = []

        for match_id, start, end in matches:
            spans.append(Span(doc, start, end, label = match_id))

        filtered = filter_spans(spans)

        with doc.retokenize() as retokenizer:
            for span in filtered:
                canonical = span.label_
                retokenizer.merge(span, attrs = {"LEMMA": canonical})
        return doc

@Language.factory("merge_vocab_phrases")
def create_merge_vocab_phrases(nlp, name):
    return MergeVocabPhrases(nlp)