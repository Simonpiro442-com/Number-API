from django.shortcuts import render
from django.http import JsonResponse
import requests

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [1]

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i :
                divisors.append(n // i)
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum([d ** power for d in digits]) == abs(n)

def classify_number(request):
    number_param = request.GET.get('number', None)

    try:
        number = int(number_param)
    except (ValueError, TypeError):
        return JsonResponse({
            "number": number_param,
            "error": True
            }, status=400)

    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    digit_sum = sum([int(d) for d in str(abs(number))])

    if armstrong:
        properties = ["armstrong", "even"] if number % 2 == 0 else ["armstrong", "odd"]
    else:
        properties = ["even"] if number % 2 == 0 else["odd"]

    fun_fact = "No fact available"
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math?json")
        if response.status_code == 200:
            data = response.json()
            fun_fact = data.get("text", fun_fact)
    except Exception:
        pass

    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    
    return JsonResponse(result)