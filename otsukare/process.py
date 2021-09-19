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
import logging
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def convert_duolingo_time_to_hours(duolingo_hours) -> pd.Series:
    """Given a pandas series with duolingo time, produce hours conversion."""
    hour_replacements = {
        "Just now": 1,
        "yesterday": 24,
        "hours ago": 1,
        "hour ago": 1,
        "days ago": 24,
        "day ago": 24,
        "weeks ago": 24 * 7,
        "week ago": 24 * 7,
        "months ago": 24 * 7 * 31,
        "month ago": 24 * 7 * 31,
        "years ago": 24 * 7 * 52,
        "year ago": 24 * 7 * 52,
    }
    new_duolingo_hours = duolingo_hours

    for text, hours in hour_replacements.items():
        new_duolingo_hours = new_duolingo_hours.str.replace(text, str(hours))

    new_duolingo_hours = new_duolingo_hours.str.split(expand=True).fillna(1).astype(int).cumprod(axis=1)[1]
    return new_duolingo_hours


def parse_duolingo_html():
    """Converts raw HTML into cleaned up csv using BeautifulSoup4 and pandas."""
    input_path = Path("data", "duolingo_words.html")
    logging.debug(f"Loading HTML from {input_path}")
    with open(input_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    table = soup.find("table")
    parsed_words = pd.read_html(table.prettify())[0]

    parsed_words["hours"] = convert_duolingo_time_to_hours(parsed_words["Last practiced"])

    # Only take unique words to export to CSV
    parsed_words = parsed_words[["Word", "hours"]].drop_duplicates(subset="Word").sort_index()

    output_path = Path("data", "duolingo_words_raw.csv")
    logging.debug(f"Saving CSV to {output_path}")
    parsed_words.to_csv(output_path, encoding="utf-8", index=False)


def extract_duolingo_words_not_in_database():
    """Checks duolingo list for words not in database and creates extract."""
    input_path = Path("data", "duolingo_words_raw.csv")
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

    # Simple dataframe of new duolingo words
    duolingo_new_words = parsed_words.loc[~parsed_words["Word"].isin(known_words)].sort_values(["hours"])

    # Format to be similar to database
    duolingo_new_words = duolingo_new_words.rename(columns={"Word": "romanji"})
    duolingo_new_words = pd.DataFrame(duolingo_new_words, columns=database.columns + ["hours"])

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

    parse_duolingo_html()
    extract_duolingo_words_not_in_database()


if __name__ == "__main__":
    run()
