import time


def recurring_task():
    now = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    print(f"recurring_task: {now}")


def scheduled_task():
    now = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    print(f"scheduled_task: {now}")


def instant_task():
    now = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    print(f"instant_task: {now}")
