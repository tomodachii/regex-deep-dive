import re

print("    =======================================   ")
print("         Celsius - Fahrenheit converter\n")
print("Enter a temperature")
print("[!] Input must a float number followed by C or F, For example: 12.05C")
input = input(" - Enter Input: ")
print(" --- Received Input: " + input)

try:
    match = re.match(r"^([-0-9]+[\.0-9\s]*)([CF])$", input, flags=re.IGNORECASE)
    if match:
        input_number = float(match.group(1))
        type = match.group(2)
        if re.match(r"c", type, re.IGNORECASE):
            output = (input_number * 9 / 5) + 32  # calculate Fahrenheit
            print(f"{str(input_number)} C is {str(output)} F")
        else:
            output = (input_number - 32) * 5 / 9
            print(f"{str(input_number)} F is {str(output)} C")
    else:
        print("Expecting a number followed by C or F")
except Exception as e:
    print(e)
