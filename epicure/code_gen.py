from string import Template

def generate_service_class(target):
    code = Template(
    '''
    struct ${name}ServiceImpl : public RPCService {
        ${result_structures}
        ${request_method}
    };
    '''
    )
    subs = {
        "name": target["name"],
        "request_method": generate_request_method(target),
        "result_structures": generate_all_result_structures(target),
    }
    return code.substitute(**subs)

def generate_request_method(target):
    code = Template(
    '''
    PVStructure::shared_pointer request(PVStructure::shared_pointer const & pvArguments) {
        ${}
    }
    '''
    )
    #TODO

def generate_all_result_structures(target):
    code = "".join(
        [generate_method_result_structure(method) for method in target.methods]
    )
    return code

def generate_method_result_structure(method):
    code = '''
    Structure::const_shared_pointer {name}_ResultStructure =
        getFieldCreate()->createFieldBuilder()->
        add("c", PVScalar<{return}>)->
        createStructure();
    '''.format(**method)
    return code
