""" 
    Example that demonstrates several ways of defining your own columns.
"""
from __future__ import print_function

import sys, logging
from math import sqrt
from PySide.QtCore import Qt

from objbrowser import browse, logging_basic_config
from objbrowser.attribute_model import (AttributeModel, DEFAULT_ATTR_COLS, 
                                        safe_tio_call, safe_data_fn)

logger = logging.getLogger(__name__)

   
def safe_tio_sqrt(tree_item):
    """ Calls math.sqrt(tree_item.obj) and converts the result to a string. 
        Returns empty string in case the sqrt cannot be calculated.
    """ 
    tio = tree_item.obj
    try:
        return str(sqrt(tio))
    except StandardError:
        return ""
    
        
def main():
    """ Main program 
    """
    logging_basic_config('DEBUG')
    logger.info('Started example')
    
    doc_str = "The sqrt of an object if it can be calculated"
    width = 120 # pixels
    
    # 1: The data_fn should be a TreeItem to string function. If you have a function 
    #    with one input and one output parameter (e.g. the sqrt function), you must wrap
    #    it with a lambda expression like this.
    sqrt_attr_model_1 = AttributeModel('sqrt 1', 
        doc         = doc_str, 
        data_fn     = lambda(tree_item): str(sqrt(tree_item.obj)),
        col_visible = True,
        width       = width,   
        alignment   = Qt.AlignRight) 

    # 2) Example 1 above displays an error message in the cell in case of an exception.
    #    To prevent this you can wrap the function in another function that returns an 
    #    empty string in case of an exception.
    sqrt_attr_model_2 = AttributeModel('sqrt 2', 
        doc         = doc_str, 
        data_fn     = safe_tio_sqrt,
        col_visible = True,
        width       = width,   
        alignment   = Qt.AlignRight) 

    # 3) The save_tio_call function does the wrapping for you but you still need to use
    #    a lambda expression.
    sqrt_attr_model_3 = AttributeModel('sqrt 3', 
        doc         = doc_str, 
        data_fn     = lambda(tree_item): safe_tio_call(sqrt, tree_item),
        col_visible = True,
        width       = width,   
        alignment   = Qt.AlignRight) 

    # 4) The simplest solution is to use the safe_data_fn function which creates the
    #    wrapped function.
    sqrt_attr_model_4 = AttributeModel('sqrt 3', 
        doc         = doc_str, 
        data_fn     = safe_data_fn(sqrt),
        col_visible = True,
        width       = width,   
        alignment   = Qt.AlignRight) 

    attribute_columns = list(DEFAULT_ATTR_COLS)
    attribute_columns.insert(5, sqrt_attr_model_1)
    attribute_columns.insert(6, sqrt_attr_model_2)
    attribute_columns.insert(7, sqrt_attr_model_3)
    attribute_columns.insert(8, sqrt_attr_model_4)
    
    objects = dict(
        #attribute_columns = attribute_columns,
        lst = range(-5, 5), 
        b = True, 
        i = 555, 
        f = 6.2, 
        c = 3.2j - 0.1,
        m = -4, 
        n = None,
        s = '44',
        z = 'zonk')
        
    exit_code = browse(objects,  
                       attribute_columns = attribute_columns, 
                       show_routine_attributes=False,
                       show_special_attributes=False)

    logging.info('Done example')
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
    