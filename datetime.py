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
