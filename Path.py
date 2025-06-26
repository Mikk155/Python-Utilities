global workspace;
workspace = None;

class Path:

    from utils.Logger import Logger;
    m_Logger = Logger( "Path" );

    @staticmethod
    def SetWorkspace( path: str ) -> None:

        '''
            Set the workspace. if this is not used we'll get this file directory
        '''

        global workspace;
        workspace = path;

        Path.m_Logger.info( "Set workspace directory to \"<g>{}<>\"", path );

    @staticmethod
    def Workspace() -> str:

        global workspace;

        if workspace is not None:

            return workspace;

        from os.path import dirname;

        return dirname( __file__ );

    @staticmethod
    def enter( *args: tuple[str], SupressWarning = False, CreateIfNoExists = False, CurrentDir = None ) -> str:

        '''
            enter folder names as arguments to join a path
        '''

        from os import makedirs;
        from os.path import join, exists, isfile;

        directory: str = CurrentDir if CurrentDir is not None else Path.Workspace();

        for arg in args:

            directory = join( directory, arg );

            if not exists( directory ):

                if CreateIfNoExists:

                    if isfile(directory):

                        Path.m_Logger.warn( "Can NOT <c>CreateIfNoExists<> \"<g>{}<>\" is not a folder!", directory );

                    else:

                        makedirs( directory, exist_ok=True );

                if SupressWarning is False:

                    Path.m_Logger.warn( "\"<g>{}<>\" doesn't exists!", directory );

        return directory;
