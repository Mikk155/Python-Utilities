from colorama import init as colorama
global colorama_init;
colorama_init: bool = False;

class LoggerLevel:

    AllLoggers = -1;
    Critical: int = ( 1 << 0 ); # critical is ignored and will always being enable
    Error: int = ( 1 << 1 ); # The same for error
    Warning: int = ( 1 << 2 );
    Information: int = ( 1 << 3 );
    Debug: int = ( 1 << 4 );
    Trace: int = ( 1 << 5 );

global GlobalLoggerLevel;
GlobalLoggerLevel = ( LoggerLevel.Information | LoggerLevel.Warning );

def LoggerToggleLevel( level: LoggerLevel ):
    global GlobalLoggerLevel;
    if GlobalLoggerLevel & level:
        GlobalLoggerLevel &= level;
    else:
        GlobalLoggerLevel |= level;

def LoggerSetLevel( level: LoggerLevel ):
    global GlobalLoggerLevel;
    if not GlobalLoggerLevel & level:
        GlobalLoggerLevel |= level;

def LoggerClearLevel( level: LoggerLevel ):
    global GlobalLoggerLevel;
    if GlobalLoggerLevel & level:
        GlobalLoggerLevel &= level;

class Logger():

    name: str;

    level: int = LoggerLevel.AllLoggers;

    def ToggleLevel( self, level: LoggerLevel ):
        if self.level & level:
            self.level &= level;
        else:
            self.level |= level;

    def SetLevel( self, level: LoggerLevel ):
        if not self.level & level:
            self.level |= level;

    def ClearLevel( self, level: LoggerLevel ):
        if self.level & level:
            self.level &= level;

    def __init__( self, name: str ):

        global colorama_init;
        if not colorama_init:
            colorama();
            colorama_init = True;

        self.name = name;

    from colorama import Fore as c;

    def log( self, levelname: str, color: str, message: str, level: LoggerLevel, *args ) -> str:

        if level != LoggerLevel.Critical or level != LoggerLevel.Error:

            LevelsCheck = ( GlobalLoggerLevel, self.level );

            for LevelCheck in LevelsCheck:

                if LevelCheck != LoggerLevel.AllLoggers:

                    if not LevelCheck & level:
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
        self.log( "debug", self.c.CYAN, message, LoggerLevel.Debug, *args );

    def info( self, message: str, *args ):
        self.log( "info", self.c.GREEN, message, LoggerLevel.Information, *args );

    def warn( self, message: str, *args ):
        self.log( "warning", self.c.YELLOW, message, LoggerLevel.Warning, *args );

    def trace( self, message: str, *args ):
        self.log( "trace", self.c.YELLOW, message, LoggerLevel.Trace, *args );

    def error( self, message: str, *args, Exit:bool = False ):
        self.log( "error", self.c.RED, message, LoggerLevel.Error, *args );
        if Exit:
            exit(1);

    def critical( self, message: str, *args, Exit:bool = False ):
        self.log( "error", self.c.RED, message, LoggerLevel.Critical, *args );
        if Exit:
            exit(1);
