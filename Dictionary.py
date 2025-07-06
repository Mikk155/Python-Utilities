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

class __DictionaryList__( list ):

    '''Auxiliary class for Dictionary. do not use.'''

    def __init__( self, iterable=None, *, parent=None, key=None ):
    #
        super().__init__( iterable if iterable is not None else [] );
        self._parent = parent;
        self._key = key;
    #

    @property
    def __TryCallback__( self ):
    #
        p = self._parent;

        while p is not None and hasattr( p, "Parent" ):
        #
            if p.Parent is None:
            #
                break;
            #
            p = p.Parent;
        #

        if p and hasattr( p, "fnCallback" ) and p.fnCallback is not None:
        #
            p.fnCallback();
        #
    #

    def append( self, item ):
    #
        super().append(item);
        self.__TryCallback__;
    #

    def extend( self, iterable ):
    #
        super().extend(iterable );
        self.__TryCallback__;
    #

    def insert( self, index, item ):
    #
        super().insert(index, item);
        self.__TryCallback__;
    #

    def remove( self, item ):
    #
        super().remove(item);
        self.__TryCallback__;
    #

    def pop( self, index=-1 ):
    #
        item = super().pop(index);
        self.__TryCallback__;
        return item;
    #

    def clear( self ):
    #
        super().clear();
        self.__TryCallback__;
    #

    def __setitem__( self, index, value ):
    #
        super().__setitem__(index, value );
        self.__TryCallback__;
    #

    def __delitem__( self, index):
    #
        super().__delitem__(index);
        self.__TryCallback__;
    #

class Dictionary:

    '''
        Dictionary is basically a dict which automatically creates sub-Dictionary classes when accessing to their values.

        This is useful when you need a dictionary and want to modify a deep-value in the memory without having to access, access, access, set, store, store store x[
    '''

    def __init__( self, *, fnCallback=None, parent=None, key=None ) -> None:
    #
        '''
            fnCallback: function to call after the Dictionary or its childs have been updated.

            parent and key are reserved for internal operations and should never be used.
        '''
        self.__dict__[ "_data" ] = {}
        self.__dict__[ "_parent" ] = parent
        self.__dict__[ "_key" ] = key
        self.fnCallback = fnCallback;
    #

    def __getitem__( self, name ) -> "Dictionary":
    #
        if name not in self._data:
        #
            _Dictionary = Dictionary( parent=self, key=name );
            self._data[ name ] = _Dictionary;
            return _Dictionary;
        #
        return self._data[ name ];
    #

    def __setitem__( self, name, value ) -> None:
    #
        if isinstance( name, int | float ):
            name = str(name);

        assert isinstance( name, str ), "Key names must be only str!";

        if isinstance( value, dict ):
        #
            _Dictionary = Dictionary( parent=self, key=name );
            _Dictionary._data = { k: self._wrap_value(k, v) for k, v in value.items() };
            self._data[name] = _Dictionary;
        #
        elif isinstance( value, list ):
        #
            self._data[name] = __DictionaryList__( value, parent=self, key=name );
        #
        else:
        #
            self._data[name] = value;
        #

        self.__TryCallback__;
    #

    def _wrap_value( self, key, value ):
    #
        if isinstance( value, dict ):
        #
            _Dictionary = Dictionary( parent=self, key=key );
            _Dictionary._data = { k: self._wrap_value(k, v) for k, v in value.items() };
            return _Dictionary;
        #
        elif isinstance( value, list | tuple ):
        #
            _Dictionary = __DictionaryList__( value, parent=self, key=key );
            return _Dictionary;
        #
        return value;
    #

    def __repr__( self ) -> str:
    #
        return self.ToJson( None );
    #

    def __str__( self ) -> str:
    #
        return self.ToJson( None );
    #

    def pop( self, name: str ) -> None:
    #
        if name in self._data:
        #
            self._data.pop( name );
            self.__TryCallback__;
        #
    #

    def ToJson( self, indent: int = None ) -> str:
    #
        '''Return a json serialized string'''
        from json import dumps;
        return dumps( self.ToDict, indent=indent );
    #

    @property
    def Serialize( self ) -> str:
    #
        '''Return a json serialized string with indent on 4'''
        return self.ToJson( indent=4 );
    #

    @property
    def ToDict( self ) -> dict:
    #
        '''Return a dict object'''
        return { k: v.ToDict if isinstance( v, Dictionary ) else v for k, v in self._data.items() };
    #

    @property
    def IsEmpty( self ) -> bool:
    #
        '''Return whatever this Dictionary has just been created and is empty'''
        return len( self._data ) == 0;
    #

    @property
    def Parent( self ) -> "Dictionary":
    #
        '''Return this Dictionary's parent'''
        return self.__dict__[ "_parent" ];
    #

    @property
    def Leader( self ) -> "Dictionary":
    #
        '''Return the instance of the first Dictionary on the top'''

        pParent: Dictionary = self;
    
        while pParent.Parent is not None:
        #
            pParent = pParent.Parent;
        #

        return pParent;
    #

    @property
    def GetCallback( self ) -> None | object:
    #
        '''Get the parent's callback if any'''
        return self.Leader.fnCallback;
    #

    @property
    def __TryCallback__( self ) -> None:
    #
        '''fnCallback is automatically called when you set a item to any Dictionary or __DictionaryList__ in the family'''

        pCallback: None | object = self.GetCallback;

        if pCallback is not None:
        #
            pCallback();
        #
    #

    @property
    def ParentName( self ) -> str | None:
    #
        '''Return the name of this Dictionary's parent'''
        pParent: None | Dictionary = self.Parent;

        if pParent is not None:
        #
            pName: str | None = pParent.__dict__[ "_key" ];

            if pName is None:
            #
                return pParent.__class__; # A dictionary created outside of this context doesn't contains _key
            #
            return pName;
        #
        return None;
    #

    @classmethod
    def FromDict( cls, data: dict, *, fnCallback=None, parent=None, key=None ) -> "Dictionary":
    #
        '''Create a Dictionary by a given dict'''

        obj = cls( fnCallback=fnCallback, parent=parent, key=key )

        for k, v in data.items():
        #
            obj._data[k] = obj._wrap_value(k, v)
        #
        return obj
    #
