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
