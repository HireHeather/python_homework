# Task 1 Diary

import traceback

try:
    with open("diary.txt", "a") as diary_file:

        prompt = "What happened today? "

        while True:
            entry = input(prompt)

            diary_file.write(entry + "\n")

            if entry == "done for now":
                break

            prompt = "What else? "

except KeyboardInterrupt as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []

    for trace in trace_back:
        stack_trace.append(
            f"File: {trace[0]}, Line: {trace[1]}, Function Name: {trace[2]}, Message: {trace[3]}"
        )

    print(f"Exception type: {type(e).__name__}")

    message = str(e)
    if message:
        print(f"Exception message: {message}")

    print(f"Stack trace: {stack_trace}")
