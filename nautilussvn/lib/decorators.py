#
# This is an extension to the Nautilus file manager to allow better 
# integration with the Subversion source control system.
# 
# Copyright (C) 2006-2008 by Jason Field <jason@jasonfield.com>
# Copyright (C) 2007-2008 by Bruce van der Kooij <brucevdkooij@gmail.com>
# Copyright (C) 2008-2008 by Adam Plumb <adamplumb@gmail.com>
# 
# NautilusSvn is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# NautilusSvn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with NautilusSvn;  If not, see <http://www.gnu.org/licenses/>.
#

"""

Simple decorators (usable in Python >= 2.4).

Decorators should be named as verbs (present or paste tense).

See: 

  - https://linkchecker.svn.sourceforge.net/svnroot/linkchecker/trunk/linkchecker/linkcheck/decorators.py
  - http://wiki.python.org/moin/PythonDecoratorLibrary
  
"""

import time
import warnings

from nautilussvn.lib.log import Log
log = Log("nautilussvn.lib.decorators")


import gtk

def update_func_meta(fake_func, real_func):
    """
    Set meta information (eg. __doc__) of fake function to that of the real 
    function.
    
    @rtype: function
    @return Fake function with metadata of the real function.
    """
    
    fake_func.__module__ = real_func.__module__
    fake_func.__name__ = real_func.__name__
    fake_func.__doc__ = real_func.__doc__
    fake_func.__dict__.update(real_func.__dict__)
    
    return fake_func

def deprecated(func):
    """
    A decorator which can be used to mark functions as deprecated.
    It emits a warning when the function is called.
    
    @type   func: function
    @param  func: The function to be designated as deprecated.
    """
    
    def newfunc(*args, **kwargs):
        """
        Print deprecated warning and execute original function.
        """
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
        
    return update_func_meta(newfunc, func)
    
def timeit(func):
    """
    This is a decorator which times a function and prints the time it took in
    milliseconds to stdout.
    
    Based on the timeit function from LinkChecker.
    
    @type   func: function
    @param  func: The function to be timed.
    
    """

    def newfunc(*args, **kwargs):
        """Execute function and print execution time."""
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start_time) * 1000.0
        log.info("%s() took %0.4f milliseconds" % (func.__name__, duration))
        return result
        
    return update_func_meta(newfunc, func)

def disable(func):
    """
    Disable a function.
    
    @type   func: function
    @param  func: The function to be disabled.
    
    """

    def newfunc(*args, **kwargs):
        return
        
    return update_func_meta(newfunc, func)

def gtk_unsafe(func):
    """
    Used to wrap a function that makes calls to GTK from a thread in
    gtk.gdk.threads_enter() and gtk.gdk.threads_leave().
    
    """
    
    def newfunc(*args, **kwargs):
        gtk.gdk.threads_enter()
        result = func(*args, **kwargs)
        gtk.gdk.threads_leave()
        return result
        
    return update_func_meta(newfunc, func)
