class fmt:

    from utils.Logger import Logger;
    m_Logger = Logger( "Formater" );

    @staticmethod
    def PurgeCommentary( string: str ) -> str:

        '''
            Purge commentaries from a string
        '''

        while string.find( '/*' ) != -1:

            index_open = string.find( '/*' );

            if index_open != -1:

                string = string[ : index_open ] + string[ string.find( '*/' ) + 2 : ];

        if string.find( "//" ) != -1:

            Items = [ line for line in string.split( '\n' ) if not line.strip( ' ' ).startswith( '//' ) ];

            string = ''.join( f'{i}\n' for i in Items );

        return string;

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

        from os import walk;
        from os.path import exists;

        if exists( licence ):

            licence = open( licence, "r" ).read();

        if sources_folder is not None:

            if not exists( sources_folder ):

                fmt.m_Logger.error( "Folder \"<g>{}<>\" does not exists!", sources_folder );

                return;

            for root, _, DirectoryFiles in walk( sources_folder ):

                ValidFiles = [ file for file in DirectoryFiles if file.endswith( ".py" ) ];

                files += ValidFiles;

        Triple = "'''";

        if licence.endswith( '\n' ):
            licence = licence[ : -2 ];

        for file in files:

            if exists( file ):

                fileIO = open( file, 'r' ).read();

                if fileIO.startswith( Triple ):

                    fileIO = fileIO[ fileIO.find( Triple, 3 ) + 3 : ];
                
                    while fileIO.startswith( '\n' ):

                        fileIO = fileIO[ 1 : ];

                open( file, 'w' ).write( f'{Triple}\n{licence}\n{Triple}\n\n{fileIO}' );

            else:

                fmt.m_Logger.warn( "file \"<g>{}<>\" does not exists!", file );
