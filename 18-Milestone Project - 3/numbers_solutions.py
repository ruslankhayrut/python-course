"""
Number Names - Show how to spell out a number in English. 
You can use a preexisting implementation or roll your own, but you should support inputs up to at least one million 
(or the maximum value of your language's default bounded integer type, if that's less). 
Optional: Support for inputs other than positive integers (like zero, negative integers, and floating-point numbers).
"""


NUMBERS = {
    'base': ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'],
    'to_twenty': ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
                  'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'],
    'deca': ['twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
}
GREATNESS = ['', 'thousand', 'million', 'billion', 'trillion']
MAX_DIGITS = 15


class NumberName:
    def __init__(self, number: int):
        if len(str(number)) > MAX_DIGITS:
            raise Exception('Number too big')
        self.number = abs(number)
        self.negative = number < 0

    def splice_number(self):
        number_str = str(self.number)
        number_list = []
        remainder = len(number_str) % 3

        if remainder:
            number_list = [int(number_str[:remainder])]
            number_str = number_str[remainder:]

        number_list.extend([number_str[i:i+3]
                           for i in range(0, len(number_str), 3)])

        return number_list

    def __str__(self):
        if not self.number:
            return 'zero'

        str_repr = 'minus ' if self.negative else ''

        number_list = self.splice_number()
        while number_list:
            greatness = GREATNESS[len(number_list) - 1]
            current = ThreeDigitNumber(int(number_list.pop(0)))
            str_repr += f'{current} {greatness} '
        return str_repr


class ThreeDigitNumber:
    def __init__(self, number: int):
        self.number = number
        self.str_n = ''.join('0' for _ in range(
            3 - len(str(number)))) + str(number)

    def __str__(self):
        ls = []

        if self.str_n[0] != '0':
            ls.append(NUMBERS['base'][int(self.str_n[0])-1])
            ls.append('hundred')

        if self.str_n[1] == '1':
            ls.append(NUMBERS['to_twenty'][int(self.str_n[1:])-10])
            return ' '.join(ls)

        if self.str_n[1] != '0':
            ls.append(NUMBERS['deca'][int(self.str_n[1])-2])

        if self.str_n[2] != '0':
            ls.append(NUMBERS['base'][int(self.str_n[2])-1])

        return ' '.join(ls)


num = NumberName(14378782)
num1 = NumberName(1402)
num2 = NumberName(213240560457035)
num3 = NumberName(0)
num4 = NumberName(-12)

print(num)
print(num1)
print(num2)
print(num3)
print(num4)
