import time

def countdown_timer():
    try:
        seconds = int(input("Enter the time in seconds for countdown: "))
        print(f"Countdown started for {seconds} seconds...")
        
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(timer, end="\r")
            time.sleep(1)
            seconds -= 1
        
        print("Time's up! ⏰")
        
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    countdown_timer()
