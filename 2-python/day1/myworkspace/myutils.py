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


def number2words(n):

    words1 = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
        5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
        10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
        14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
        17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'
    }

    words2 = {
        2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty',
        6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'
    }

    units = ['', 'hundred', 'thousand', 'lakh', 'crore']

    print(f'received {n}')
    # 1_23_45_6_78
    nums = []
    i = 1
    while n > 0:
        if i == 2:
            m = n % 10
            n //= 10
        else:
            m = n % 100
            n //= 100
        nums.append(m)
        i += 1

    s = ''
    while len(nums) > 0:
        x = nums.pop()
        u = units.pop()

        if x <= 20:
            s += words1.get(x) + ' '  + u + ' '
        else:
            x1 = x // 10
            x2 = x % 10
            s += words2.get(x1) + ' ' + words1.get(x2) + ' '  + u + ' '

    print(s)


if __name__ == '__main__':
    # n = input('Enter a number: ')
    n = 12345678
    print(number2words(n))
