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

from utils.Logger import Logger;

class jsonc( dict ):

    m_Logger = Logger( "Json Commentary" );

    @staticmethod
    def PurgeCommentary( string: str ) -> str:

        '''
            Purge commentaries from a string
        '''

        FormattedString = '';

        InPair = False;
        InSingleCommentary = False;
        InMultiCommentary = False;
        SkipNextChar = False;

        for index, char in enumerate(string):

            if SkipNextChar is True:
                SkipNextChar = False;
                continue;

            if InPair is True:

                if char == '\"' and string[index - 1 ] != '\\':
                    InPair = False;

            elif InSingleCommentary is True:

                if char == '\n' or ( char == '\\' and string[index + 1 ] == 'n' ):
                    InSingleCommentary = False;
                    SkipNextChar = True;
                continue;

            elif InMultiCommentary is True:

                if char == '*' and string[index + 1 ] == '/':
                    InMultiCommentary = False;
                    SkipNextChar = True;
                continue;

            elif char == '/' and string[index + 1 ] == '/':
                InSingleCommentary = True;
                SkipNextChar = True;
                continue;

            elif char == '/' and string[index + 1 ] == '*':
                InMultiCommentary = True;
                SkipNextChar = True;
                continue;

            elif char == '\"' and string[index - 1 ] != '\\':
                InPair = True;

            elif char == ' ':
                continue;

            FormattedString += char;

        return FormattedString;

    def __init__(
        self,
        file_path: str,
        *,
        exists_ok: bool = False,
        schema_validation: str | dict = None,
        sensitive: bool = None
    ) -> dict | list:

        """
            Deserialize file into a json dict or list based on the absolute path ``file_path``

            ``exists_ok`` if true and the file doesn't exist we'll create it and initialize a empty dict
        """

        from os.path import exists;

        json = {};

        if exists( file_path ):
        #
            from utils.fmt import fmt;
            from json import loads;

            try:
            #
                json: list | dict = loads( jsonc.PurgeCommentary( open( file = file_path, mode = 'r' ).read() ) );
            #
            except Exception as e:
            #
                msg: str = self.m_Logger.error( "Couldn't deserialize file <g>{}<> <r>{}<><y>:<> <r>{}<>", file_path, type(e).__name__, e );

                if sensitive is True:
                #
                    raise Exception(msg)
                #
            #
        #
        elif exists_ok is True:
        #
            open( file_path, 'w' ).write( "{ }" );
            self.m_Logger.error( "Couldn't open file <g>{}<> Generated.", file_path );
        #
        else:
        #
            self.m_Logger.error( "Couldn't open file <g>{}<>", file_path );
            raise FileNotFoundError( f"Couldn't open file \"{file_path}\"" )
        #

        if '$schema' in json:
        #
            from os.path import join, dirname;

            SchemaPath: str = json.pop( "$schema" );

            if schema_validation is None: # Append json-defined if the code dont send a explicit one
            #
                schema_validation = join( dirname( file_path ), SchemaPath );
            #
        #

        super().__init__( json );

        if schema_validation is not None and schema_validation != -1:
        #
            self.SchemaValidate( schema_validation, sensitive=sensitive );
        #

    def SchemaValidate( self, schema: dict | str, sensitive: bool = None ) -> None:
        '''
            Validates a schema
        '''

        self.m_Logger.info( "Start validating schema <g>{}<>", schema );

        from jsonschema import Draft7Validator, ValidationError;

        if isinstance( schema, str ):
        #
            schema = jsonc( schema, schema_validation=-1 );
        #

        Validator = Draft7Validator(schema)

        Errors: list = list( Validator.iter_errors(self) );

        if Errors:
        #
            raise ValidationError( "\n".join( f"{e.message} at {list(e.path)}" for e in Errors ) );
        #

        # if schema.get( "type" ) == "object" and not schema.get( "additionalProperties", True ):
        # #
        #     for k, v in schema.get( "properties", {} ).items():
        #         self.m_Logger.warn( "Invalid additional property <g>{}<>: <c>{}<>", k, self.pop( k, None ) );
        # #
