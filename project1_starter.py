import json

# converts the string times into minutes
def time_to_minutes(time):
    time_parts = time.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    total_minutes = hours * 60 + minutes
    return total_minutes

# converts minutes into a time string format
def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return "{:02d}:{:02d}".format(hours, minutes)

# Converts schedule times to minutes
def schedule_to_minutes(busy_times):
    times_in_min = []

    for busy_time in busy_times:
        start = time_to_minutes(busy_time[0])
        end = time_to_minutes(busy_time[1])
        times_in_min.append([start, end])
    
    return times_in_min

# Convert mintes back to string
def format_time(times_in_minutes):
    times_as_text = []
    
    for time_range in times_in_minutes:
        start_text = minutes_to_time(time_range[0])
        end_text = minutes_to_time(time_range[1])
        times_as_text.append([start_text, end_text])
    
    return times_as_text

# Looks for free time in schedule
def find_free(busy_times, working_hours, min_time):
    if not busy_times:
        start, end = working_hours
        if end - start >= min_time:
            return [(start, end)]
        else:
            return []
    
    free_times = []
    current = working_hours[0]
    end = working_hours[1]
    
    for busy_start, busy_end in busy_times:
        free_time = busy_start - current
        if free_time >= min_time:
            free_times.append((current, busy_start))
        if busy_end > current:
            current = busy_end

    if end - current >= min_time:
        free_times.append((current, end))
    
    return free_times

def main():
    results = []

    # test out the functions
    busy_times = [["09:00", "10:00"], ["12:00", "13:00"]]
    working_hours = ["09:00", "17:00"]
    min_time = 60

    working_hours_min = (time_to_minutes(working_hours[0]), time_to_minutes(working_hours[1]))
    busy_times_min = schedule_to_minutes(busy_times)
    free_times = find_free(busy_times_min, working_hours_min, min_time)
    formatted_free_times = format_time(free_times)

    print("Free times:")
    for start, end in formatted_free_times:
        print(f"From {start} to {end}")

    # Read input.txt file and store the data
    with open("Input.txt", "r") as f:
        for line in f:
            data = json.loads(line.strip())
            results.append(data)

    # Output results into output.txt file in a neat format
    with open("Output.txt", "w") as f:
        for result in results:
            f.write(json.dumps(result, indent=4) + "\n")

if __name__ == "__main__":
    main()