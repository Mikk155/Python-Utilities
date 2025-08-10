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

    @staticmethod
    def PurgeCommentary( string: str ) -> str:
    #
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
    #

    def __init__(
        self,
        file_path: str,
        *,
        exists_ok: bool = False,
        schema_validation: str | dict = None,
        sensitive: bool = None,
        fnoutput: object = None
    ) -> dict | list:
    #
        """
            Deserialize a json object based on the absoulte ``file_path``

            ``exists_ok`` if true and the file doesn't exist we'll create it and initialize a empty dict

            ``schema_validation`` absolute path to a schema json to validate this object. this could also be defined in within the json with the \"$schema\" key.

            ``sensitive`` By default jsonc will return a empty dictionary if Deserialization fails. set this to True to raise a exception.

            ``fnoutput`` Method to send loggin output. You can set to ``print`` to just use print()
        """

        from os.path import exists;

        json = {};

        self.Output: object = fnoutput;

        if self.Output is not None:
        #
            self.Output( f"Loading {file_path}" );
        #

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
                msg: str = f"Couldn't deserialize file \"{file_path}\" {type(e).__name__}: {e}";

                if sensitive is True:
                #
                    raise Exception( msg );
                #
                elif self.Output is not None:
                #
                    self.Output( msg );
                #
            #
        #
        elif exists_ok is True:
        #
            open( file_path, 'w' ).write( "{ }" );

            if self.Output is not None:
            #
                self.Output( f"Couldn't open file {file_path}. Generated." );
            #
        #
        else:
        #
            raise FileNotFoundError( f"Couldn't open file {file_path}." )
        #

        if '$schema' in json:
        #
            from os.path import dirname;

            SchemaPath: str = json.pop( "$schema" );

            if schema_validation is None and not SchemaPath.startswith( 'http' ):
            #
                from utils.Path import Path;
                schema_validation = Path.enter( *SchemaPath.split( "/" ), CurrentDir=dirname(file_path) );
            #
        #

        super().__init__( json );

        if schema_validation is not None:
        #
            if self.Output is not None:
            #
                self.Output( f"Validating schema..." );
            #
            self.SchemaValidate( schema_validation, sensitive=sensitive );
        #
    #

    def SchemaValidate( self, schema: dict | str, sensitive: bool = None ) -> None:
    #
        '''
            Validates a schema
        '''

        from jsonschema import Draft7Validator, ValidationError;

        if isinstance( schema, str ):
        #
            schema = jsonc( schema, sensitive=sensitive, fnoutput=self.Output );
        #

        Validator = Draft7Validator(schema)

        Errors: list = list( Validator.iter_errors(self) );

        if Errors:
        #
            raise ValidationError( "\n".join( f"{e.message} at {list(e.path)}" for e in Errors ) );
        #

        # -TODO Add this. if sensitive is true raise exception else just pop items
        # if schema.get( "type" ) == "object" and not schema.get( "additionalProperties", True ):
        # #
        #     for k, v in schema.get( "properties", {} ).items():
        #         self.m_Logger.warn( "Invalid additional property <g>{}<>: <c>{}<>", k, self.pop( k, None ) );
        # #
    #
