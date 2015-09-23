These are the utilities to scrape the Kanji information in
'http://www.manythings.org/kanji/d/'. They all serve different purposes.

* `scrape.py` - This is the main scraper. It gets the data and outputs a JSON file with
  words, and Kanjis. This JSON file can be used to generate the graphml file.
* `make_kanji_graph.py` - This takes the JSON output from `scrape.py`, and makes it into a Graphml
file.
