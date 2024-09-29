# server.py

import json
import redis
import random
import time
from inputimeout import inputimeout, TimeoutOccurred

REDIS_HOST = 'localhost'

def main():
    # Connect to Redis
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

    # Ask for student's name
    student_name = input("Enter your name: ")

    # Load quiz data from JSON file
    with open('quiz_data.json', 'r') as f:
        quiz_data = json.load(f)

    score = 0  # Initialize score
    question_idx = 0  # Track the question index
    print("\n--- Quiz Started! ---\n")

    while True:
        # Get the current question
        question = quiz_data[question_idx % len(quiz_data)]
        question_idx += 1

        # Display the question and options
        print(f"\nQuestion: {question['question']}")
        for idx, option in enumerate(question["options"], start=1):
            print(f"{idx}. {option}")

        # Handle user answer with a timeout
        try:
            answer = inputimeout(prompt="Your answer (enter the option number): ", timeout=10)
            # Validate input
            if not answer.isdigit() or int(answer) < 1 or int(answer) > len(question["options"]):
                print("Invalid input. Random answer will be selected.")
                answer_idx = random.randint(0, len(question["options"]) - 1)
            else:
                answer_idx = int(answer) - 1
        except TimeoutOccurred:
            print("Time's up! Random answer will be selected.")
            answer_idx = random.randint(0, len(question["options"]) - 1)

        selected_answer = question["options"][answer_idx]
        print(f"You selected: {selected_answer}")

        # Check if the answer is correct
        if selected_answer == question["correct_answer"]:
            score += 2
            print(f"Correct! +2 points. Current score: {score}")
        else:
            score -= 1
            print(f"Incorrect. -1 point. Current score: {score}")

        # Update the student's score in the Redis leaderboard
        redis_client.zincrby('leaderboard', 2 if selected_answer == question["correct_answer"] else -1, student_name)

        # Display updated score
        print(f"\n{student_name}, your total score: {score}")

        # Optional delay before next question
        time.sleep(0.5)

if __name__ == '__main__':
    main()
