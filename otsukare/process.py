# Copyright © 2021 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Tools for the manual processing of Duolingo <-> Database."""
import argparse
import getpass
import logging
from datetime import datetime as dt
from pathlib import Path

import duolingo
import pandas as pd
from tqdm import tnrange


def get_duolingo_info():
    """Login to Duolingo, get known words, details and translations."""
    lingo = duolingo.Duolingo("bluemania", getpass.getpass())

    vocab_overview = lingo.get_vocabulary("ja")["vocab_overview"]
    keep_cols = ["word_string", "last_practiced_ms", "skill", "strength"]

    df = pd.DataFrame(vocab_overview)
    df = df[keep_cols]
    df["last_practiced_ms"] = pd.to_datetime(df["last_practiced_ms"], unit="ms")
    df = df.drop_duplicates(subset="word_string")
    df = df.reset_index(drop=True)
    df["translation"] = ""

    for i in tnrange(len(df.index)):
        word_string = df.loc[i, "word_string"]
        response = lingo.get_translations([word_string], source="ja", target="en")
        translation = " / ".join(response[word_string])
        df.loc[i, "translation"] = translation

    output_path = Path("data", "duo_info.csv")
    df.to_csv(output_path, index=False)


def extract_duolingo_words_not_in_database():
    """Checks duolingo list for words not in database and creates extract."""
    input_path = Path("data", "duo_info.csv")
    logging.debug(f"Loading CSV from {input_path}")
    parsed_words = pd.read_csv(input_path)

    input_path = Path("data", "nick_japanese - words.csv")
    logging.debug(f"Loading CSV from {input_path}")
    database = pd.read_csv(input_path)

    # Get simple set of known kanji and kana
    known_kanji = database.dropna(subset=["kanji"])
    kanji = set(known_kanji["kanji"])
    kanji_kana = set(known_kanji["kana"])

    non_kanji_index = set(database.index) - set(known_kanji.index)
    kana = set(database.loc[non_kanji_index, "kana"])
    known_words = kanji | kanji_kana | kana

    duolingo_new_words = parsed_words.loc[~parsed_words["word_string"].isin(known_words)].sort_values(
        ["last_practiced_ms"]
    )

    # Simple dataframe of new duolingo words
    column_rename = {
        "word_string": "romanji",
        "last_practiced_ms": "last_practiced",
        "skill": "source",
        "translation": "english",
    }

    # Format to be similar to database
    columns = database.columns.tolist() + ["last_practiced", "strength"]
    duolingo_new_words = duolingo_new_words.rename(columns=column_rename)
    duolingo_new_words = pd.DataFrame(duolingo_new_words, columns=columns)
    duolingo_new_words["date_added"] = dt.now().date()

    # Only include those words practiced in last 6 months
    duolingo_new_words["last_practiced"] = pd.to_datetime(duolingo_new_words["last_practiced"])
    duolingo_new_words = duolingo_new_words.loc[
        duolingo_new_words["last_practiced"] > dt.now() - pd.DateOffset(month=6)
    ]

    output_path = Path("data", "duolingo_new_words.csv")
    logging.debug(f"Saving CSV to {output_path}")
    duolingo_new_words.to_csv(output_path)


def run() -> None:
    """Runs cleaning pipeline."""
    parser = argparse.ArgumentParser("Otsukare - find difference between duolingo and database")
    parser.add_argument("-v", action="store_true", help="Debug mode")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.v else logging.INFO
    log_path = Path("logs", "_log.txt")
    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        logging.basicConfig(
            level=log_level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()]
        )
        logging.warning("'/logs/' directory missing, cannot create log files.")

    get_duolingo_info()
    extract_duolingo_words_not_in_database()


if __name__ == "__main__":
    run()
