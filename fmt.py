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
from datetime import datetime, timedelta;

class fmt:

    m_Logger = Logger( "Formater" );

    @staticmethod
    def DiscordUserMention( user ) -> str:

        '''
            Return a fixed ``discord.Member.mention`` string for globalization\n
            since a leading characters are added when the user has a custom nickname

            user could be a int or a guild Member instance
        '''

        if isinstance( user, int ):

            return f"<@{user}>";

        return f"<@{user.id}>";

    @staticmethod
    def FormatSourcesWithLicence( licence: str, *, sources_folder: str = None, files: list[str] = None ) -> None:
        '''
            Formats all .py files including the licence on the header

            `licence`: absolute path to a file. if fails to open then this assumes the licence string itself is a container.

            `sources_folder`: Folder to inspect for .py files to update.

            `files`: List of absolute path to files. `sources_folder` will add items here so have that value set to None.
        '''

        if files is None:
            files = [];

        from os import walk;
        from os.path import exists, join;

        if exists( licence ):

            licence = open( licence, "r" ).read();

        if sources_folder is not None:

            if not exists( sources_folder ):

                fmt.m_Logger.error( "Folder \"<g>{}<>\" does not exists!", sources_folder );

                return;

            for root, _, DirectoryFiles in walk( sources_folder ):

                ValidFiles = [ join( root, file ) for file in DirectoryFiles if file.endswith( ".py" ) ];

                files += ValidFiles;

        Triple = "'''";

        if licence.endswith( '\n' ):
            licence = licence[ : -2 ];

        for file in files:

            if exists( file ):

                try:

                    fileIO: str = open( file, 'r' ).read();

                    if fileIO.startswith( Triple ):

                        fileIO = fileIO[ fileIO.find( Triple, 3 ) + 3 : ];

                        while fileIO.startswith( '\n' ):

                            fileIO = fileIO[ 1 : ];

                    open( file, 'w' ).write( f'{Triple}\n{licence}\n{Triple}\n\n{fileIO}' );

                except Exception as e:

                    fmt.m_Logger.warn( "Exception: \"<g>{}<>\" for \"<c>{}<>\"", e, file );

            else:

                fmt.m_Logger.warn( "file \"<g>{}<>\" does not exists!", file );

    @staticmethod
    def DiscordCommandsChoices( obj: dict[str, str] | list[str] ) -> list:

        '''
        Converts a dictionary to a list of app_commands.Choice
        '''

        from discord import app_commands

        icount = 0;

        app_commands_choices = [];

        for k, v in obj.items() if isinstance( obj, dict ) else enumerate( obj ):

            if icount >= 25:

                fmt.m_Logger.warn( "Size is above discord limit of 25 items!" );

                break;

            icount += 1;

            if isinstance( k, int ):

                app_commands_choices.append( app_commands.Choice( name=v, value=str(k) ) );

            else:

                app_commands_choices.append( app_commands.Choice( name=k, value=v ) );

        return app_commands_choices;

    @staticmethod
    def TimeDelta( delta: timedelta ) -> tuple[int, int, int]:

        '''
            Return a tuple with the timedelta in seconds, minutes and hours
        '''

        TimeStampSeconds = int( timedelta.total_seconds() );

        return (
            int( TimeStampSeconds % 60 ),
            int( ( TimeStampSeconds % 3600) // 60 ),
            int( TimeStampSeconds // 3600 )
        );
