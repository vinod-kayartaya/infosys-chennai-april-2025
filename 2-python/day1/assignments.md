# Python Assignment: Number to Words Converter

## Problem Statement

Create a function called `number2words` that converts a given integer into its word representation in the Indian number system.

## Requirements

1. The function should take a single integer parameter
2. The function should return a string containing the number in words
3. The function should handle numbers up to 99,99,99,999 (99 crores)
4. The function should follow Indian number system conventions:
   - 1,00,000 = One Lakh
   - 1,00,00,000 = One Crore
   - Use proper spacing between words
   - Use proper capitalization

## Example Inputs and Outputs

```python
number2words(1234567)  # Returns: "twelve lakh thirty four thousand five hundred sixty seven"
number2words(100000)   # Returns: "one lakh"
number2words(10000000) # Returns: "one crore"
number2words(999999999) # Returns: "ninety nine crore ninety nine lakh ninety nine thousand nine hundred ninety nine"
number2words(0)        # Returns: "zero"
```

## Hints

1. Break down the number into different parts:

   - Crores
   - Lakhs
   - Thousands
   - Hundreds
   - Tens and Ones

2. Create helper functions for:

   - Converting numbers 0-99 to words
   - Handling hundreds
   - Handling thousands
   - Handling lakhs
   - Handling crores

3. Use dictionaries for number mappings:

   ```python
   ones = {
       0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
       5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'
   }

   tens = {
       10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
       14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
       17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
       20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
       60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'
   }
   ```

## Testing

Create test cases to verify:

1. Basic numbers (0-99)
2. Hundreds
3. Thousands
4. Lakhs
5. Crores
6. Edge cases (0, maximum value)
7. Numbers with all parts (e.g., 1234567)

## Submission Guidelines

1. Create a Python file named `number2words.py`
2. Implement the `number2words` function
3. Include docstring documentation
4. Add test cases
5. Follow PEP 8 style guidelines

## Example Implementation Structure

```python
def number2words(num):
    """
    Convert a number to its word representation in Indian number system.

    Args:
        num (int): The number to convert (0 to 999999999)

    Returns:
        str: The number in words

    Raises:
        ValueError: If the number is negative or greater than 999999999
    """
    # Your implementation here
    pass

def test_number2words():
    # Your test cases here
    pass

if __name__ == "__main__":
    test_number2words()
```

## Additional tasks

1. Handle negative numbers
2. Add support for decimal numbers
3. Implement unit tests using unittest or pytest
4. Add input validation and error handling
5. Optimize the code for performance

## Resources

1. [Indian Number System](https://en.wikipedia.org/wiki/Indian_numbering_system)
2. [Python String Formatting](https://docs.python.org/3/library/string.html#format-string-syntax)
3. [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
