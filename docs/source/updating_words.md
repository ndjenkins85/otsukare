# Updating words process

1. Visit Google Sheets, File -> Download -> CSV. Save to `data` folder as `nick_japanese - words.csv`.
2. Run the following command `python -m otsukare.process -v`. This will produce a CSV with unknown Duolingo words to `data/duolingo_new_words.csv`.
3. Upload these words to database in new tab; add new known words.
4. If known, move to Kanji and Kana columns and add english. Remove rows where still unsure/unknown.
5. Add to main database, check for duplicates using =countif()
