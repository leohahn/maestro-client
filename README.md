maestro-client
==============

maestro-client is [maestro's](https://github.com/topfreegames/maestro) framework that should be included in game rooms

## Dependencies
  * [restclient-cpp](https://github.com/mrtazz/restclient-cpp)
  * [boost](http://www.boost.org/)
  * [cmake](https://cmake.org) for generating the Makefiles
  * C++11 or newer for building

## Building
You can generate a project using cmake. The library itself depends on Boost format and restclient-cpp, which depends on libcurl. In order to make the build process easier, the lib includes a precompiled restclient-cpp lib (for MacOS and Linux) in the repository. By passing the variable `CMAKE_PREFIX_PATH`, you can tell CMake where the library is located. For example, building a shared library for MacOS can be done with the following command:

```bash
cmake -H. -B_builds/mac                              \ # output build artifacts to _builds/mac
      -DCMAKE_BUILD_TYPE=Release                     \ # release build
      -DCMAKE_PREFIX_PATH=../deps/restclient-cpp/mac \ # restclient-cpp location in relation to the build folder

cmake --build _builds/mac # build the project
```

The previous command will try to find boost and libcurl on your system. In order to build the library without shared dependencies (outside of things like `libc++`) you can install curl using `conan`. The process should be something like the following:

```bash
pip install conan # install conan if you dont have it
conan install . -if _builds/mac # install dependencies in the _builds/mac folder
cmake -H. -B_builds/mac -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=../deps/restclient-cpp/mac
cmake --build _builds/mac
```

You can then check this using `otool` on MacOS or `ldd` if built for Linux:
```bash
$ otool -L _builds/mac/lib/libmaestro.dylib
_builds/mac/lib/libmaestro.dylib:
        libmaestro.dylib (compatibility version 0.0.0, current version 0.0.0)
        /System/Library/Frameworks/Cocoa.framework/Versions/A/Cocoa (compatibility version 1.0.0, current version 23.0.0)
        /System/Library/Frameworks/Security.framework/Versions/A/Security (compatibility version 1.0.0, current version 58286.200.222)
        /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 400.9.4)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1252.200.5)
        /System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation (compatibility version 150.0.0, current version 1555.10.0)

```

The binaries should then be located at `lib/libmaestro-client.dylib` and `bin/example` in the build folder.

The process for building on linux is the same as the previous one, but you have to point to the correct `restclient-cpp`, changing the path:

```bash
# Building for linux (the conan step is optional)
conan install . -if _builds/linux
cmake -H. -B_builds/linux -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=../deps/restclient-cpp/linux
cmake --build _builds/linux
```

### Docker image to build for linux
There's also a docker image available to build the lib and the room-example for linux if you are running OS X for example or simply don't want to install the dependencies to compile or haven't got it to work, use it like that:
```
$ docker run -v $(pwd):/app-src -it quay.io/tfgco/maestro-example-builder:v2.0.0
## inside the container
$ conan install . -if _builds/linux
$ cmake -H. -B_builds/linux -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=../deps/restclient-cpp/linux
$ cmake --build _builds/linux
```
building the image for the builder:
```
docker build -f Dockerfile-builder -t maestro-example-builder .
```
exit from the container and, as before, if everything went well then, the ouput files should be at at ```_builds/linux/lib/libmaestro-client.a``` and ```_builds/linux/bin/example``` but will only work on linux.

## How to integrate maestro in your game room

### Unity instructions
* Include the files in folder maestro-unity into your Assets folder
* Initialize maestro like: MaestroClient.Initialize ("http://localhost:5000"); //change localhost:5000 for a real maestro api url
* You will have to keep calling the following methods to report the room's status to maestro:
  - RoomReady() //Every time the room is ready to receive new players, e.g. on the init or when a match has just ended
  - RoomOccupied() //When a match is happenning on this room
  - RoomTerminated() //When a room is to die (your room must die gracefully, you must catch SIGKILL and SIGTERM status and only let the room die when Maestro::RoomTerminated is called)
  - RoomTerminatind() //This should be the first method you call when the room is to die, it's to be called when a gracefull shutdown will occur
* You should also call Ping() method periodically, so that maestro knows that your room server is alive. Call it for example every 30 seconds after the first RoomReady (on room initialization)

### C++ instructions
* Same as unity, using the c++ sources inside cpplib directly or compiling the shared library with the instructions above.

## Release Map

* ### Milestone 1

- [ ] maestro-client
    - [ ] docs
    - [x] fake http server
    - [x] configuration (maestro url / ping interval)
    - [x] http client
    - [x] polling to retrieve (host / port)
    - [ ] deal with connection errors
    - [x] catch sigterm/sigkill and handle graceful shutdown
    - [x] unity support
    - [ ] tests
    - [x] error handling
