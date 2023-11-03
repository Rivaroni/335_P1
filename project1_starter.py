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

#look for avaiabile free times between the two schedules
def find_common_free_times(person1_free_times, person2_free_times, duration_of_meeting):
    common_free_times = []
    i = 0
    j = 0

    while i < len(person1_free_times) and j < len(person2_free_times):
        # find overlap between the two schedules
        start_time = max(person1_free_times[i][0], person2_free_times[j][0])
        end_time = min(person1_free_times[i][1], person2_free_times[j][1])

        if end_time - start_time >= duration_of_meeting:
            common_free_times.append((start_time, end_time))

        if person1_free_times[i][1] < person2_free_times[j][1]:
            i += 1
        else:
            j += 1

    return common_free_times

# func to handle multiple inputs from the file to find the common free times
def handle_common_times(p1_busy, p1_work, p2_busy, p2_work, dur):
    p1_schedule = schedule_to_minutes(p1_busy)
    p1_start, p1_end = time_to_minutes(p1_work[0]), time_to_minutes(p1_work[1])
    p1_hours = (p1_start, p1_end)

    p2_schedule = schedule_to_minutes(p2_busy)
    p2_start, p2_end = time_to_minutes(p2_work[0]), time_to_minutes(p2_work[1])
    p2_hours = (p2_start, p2_end)

    meeting_time = dur

    p1_free, p2_free = find_free(p1_schedule, p1_hours, meeting_time), find_free(p2_schedule, p2_hours, meeting_time)
    common_free =  find_common_free_times(p1_free, p2_free, meeting_time)

    return format_time(common_free)

def main():
    results = []

    with open("Input.txt", "r") as file:
        for line in file:
            schedule_data = json.loads(line.strip())
            meeting_slots = handle_common_times(
                schedule_data["person1_Schedule"],
                schedule_data["person1_DailyAct"],
                schedule_data["person2_Schedule"],
                schedule_data["person2_DailyAct"],
                schedule_data["duration_of_meeting"]
            )
            results.append(meeting_slots)


    with open("Output.txt", "w") as file:
        for result in results:
            file.write(json.dumps(result) + "\n")
        

if __name__ == "__main__":
    main()