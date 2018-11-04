


auto rpc_from_class = epicure::make_rpc<MyDeviceClass>(a, b, c);
auto rpc_from_lambda = epicure::make_rpc([](a,b,c) {/*code*/});

std::unique_ptr<MyDeviceClass> device_only = epicure::release(std::move(rpc_from_class));
