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
        from os.path import join, exists, isfile;

        directory: str = CurrentDir if CurrentDir is not None else Path.Workspace();

        for arg in args:

            directory = join( directory, arg );

            if not exists( directory ):

                if CreateIfNoExists:

                    if isfile(directory) or directory.find( '.' ):

                        if SupressWarning is False:

                            Path.m_Logger.warn( "Can NOT <c>CreateIfNoExists<> \"<g>{}<>\" is not a folder!", directory );

                    else:

                        makedirs( directory, exist_ok=True );

                if SupressWarning is False:

                    Path.m_Logger.warn( "\"<g>{}<>\" doesn't exists!", directory );

        return directory;
