#!/bin/bash
mkdir -p static/download/files_to_zip
mkdir -p static/upload/merge

# 启动第一个Python程序，并在第一个窗格中显示输出
# konsole --hold -e 'python3 delete_old_files.py; read -p "Press Enter to exit"'

# 创建一个新的tmux会话，并在第二个窗格中启动第二个Python程序
# tmux new-session -d -s my_session "flask run"

# # 分离tmux会话，使其在后台运行
# tmux detach -s my_session

# # 在控制台显示提示信息
# echo "Both Python scripts are running. Use 'tmux attach-session -t my_session' to view the outputs."


# 创建一个新的tmux会话
tmux new-session -d -s my_session

# 在第一个窗格中运行第一个Python程序
tmux send-keys -t my_session 'python3 delete_old_files.py' C-m

# 分割当前窗格，创建第二个窗格
tmux split-window -t my_session

# 在第二个窗格中运行第二个Python程序
tmux send-keys -t my_session 'flask run' C-m

# 进入tmux会话，观察两个程序的输出
tmux attach-session -t my_session