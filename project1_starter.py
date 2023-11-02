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

def main():
    results = []

    # test out the functions
    time_text = "14:30"
    time_in_minutes = time_to_minutes(time_text)
    print("The time " + time_text + " = " + str(time_in_minutes))

    back_to_time = minutes_to_time(time_in_minutes)
    print(str(time_in_minutes) + " minutes = " + back_to_time)


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