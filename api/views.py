from django.http import JsonResponse
import math
import requests

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    divisors_sum = sum(i for i in range(1, abs(n)//2 + 1) if n % i == 0)
    return divisors_sum == abs(n)

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def classify_number(request):
    # Retrieve number parameter from GET
    number_param = request.GET.get('number', None)

    # Try to handle float or integer input correctly
    try:
        number = float(number_param)  # Can handle integers and floats
    except (ValueError, TypeError):
        # If conversion fails, return error response
        return JsonResponse({
            "number": number_param,
            "error": "Invalid input, not a number"
        }, status=400)

    # If number is valid, proceed with classification
    prime = is_prime(int(number))  # Integer conversion for prime check
    perfect = is_perfect(int(number))  # Integer conversion for perfect number check
    armstrong = is_armstrong(int(number))  # Integer conversion for Armstrong check
    digit_sum = sum([int(d) for d in str(abs(number))])  # Sum of digits

    # Determine number properties
    if armstrong:
        properties = ["armstrong", "even"] if number % 2 == 0 else ["armstrong", "odd"]
    else:
        properties = ["even"] if number % 2 == 0 else ["odd"]

    # Get fun fact from Numbers API
    fun_fact = "No fact available"
    try:
        response = requests.get(f"http://numbersapi.com/{int(abs(number))}/math?json")
        if response.status_code == 200:
            data = response.json()
            fun_fact = data.get("text", fun_fact)
    except Exception:
        pass

    # Return valid response with proper status and data
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return JsonResponse(result, status=200)

