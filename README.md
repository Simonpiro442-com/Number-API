# Number Classification API

## Features:
- Classifies numbers as **prime, perfect, armstrong**
- Returns **fun facts** using Numbers API
- JSON responses
- **Deployed to public API**

## API Usage:
### **GET /api/classify-number?number=371**
Example Response:
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
