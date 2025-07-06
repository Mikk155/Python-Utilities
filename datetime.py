'''
MIT License

Copyright (c) 2025 Mikk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
'''

from enum import IntEnum;

class Days:

    class Names(IntEnum):
        '''
            Days of the week enumeration
        '''
        Monday = 1;
        Tuesday = 2;
        Wednessday = 3;
        Thursday = 4;
        Friday = 5;
        Saturday = 6;
        Sunday = 7;

    __Array__: tuple[ str ] = (
        'MONDAY',
        'TUESDAY',
        'WEDNESDAY',
        'THURSDAY',
        'FRIDAY',
        'SATURDAY',
        'SUNDAY',
    );

    @staticmethod
    def FromString( day: str ) -> int | None:
        '''
            Return the value for the given day name.

            Case is not sensitive

            Returns a number between 1 for monday to 7 for sunday.

            If fails it returns None
        '''
        if day.upper() in Days.__Array__:
        #
            return Days.__Array__.index( day.upper() ) + 1;
        #
        return None;

    @staticmethod
    def FromInt( day: int ) -> str | None:
        '''
            Return the name of the day based on the given value between 1 for monday to 7 for sunday

            If fails it returns None
        '''
        day -= 1;

        if day > 0 and day < 8:
        #
            return Days.__Array__[ day ];
        #
        return None;
