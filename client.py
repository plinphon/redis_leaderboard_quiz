# client.py

import curses
import redis
import time

REDIS_HOST = 'localhost'

def display_leaderboard(stdscr, redis_client):
    # Set up curses environment
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(1000)  # Screen refresh every 1000ms (1 second)

    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(1, 2, "Real-Time Leaderboard", curses.A_BOLD)

        # Get leaderboard data from Redis
        leaderboard = redis_client.zrevrange('leaderboard', 0, -1, withscores=True)

        # Display the leaderboard
        if not leaderboard:
            stdscr.addstr(3, 2, "No data available yet.", curses.A_DIM)
        else:
            for rank, (student_name, score) in enumerate(leaderboard, start=1):
                stdscr.addstr(3 + rank, 2, f"{rank}. {student_name.decode('utf-8')}: {int(score)}")

        max_y, max_x = stdscr.getmaxyx()
        if max_y > 15:  # Check if the terminal height is sufficient
            stdscr.addstr(15, 2, "Press 'q' to quit.", curses.A_BOLD)
        else:
            stdscr.addstr(max_y - 1, 2, "Press 'q' to quit.", curses.A_BOLD)


        # Check for user input to quit the leaderboard display
        key = stdscr.getch()
        if key == ord('q'):
            break

        # Refresh screen and wait
        stdscr.refresh()
        time.sleep(0.2)

def main(stdscr):
    # Connect to Redis
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

    print("Starting real-time leaderboard...")
    try:
        display_leaderboard(stdscr, redis_client)
    except KeyboardInterrupt:
        print("Stopping leaderboard display.")

if __name__ == '__main__':
    curses.wrapper(main)
