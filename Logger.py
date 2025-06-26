from colorama import init as colorama
global colorama_init;
colorama_init: bool = False;

class Logger():

    name: str;

    class Level:

        CRITICAL: int = ( 1 << 0 );
        ERROR: int = ( 1 << 1 );
        WARNING: int = ( 1 << 2 );
        INFORMATION: int = ( 1 << 3 );
        DEBUG: int = ( 1 << 4 );
        TRACE: int = ( 1 << 5 );

    level: int = ( Level.DEBUG | Level.INFORMATION | Level.WARNING | Level.TRACE );

    @staticmethod
    def ToggleLevel( self, level: Level ):

        if Logger.level & level:

            Logger.level &= level;

        else:

            Logger.level |= level;

    @staticmethod
    def SetLevel( self, level: Level ):

        if not Logger.level & level:

            Logger.level |= level;

    @staticmethod
    def ClearLevel( self, level: Level ):

        if Logger.level & level:

            Logger.level &= level;

    def __init__( self, name: str ):

        global colorama_init;
        if not colorama_init:
            colorama();
            colorama_init = True;

        self.name = name;

    from colorama import Fore as c;

    def log( self, levelname: str, color: str, message: str, level: Level, *args ) -> str:

        if not Logger.level & level and level != Logger.Level.ERROR and level != Logger.Level.CRITICAL:
            return;

        from datetime import datetime;

        now = datetime.now();

        if len(args) > 0:
            message = message.format( *args );

        message = '[{}{}{}:{}{}{}:{}{}{}] [{}{}{}] [{}{}{}] {}'.format(
            Logger.c.YELLOW, now.hour, Logger.c.RESET,
            Logger.c.YELLOW, now.minute, Logger.c.RESET,
            Logger.c.YELLOW, now.second, Logger.c.RESET,
            color, levelname, Logger.c.RESET, Logger.c.CYAN,
            self.name, Logger.c.RESET, message
        );

        ColorList = {
            "R": Logger.c.RED,
            "G": Logger.c.GREEN,
            "Y": Logger.c.YELLOW,
            "B": Logger.c.BLUE,
            "M": Logger.c.MAGENTA,
            "C": Logger.c.CYAN,
            # Aliases
            "red": Logger.c.RED,
            "green": Logger.c.GREEN,
            "yellow": Logger.c.YELLOW,
            "blue": Logger.c.BLUE,
            "magenta": Logger.c.MAGENTA,
            "cyan": Logger.c.CYAN,
        };

        for pv, v in ColorList.items():

            pv = [ pv.upper(), pv.lower() ];

            for p in pv:

                while f'<{p}>' in message:

                    message = message.replace( f'<{p}>', v, 1 );
                    message = message.replace( f'<>', Logger.c.RESET, 1 );

        print( message );

    def debug( self, message: str, *args ):
        self.log( "debug", self.c.CYAN, message, Logger.Level.DEBUG, *args );

    def info( self, message: str, *args ):
        self.log( "info", self.c.GREEN, message, Logger.Level.INFORMATION, *args );

    def warn( self, message: str, *args ):
        self.log( "warning", self.c.YELLOW, message, Logger.Level.WARNING, *args );

    def trace( self, message: str, *args ):
        self.log( "trace", self.c.YELLOW, message, Logger.Level.TRACE, *args );

    def error( self, message: str, *args, Exit:bool = False ):
        self.log( "error", self.c.RED, message, Logger.Level.ERROR, *args );
        if Exit:
            exit(1);

    def critical( self, message: str, *args, Exit:bool = False ):
        self.log( "error", self.c.RED, message, Logger.Level.CRITICAL, *args );
        if Exit:
            exit(1);
