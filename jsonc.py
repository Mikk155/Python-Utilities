class jsonc( dict ):

    from utils.Logger import Logger;
    m_Logger = Logger( "Json Commentary" );

    def __init__( self, file_path: str, *, exists_ok=None ) -> dict | list:

        """
            Deserialize file into a json dict or list based on the absolute path ``file_path``

            ``exists_ok`` if true and the file doesn't exist we'll create it and initialize a empty dict
        """

        from os.path import exists;

        if exists( file_path ):

            from utils.fmt import fmt;
            from json import loads;

            json = {};
            
            try:
                json= loads( fmt.PurgeCommentary( open( file = file_path, mode = 'r' ).read() ) );
            except Exception as e:
                self.m_Logger.info( "Couldn't deserialize file <g>{}<> Generated empty.", e );

            super().__init__( json );

        elif exists_ok:

            open( file_path, 'w' ).write( "{ }" );

            self.m_Logger.info( "Couldn't open file <g>{}<> Generated.", file_path );

            super().__init__( {} );

            return;

        else:

            self.m_Logger.error( "Couldn't open file <g>{}<>", file_path );

            raise FileNotFoundError( f"Couldn't open file \"{file_path}\"" )

        super().__init__( {} );
