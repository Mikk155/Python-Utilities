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

class RGB:

    R = 0;
    G = 0;
    B = 0;

    def __init__( self, Red: int = 0, Green: int = 0, Blue: int = 0 ):
        self.R = max( 0, min( 255, Red ) );
        self.G = max( 0, min( 255, Green ) );
        self.B = max( 0, min( 255, Blue ) );

    def __repr__( self ):
        return "#{:02x}{:02x}{:02x}".format( self.R, self.G, self.B )

    @property
    def hex( self ) -> int:
        return ( self.R << 16 ) | ( self.G << 8 ) | self.B;

    def cmd( self, message: str, background: bool = False, reset: bool = True ) -> str:

        '''
            Colorize and return message for printing.

            May only works on windows 10-11

            background: if true colorize the background instead of the characters

            reset: if false do not reset the color after message. so any subsequent string will be also colored.
        '''

        message = f"\033[{48 if background else 38};2;{self.R};{self.G};{self.B}m{message}"

        if reset:

            return f'{message}\033[0m';

        return message;
