# Data Cleaning Process
1. Download raw PGN file from https://database.lichess.org
2. Download the `pgn-extract` <a href="https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/">module</a> and call `pgn-extract --quiet -D --fencomments --fixresulttags -w 100000 -o output.pgn master_db.pgn`. This adds a FEN comment after each move
3. Run `extract_fen.py` to extract the FEN comments, keeping only the board position and turn in the FEN
4. Run `get_moves.py` to extract the square that was moved from and to in the current FEN position
5. `cat db.pgn | sort | uniq > file.txt` removes duplicates
6. `cat file.txt | sort -R > file2.txt` randomizes the dataset

