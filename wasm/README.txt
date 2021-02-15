webassembly/ wasm:

    references:
        https://emscripten.org/docs/getting_started/downloads.html
        https://levelup.gitconnected.com/a-hands-on-introduction-to-webassembly-with-go-959babb58109
        https://www.jamesfmackenzie.com/2019/11/30/whats-is-webassembly-hello-world/
        https://wasmbyexample.dev/examples/hello-world/hello-world.c.en-us.html

    install emscripten:
        git clone https://github.com/emscripten-core/emsdk.git
        cd emsdk/
        ./emsdk install latest
        ./emsdk activate latest
        source ./emsdk_env.sh

    compile:
        emcc hello.c -o hello.js
        emcc hello.c -o hello.html
        
    run node.js:
        node hello.js

    run browser:
        python -m http.server 8000
        http://localhost:8000/hello.html        

    disassembly:
        git clone --recursive https://github.com/WebAssembly/wabt
        cd wabt/; mkdir build; cd build; cmake ..; cmake --build .
        wasm2wat ../../hello.wasm --no-debug-names 


