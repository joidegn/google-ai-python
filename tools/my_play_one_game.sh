#!/usr/bin/env sh
./playgame.py -Eev --player_seed 42 --end_wait=0.25 --log_dir game_logs --turns 200 --map_file maps/multi_hill_maze/multi_maze_07.map "$@" "python ../MyBot.py" "python sample_bots/python/LeftyBot.py" "python sample_bots/python/HunterBot.py" "python sample_bots/python/GreedyBot.py"
