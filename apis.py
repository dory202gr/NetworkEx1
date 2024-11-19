import re
from  consts import INT32_MIN, INT32_MAX


def calculate_message(operation: str):
    operation_elements = operation.split(": ")
    if len(operation_elements) > 2 or operation_elements == []:
        return None
    operation_to_execute = operation_elements[0]
    if operation_to_execute == "calculate":
        result = calculate(operation_elements[1])
        return result
    if operation_to_execute == "max":
        result = maximum(operation_elements[1])
        return result
    if operation_to_execute == "factor":
        result = factor(operation_elements[1])
        return result
    if operation_to_execute == "quit":
        return "quit"
    else:
        return None


def calculate(expression_to_calculate):
    if not verify_pattern(expression_to_calculate, r"^(0|[1-9]\d*)(\^|\/|\*|\-|\+)(0|[1-9]\d*)$"):
        return None
    try:
        if "^" in expression_to_calculate:
            expression_to_calculate = "**".join(expression_to_calculate.split("^"))
        res = eval(expression_to_calculate)
    except:
        return None
    if not INT32_MIN <= res <= INT32_MAX:
        return "error: result is too big"
    if isinstance(res, float):
        res = round(res, 2)
    return f"response: {res}."


def maximum(expression_to_calculate):
    if not verify_pattern(expression_to_calculate, r"^\((-?(0|[1-9]\d*))(\s-?(0|[1-9]\d*))*\)$"):
        return None
    number_list = list(map(lambda x: int(x), expression_to_calculate[1:-1].split()))
    return f"the maximum is {max(number_list)}"


def factor(expression_to_calculate):
    if not verify_pattern(expression_to_calculate, r"^[1-9]\d*$"):
        return None
    res = prime_factors(int(expression_to_calculate))
    unique_prime_list = []
    [unique_prime_list.append(item) for item in res if item not in unique_prime_list]
    res_str = ",".join(map(lambda x : str(x), unique_prime_list))
    return f"the prime factors of {expression_to_calculate} are: {res_str}"


def verify_pattern(expression, pattern):
    if re.match(pattern, expression):
        return True
    else:
        return False


def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(n ** 0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors
