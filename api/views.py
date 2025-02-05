from django.http import JsonResponse
import math
import requests

# Helper functions
def is_prime(n):
    if n < 2 or not n.is_integer():
        return False
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 1 or not n.is_integer():
        return False
    n = int(n)
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n):
    if not n.is_integer():
        return False
    n = int(n)
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def classify_number(request):
    number_param = request.GET.get('number', None)

    # Handle invalid input
    try:
        number = float(number_param)
    except (ValueError, TypeError):
        return JsonResponse({
            "number": number_param,  # Include the invalid input
            "error": "Invalid input, not a number"
        }, status=400, content_type="application/json")

    # Process number properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    properties = ["even"] if number % 2 == 0 else ["odd"]
    
    if armstrong:
        properties.append("armstrong")

    # Calculate digit sum (only for integers)
    digit_sum = sum(int(d) for d in str(abs(int(number)))) if number.is_integer() else None

    # Get fun fact (for positive integers only)
    fun_fact = "No fact available"
    if number >= 0 and number.is_integer():
        try:
            response = requests.get(f"http://numbersapi.com/{int(number)}/math?json")
            if response.status_code == 200:
                data = response.json()
                fun_fact = data.get("text", fun_fact)
        except Exception:
            pass

    # Return valid JSON response
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return JsonResponse(result, status=200, content_type="application/json")
