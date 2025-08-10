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
        from os.path import join, exists, isfile, dirname;

        directory: str = CurrentDir if CurrentDir is not None else Path.Workspace();

        for arg in args:

            directory = join( directory, arg ) if arg != '..' else dirname( directory );

            if not exists( directory ):

                if CreateIfNoExists is True:

                    if isfile(directory) or directory.rfind( "." ) != -1:

                        if SupressWarning is False:

                            Path.m_Logger.warn( "Can NOT <c>CreateIfNoExists<> \"<g>{}<>\" is not a folder!", directory );

                    else:

                        makedirs( directory, exist_ok=True );

                if SupressWarning is False:

                    Path.m_Logger.warn( "\"<g>{}<>\" doesn't exists!", directory );

        return directory;

    @staticmethod
    def GetSteamInstallation() -> str:
    #
        '''Try getting Steam's installation path'''

        from os import environ;

        if "STEAM_INSTALLATION_PATH" in environ:
        #
            return environ[ "STEAM_INSTALLATION_PATH" ];
        #

        def TryGetPathFromInput() -> str:
        #
            from os import path;

            UserDefinedPath: str = None;

            while UserDefinedPath is None:
            #
                UserDefinedPath = input( "Write the absolute path to your steam installation folder.\nShould look like \"C:\Program Files (x86)\Steam\"" );

                if  ( UserDefinedPath == "" ) \
                or ( not path.isabs( UserDefinedPath ) ) \
                or ( not path.exists( UserDefinedPath ) ) \
                or ( not path.exists( path.join( UserDefinedPath, "steamapps" ) ) ):
                #
                    print( "Invalid path." );
                    UserDefinedPath = None;
                #
            #
            return UserDefinedPath;
        #

        DynamicFoundPath: str;

        from platform import system;

        OperativeSystem: str = system();

        match OperativeSystem:
        #
            case "Windows":
            #
                from os import path;

                PossiblePaths: list[str] = [
                    path.expandvars( r"%ProgramFiles(x86)%\Steam" ),
                    path.expandvars( r"%ProgramFiles%\Steam" )
                ];

                for pPath in PossiblePaths:
                #
                    if path.exists( pPath ):
                    #
                        return pPath;
                    #
                #

                try:
                #
                    import winreg;

                    with winreg.OpenKey( winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam" ) as key:
                    #
                        return winreg.QueryValueEx( key, "SteamPath" )[0];
                    #
                #
                except( ImportError, FileNotFoundError, OSError, PermissionError ) as e:
                #
                    Path.m_Logger.warn( "Something went wrong: {}", e );
                #

                from subprocess import run;
                DynamicFoundPath = TryGetPathFromInput();
                run( [ "setx", "STEAM_PATH", DynamicFoundPath ], shell=True );
            #
            case _:
            #
                Path.m_Logger.error( "Path.GetSteamInstallation is not implemented for you operative system.\nYou can write yourself the absolute path." );
                DynamicFoundPath = TryGetPathFromInput();
            #
        #

        return DynamicFoundPath;
