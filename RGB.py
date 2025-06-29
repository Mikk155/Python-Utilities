class RGB:

    R = 0;
    G = 0;
    B = 0;

    def __init__( self, Red: int = 0, Green: int = 0, Blue: int = 0 ):
        self.R = 0 if Red < 0 else 255 if Red > 255 else Red;
        self.G = 0 if Green < 0 else 255 if Green > 255 else Green;
        self.B = 0 if Blue < 0 else 255 if Blue > 255 else Blue;

    def __repr__( self ):
        return "#{:02x}{:02x}{:02x}".format( self.R, self.G, self.B )

    def int( self ) -> int:
        return ( self.R << 16 ) | ( self.G << 8 ) | self.B;
