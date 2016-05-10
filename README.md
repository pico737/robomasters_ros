# robomasters_ros

## Get start
1. check if your computer has a catkin workspace in ~/ directory. If not, ..
..1`mkdir catkin_ws` ..
..2`cd catkin_ws/` ..
..3`mkdir src`..
..4`cd src/`..
..5`git clone https://github.com/pico737/robomasters_ros.git`..
..6`catkin_make` 
2. After you run the `roscore`, open a new terminal and pull the new code from github inside the ~/catkin_ws/src/robomasters_ros ..
...`catkin_make`..
...`source devel/setup.bash`..
...`rosrun trapezoid trapezoid_node.py/`..
3. Test to see if your node is correctly running, open a new terminal and ..
...`rosnode list`..
...`rostopic list`..
