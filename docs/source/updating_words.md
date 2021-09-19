# Updating words process

1. Visit https://www.duolingo.com/words
2. Use inspect element on page. Right click the first `<html>` tag and select `Edit as HTML`. Copy entire text into `data/duolingo_words.html`
3. Download a local copy of the database as CSV to `data/nick_japanese - words.csv`
4. Run the following command `python -m otsukare.process -v`. This will produce a CSV with unknown Duolingo words to `data/duolingo_new_words.csv`.
5. Upload these words to database in new tab; add new known words.
