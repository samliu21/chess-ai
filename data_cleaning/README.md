# Data Cleaning Process
1. Download the raw PGN data file from <a href="https://database.lichess.org">Lichess</a>.
2. Download the `pgn-extract` module <a href="https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/">here</a>.
3. Run `pgn-extract --quiet -D --fencomments --fixresulttags -w 100000 -o output.pgn master_db.pgn`. This adds a FEN comment after each move and reduces each game to a single line. 
4. Run `extract_fen.py` to extract the FEN comments. 
5. `get_moves.py` determines the square that was moved out of and the square that was moved into for each move. 
6. `cat db.pgn | sort | uniq > file.txt` removes duplicates.
7. `cat file.txt | sort -R > file2.txt` randomizes the dataset.

