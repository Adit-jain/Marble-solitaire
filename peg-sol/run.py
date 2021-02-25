import subprocess
import sys

command = sys.executable + " search.py input_files/size5.txt {}"


# Graph Search with A* using manhattan_distance
subprocess.call(command.format('astar'), shell=True)

# Graph Search with BFS
subprocess.call(command.format('bfs'), shell=True)
