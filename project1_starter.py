import json

def main():
    results = []

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