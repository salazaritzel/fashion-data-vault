import pytest
import pandas as pd
import uuid
from backend.services.nlp.entity_extractor import EntityExtractor

@pytest.fixture(scope="module")
def extractor():
    return EntityExtractor() # loads the spaCy model once per file

def trends_in(result):
    return {value for entity_type, value in result if entity_type == "trend"}

def test_repeated_trend_counts_once(extractor):
    result = extractor.extract_article_entities(
        "suede boots are back. suede boots, suede boot, everywhere"
    )
    assert trends_in(result) == {"suede boot"}

def test_brand_and_season_are_found(extractor):
    result = extractor.extract_article_entities("a front row scene report from chanel's spring 2027 show")
    assert ("brand", "chanel") in result
    assert ("season", "spring 2027") in result

def test_no_fashion_terms_return_empty(extractor):
    result = extractor.extract_article_entities("i went to my pilates class today")
    assert result == set()

def test_diff_trends_in_one_article_returns_multiple(extractor):
    result = extractor.extract_article_entities("during miu miu's ss27 show, we saw plaid skirts, tailored suits, and embroidered eveningwear.")
    expected = {("brand", "miu miu"), ("season", "ss27"), ("trend", "plaid skirt"), ("trend", "embroider eveningwear"), ("trend", "tailor suit")}
    assert expected <= result, f"missing: {expected - result}"

def test_accurate_color_or_aesthetic(extractor):
    result = extractor.extract_article_entities("i've been noticing a lot of y2k references on the runway, especially the use of magenta.")
    assert ("aesthetic", "y2k") in result
    assert ("color", "magenta") in result

def make_article(conn):
    """Insert a throwaway article (the foreign key needs one) and return its id."""
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO aggregates_trend (source_type, source_name, title, link) "
            "VALUES ('test', 'test', 'test article', %s) RETURNING id",
            (f"https://example.com/{uuid.uuid4()}",),
        )
        article_id = cur.fetchone()[0]
    conn.commit()
    return article_id

def rows_for(conn, article_id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT entity_type, entity_value FROM article_entities WHERE article_id = %s",
            (article_id,),
        )
        return set(cur.fetchall())

def test_save_replaces_old_rows(extractor, conn):
    article_id = make_article(conn)
    try:
        # We're saving first into our database, then we're comparing what we saved with 'first' below.
        first = {("trend", "plaid skirt"), ("brand", "prada")}
        extractor.save_article_entities_to_database(article_id, first, conn)
        assert rows_for(conn, article_id) == first 
        
        # We're saving second into our database, then we're comparing what we saved with 'second' below.
        second = {("trend", "plaid skirt"), ("color", "red")}
        extractor.save_article_entities_to_database(article_id, second, conn)
        assert rows_for(conn, article_id) == second # the saved rows should equal `second`, so the brand row is GONE
    finally:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM aggregates_trend WHERE id = %s", (article_id,))
        conn.commit()

def test_process_articles_saves_each_article(extractor, conn):
    first_id = make_article(conn)
    second_id = make_article(conn)
    try:
        data_frame = pd.DataFrame({
            "id": [first_id, second_id],
            "full_text": [
                "miu miu always draws an it-girl crowd. from alexa chung in a striped cardigan and pencil skirt to maude apatow in relaxed suiting, the front row looked as cool as ever for miu miu's spring 2027 show.",
                "i went to pilates class today",
            ],
        })

        count = extractor.process_articles(data_frame, conn)
        assert count == 2

        assert {("brand", "miu miu"), ("season", "spring 2027")} <= rows_for(conn, first_id)
        assert rows_for(conn, second_id) == set()
    finally:
        conn.rollback()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM aggregates_trend WHERE id = %s", (first_id,))
            cur.execute("DELETE FROM aggregates_trend WHERE id = %s", (second_id,))
        conn.commit()

def test_process_articles_with_no_articles_returns_zero(extractor, conn):
    data_frame = pd.DataFrame({"id": [], "full_text": []})
    assert extractor.process_articles(data_frame, conn) == 0

       