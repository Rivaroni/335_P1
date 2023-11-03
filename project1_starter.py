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

# looks for the common free times between two schedules
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

    # Read input.txt file and store the data
    with open("Input.txt", "r") as file:
        data = json.load(file)
        test_cases = data["test_cases"]

    # run each test case
    for case_number, test_case in enumerate(test_cases, start=1):
 
        schedule1 = test_case.get("person1_Schedule", [])
        daily1 = test_case.get("person1_DailyAct", [])
        person1_schedule = schedule_to_minutes(schedule1)
        person1_daily = [time_to_minutes(time) for time in daily1]
        person1_free = find_free(person1_schedule, person1_daily, test_case.get("duration_of_meeting", 30))

        schedule2 = test_case.get("person2_Schedule", [])
        daily2 = test_case.get("person2_DailyAct", [])
        person2_schedule = schedule_to_minutes(schedule2)
        person2_daily = [time_to_minutes(time) for time in daily2]
        person2_free = find_free(person2_schedule, person2_daily, test_case.get("duration_of_meeting", 30))
        duration_of_meeting = test_case.get("duration_of_meeting", 30)

        # find common times
        common_free = find_common_free_times(person1_free, person2_free, test_case.get("duration_of_meeting", 30))

        # print to output file in nice format
        case_result = "Test Case " + str(case_number) + ":\n"
        case_result += f"schedule1 {json.dumps(schedule1)}\n"
        case_result += f"daily1 {json.dumps(daily1)}\n"
        case_result += f"schedule2 {json.dumps(schedule2)}\n"
        case_result += f"daily2 {json.dumps(daily2)}\n"
        case_result += f"duration: {minutes_to_time(duration_of_meeting)} minutes\n\n"

        case_result += "Person 1 Free Times:\n"
        for start, end in format_time(person1_free):
            case_result += f"From {start} to {end}\n"

        case_result += "\nPerson 2 Free Times:\n"
        for start, end in format_time(person2_free):
            case_result += f"From {start} to {end}\n"
        
        case_result += "\nCommon Free Times:\n"
        for start, end in format_time(common_free):
            case_result += f"From {start} to {end}\n"
        
        case_result += "-" * 50 + "\n"
        results.append(case_result)

    # Write the results to the output file
    with open("Output.txt", "w") as file_output:
        for result in results:
            file_output.write(result)

if __name__ == "__main__":
    main()
