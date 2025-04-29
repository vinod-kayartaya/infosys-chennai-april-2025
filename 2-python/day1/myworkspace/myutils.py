"""
This module contains custom utility functions
"""

def dirr(obj):
    """
    This function returns a list of non-dunder attributes of the input object
    
    To import this, open python REPL shell from the current folder
    `from myutils import dirr`
    """
    return [a for a in dir(obj) if not a.startswith('_')]


def number_to_words(number):
    """
    Converts a number into words (supports up to crores).
    """

    single_digits = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
        5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
        10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
        14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
        17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'
    }

    tens_multiples = {
        2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty',
        6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'
    }

    place_values = ['', 'hundred', 'thousand', 'lakh', 'crore']

    if number == 0:
        return single_digits[0]

    number_parts = []
    place_index = 0
    while number > 0:
        if place_index == 1:  # For the "hundred" place
            number_parts.append(number % 10)
            number //= 10
        else:  # For other places (thousands, lakhs, crores)
            number_parts.append(number % 100)
            number //= 100
        place_index += 1

    words = ''
    for place_index in range(len(number_parts) - 1, -1, -1):
        current_part = number_parts[place_index]
        if current_part == 0:
            continue

        if place_index == 1:  # Handle "hundred" separately
            words += single_digits[current_part] + ' ' + place_values[place_index] + ' '
        else:
            if current_part <= 20:
                words += single_digits[current_part] + ' ' + place_values[place_index] + ' '
            else:
                tens_place = current_part // 10
                units_place = current_part % 10
                words += tens_multiples.get(tens_place, '') + ' '
                if units_place > 0:
                    words += single_digits[units_place] + ' '
                words += place_values[place_index] + ' '

    return words.strip()


if __name__ == '__main__':
    number = int(input('Enter a number: '))
    # number = 1002
    print(number_to_words(number))
