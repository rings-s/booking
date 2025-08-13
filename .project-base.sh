#!/bin/bash
tmux new-session -d -s project-base # new session named project-base
tmux split-window -v -t project-base -p 30 # split window vertically
tmux send-keys -t project-base 'cd back/ ' C-m # cd to back/
tmux split-window -h -t project-base -p 30 # split window horizontally
tmux send-keys -t project-base 'cd front/ && npm run dev' C-m # cd to front/ and run dev
tmux send-keys -t project-base 'nvim .' C-m # open nvim
tmux attach -t project-base # attach to session
