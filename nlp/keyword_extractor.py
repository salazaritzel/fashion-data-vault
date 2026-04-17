# Notebooks are for testing, python files are the real implementation.
# So........

# Loading the pipelines
import spacy


# After installing the new trained pipeline, load it via spacy.
nlp = spacy.load('en_core_web_sm')  

doc = nlp('I just want to make a difference. I want a sense of fulfillment.')

for token in doc:
    print(token.text)
# Calling the nlp object on a string of text will return a processed Doc
# Even though a Doc is processed – e.g. split into individual words and annotated – it still holds all information of the original text, like whitespace characters. 