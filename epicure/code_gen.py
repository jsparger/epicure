from string import Template

def generate_method_service_classes(target):
    code = Template(
    '''
    struct ${class}_${method}_ServiceImpl : public RPCService {
        ${result_structure}
        ${request_method}
    };
    '''
    )

    classes = [];
    for method in target["methods"].values():
        subs = {
            "class": target["name"],
            "method": method["name"],
            "request_method": generate_request_method(method),
            "result_structure": generate_result_structure(method),
        }
        classes.append(code.substitute(**subs))
    return "".join(classes)

def generate_request_method(method):
    code = Template(
    '''
    PVStructure::shared_pointer request(PVStructure::shared_pointer const & pvArguments) {
        // NTURI support
        PVStructure::shared_pointer args(
            (starts_with(pvArguments->getStructure()->getID(), "epics:nt/NTURI:1.")) ?
            pvArguments->getSubField<PVStructure>("query") :
            pvArguments
        );

        ${get_fields}

        // create a return structure and set data
        ${get_result}
    }
    '''
    )
    subs = {
        "get_fields": generate_field_retrieval(method),
        "get_result": generate_result_retrieval(method),
    }
    return code.substitute(**subs)

def generate_field_retrieval(method):
    code = Template(
    '''
    // get fields and check their existence
    PVScalar::shared_pointer ${name}_f = args->getSubField<PVScalar>("${name}");
    if (!${name}_f) {
        throw RPCRequestException(Status::STATUSTYPE_ERROR, "scalar '${name}' field is required");
    }

    // get the numbers (and convert if neccessary)
    ${type} ${name};
    try {
        ${name} = ${name}_f->getAs<${type}>();
    }
    catch (std::exception &e) {
        throw RPCRequestException(Status::STATUSTYPE_ERROR,
            std::string("failed to convert argument named ${name} to ${type}: ") + e.what());
    }
    '''
    )
    fields = [code.substitute(**arg) for arg in method["args"]]
    return "".join(fields)

def generate_result_retrieval(method):
    code = Template(
    '''
    // create return structure and set data
    PVStructure::shared_pointer result = getPVDataCreate()->createPVStructure(this->resultStructure);
    result->getSubField<PVScalar<${return_type}>>("r")->put(this->target->${method}(${args}));
    return result;
    '''
    )
    subs = {
        "return_type": method["return"],
        "method": method["name"],
        "args": ",".join([arg["name"] for arg in method["args"]]),
    }
    return code.substitute(**subs)

def generate_result_structure(method):
    code = '''
    Structure::const_shared_pointer resultStructure =
        getFieldCreate()->createFieldBuilder()->
        add("c", PVScalar<{return}>)->
        createStructure();
    '''.format(**method)
    return code
