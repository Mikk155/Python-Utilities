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

    def DiscordUserMention( user ) -> str:
        
        '''
            Return a fixed ``discord.Member.mention`` string for globalization\n
            since a leading characters are added when the user has a custom nickname

            user could be a int or a guild Member instance
        '''

        if isinstance( user, int ):

            return f"<@{user}>";

        return f"<@{user.id}>";