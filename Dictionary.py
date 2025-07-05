class Dictionary:

    '''
        Dictionary is basically a dict which automatically creates sub-Dictionary classes when accessing to their values by **__getattr__** or either **__getitem__**

        This is useful when you need a dictionary and want to modify a deep-value in the memory without having to access, access, access, set, store, store store x[
    '''

    def __init__( self, parent=None, key=None ) -> None:
        self.__dict__[ "_data" ] = {}
        self.__dict__[ "_parent" ] = parent
        self.__dict__[ "_key" ] = key

    def IsPrivate( self, name: str ) -> bool:
        return ( name in ( '_data', '_parent', '_key' ) );

    def __getattr__( self, name ) -> "Dictionary":

        if self.IsPrivate( name ):
        #
            raise AttributeError(f"Access to {name} not allowed" );
        #
        if name not in self._data:
        #
            self._data[ name ] = Dictionary( self, name );
        #
        return self._data[ name ];

    def __setattr__(self, name, value) -> None:

        if self.IsPrivate( name ):
        #
            raise AttributeError(f"Access to {name} not allowed" );
        #
        elif isinstance(value, dict):
        #
            node = Dictionary(self, name)
            node._data = {k: self._wrap_value(k, v) for k, v in value.items()}
            self._data[name] = node
        #
        else:
        #
            self._data[name] = value
        #

    def __getitem__(self, key) -> "Dictionary":
        return self.__getattr__(key)

    def __setitem__(self, key, value) -> None:
        return self.__setattr__(key, value)

    def _wrap_value(self, key, value):
        
        if isinstance(value, dict):
        #
            node = Dictionary(self, key)
            node._data = {k: self._wrap_value(k, v) for k, v in value.items()}
            return node
        #
        return value

    def serialize( self, value ) -> dict:
        if isinstance( value, Dictionary ):
        #
            return value.ToDict;
        #
        return value

    @property
    def ToDict( self ) -> dict:
        '''Return a dict object'''
        return { k: self.Serialize(v) for k, v in self._data.items() }

    @property
    def ToJson( self ) -> str:
        '''Return a json serialized string'''
        from json import dumps;
        return dumps( self.ToDict, indent=4 );
