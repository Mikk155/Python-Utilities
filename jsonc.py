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
