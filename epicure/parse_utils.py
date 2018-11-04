import clang.cindex
from clang.cindex import CursorKind, TypeKind

def is_call_to_publish(node):
    '''Check if the node (cursor) is an invocation of the magical publish funciton'''
    #TODO: WATCH OUT FOR THIS. NEED A MUCH BETTER CHECK.
    return node.type.kind == TypeKind.FUNCTIONPROTO and node.spelling == "publish"

def find_all_published_type_definitions(cursor):
    '''Returns a list of cursors to the definitions of all types used as
    template arguments to the publish function.'''
    definitions = []
    for node in cursor.walk_preorder():
        if is_call_to_publish(node):
            # As far as I can tell, calls to template functions look like regular functions but have records as children.
            for child in node.get_children():
                if child.type.kind == TypeKind.RECORD:
                    d = child.get_definition()
                    if d.kind in [CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL]:
                        definitions.append(d)
    return definitions

def describe_methods(definition_cursor):
    methods = {}
    for node in definition_cursor.walk_preorder():
        if node.kind == CursorKind.CXX_METHOD:
            methods[node.spelling] = {
                "args": [{"name": arg.spelling, "type": arg.type.spelling} for arg in node.get_arguments()],
                "return": node.result_type.spelling,
            }
    return methods
