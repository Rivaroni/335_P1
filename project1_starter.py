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


    # Read input.txt file and store the data
    with open("Input.txt", "r") as f:
        for line in f:
            data = json.loads(line.strip())
            results.append(data)
    for data in results:
        person1_schedule = data.get("person1_Schedule", [])
        person1_daily_activity = data.get("person1_DailyAct", [])
        person2_schedule = data.get("person2_Schedule", [])
        person2_daily_activity = data.get("person2_DailyAct", [])
        duration_of_meeting = data.get("duration_of_meeting", 30)
         # Convert daily activity time to minutes
        person1_daily_activity_min = [time_to_minutes(time) for time in person1_daily_activity]
        person2_daily_activity_min = [time_to_minutes(time) for time in person2_daily_activity]

        # Find free time for both individuals
        person1_working_hours_min = (person1_daily_activity_min[0], person1_daily_activity_min[1])
        person2_working_hours_min = (person2_daily_activity_min[0], person2_daily_activity_min[1])

        person1_busy_times_min = schedule_to_minutes(person1_schedule)
        person2_busy_times_min = schedule_to_minutes(person2_schedule)

        person1_free_times = find_free(person1_busy_times_min, person1_working_hours_min, duration_of_meeting)
        person2_free_times = find_free(person2_busy_times_min, person2_working_hours_min, duration_of_meeting)

        # Find common free times
        common_free_times = find_common_free_times(person1_free_times, person2_free_times, duration_of_meeting)

        # Convert free times back to text format
        formatted_person1_free_times = format_time(person1_free_times)
        formatted_person2_free_times = format_time(person2_free_times)
        formatted_common_free_times = format_time(common_free_times)

    # Output results into output.txt file in a neat format
    with open("Output.txt", "w") as f:
        
         f.write("schedule1 " + str(person1_schedule) + "\n")
         f.write("daily1 " + str(person1_daily_activity) + "\n")
         f.write("schedule2 " + str(person2_schedule) + "\n")
         f.write("daily2 " + str(person2_daily_activity) + "\n")
        
         f.write("Person 1 Free Times:\n")
         for start, end in formatted_person1_free_times:
             f.write(f"From {start} to {end}\n")
        
         f.write("Person 2 Free Times:\n")
         for start, end in formatted_person2_free_times:
             f.write(f"From {start} to {end}\n")

         f.write("Common Free Times:\n")
         for start, end in formatted_common_free_times:
             f.write(f"From {start} to {end}\n")
   
        

if __name__ == "__main__":
    main()