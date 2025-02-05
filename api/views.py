from django.http import JsonResponse
import requests

def is_prime(n):
    """Check if n is a prime number."""
    if n <= 1 or not n.is_integer():  # Prime numbers are positive integers greater than 1
        return False
    n = int(n)
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Determine if n is a perfect number (sum of proper divisors equals n)."""
    if n < 2 or not n.is_integer():  # Only positive integers can be perfect
        return False
    n = int(n)
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sum(divisors) == n

def is_armstrong(n):
    """Check if n is an Armstrong (narcissistic) number."""
    if not n.is_integer():  # Armstrong numbers are only valid for whole numbers
        return False
    n = int(n)
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum([d ** power for d in digits]) == abs(n)

def classify_number(request):
    """
    API endpoint to classify a number.
    URL format: /api/classify-number?number=371
    """
    number_param = request.GET.get('number', None)
    
    # Validate input: must be convertible to a float
    try:
        number = float(number_param)  # Accept floats
    except (ValueError, TypeError):
        return JsonResponse({
            "number": number_param,
            "error": True
        }, status=400)
    
    # Calculate mathematical properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    digit_sum = sum([int(d) for d in str(abs(int(number)))]) if number.is_integer() else None
    
    # Determine properties list based on Armstrong status and parity
    properties = []
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    if armstrong:
        properties.append("armstrong")

    # Fetch a fun fact from the Numbers API (only for positive integers)
    fun_fact = "No fact available"
    if number >= 0 and number.is_integer():
        try:
            response = requests.get(f"http://numbersapi.com/{int(number)}/math?json")
            if response.status_code == 200:
                data = response.json()
                fun_fact = data.get("text", fun_fact)
        except Exception:
            pass

    # Build the JSON response as per the specification
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    
    return JsonResponse(result, status=200)  # Always return 200 status code
