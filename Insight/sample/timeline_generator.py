import random
from datetime import datetime, timedelta

# Generate a random timeline with events
def generate_timeline_data(num_events=10):
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    end_date = datetime(2022, 1, 1, 23, 59, 59)
    
    timeline_data = []
    
    for _ in range(num_events):
        random_timestamp = start_date + timedelta(minutes=random.randint(1, (end_date - start_date).total_seconds() // 60))
        event = f"Event {random.randint(1, 100)}"
        timeline_data.append(f"{random_timestamp.strftime('%Y-%m-%d %H:%M:%S')}, {event}")
    
    return timeline_data

# Save the generated timeline data to a file
def save_to_file(file_path, timeline_data):
    with open(file_path, 'w') as file:
        file.write('\n'.join(timeline_data))

if __name__ == "__main__":
    # Adjust the number of events as needed
    num_events = 10
    timeline_data = generate_timeline_data(num_events)
    
    # Specify the desired file path
    file_path = 'timeline_data.txt'
    
    # Save the generated timeline data to the file
    save_to_file(file_path, timeline_data)
    
    print(f"Generated timeline data saved to: {file_path}")
