# Tetris-Command-Line
My third terminal game, tetris

how it works
rotation matrix: instead of hardcoding every possible position, I used a rotation system to transform the coordinates of the tetrominoes.

the well system: the game board is a 2D array (the well). when a piece lands, its coordinates are locked into the array and it becomes part of the static map.

line clearing: after every piece locks, the script scans the 2D array for full rows. if a row is full, it pops it out and shifts everything above it down by one.

technical wins
collision look-ahead: before the piece moves or rotates, the game runs a "check" function. if the next position would overlap with a wall or an existing block, the move is canceled.

ghost pieces: I implemented a preview of where the piece will land, which is just a recursive function that checks the collision logic downwards until it hits something.

gravity scaling: the tick speed increases as your score goes up, making the time.sleep() duration shorter so the game actually gets harder.

what's next
refactoring into oop
