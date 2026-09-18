cmake_minimum_required(VERSION 3.18)
project(c2ui_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Python interpreter of the C2UI venv (pass -DPython_EXECUTABLE=<...>/.venv/Scripts/python.exe)
find_package(Python 3.10 COMPONENTS Interpreter Development.Module REQUIRED)

# pybind11: use the pip package if present (pip install pybind11), else FetchContent.
execute_process(
    COMMAND "${Python_EXECUTABLE}" -c "import pybind11, sys; sys.stdout.write(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _pybind11_dir ERROR_QUIET)
if(_pybind11_dir)
    list(APPEND CMAKE_PREFIX_PATH "${_pybind11_dir}")
    find_package(pybind11 CONFIG REQUIRED)
else()
    include(FetchContent)
    FetchContent_Declare(pybind11 GIT_REPOSITORY https://github.com/pybind/pybind11.git GIT_TAG v2.13.6)
    FetchContent_MakeAvailable(pybind11)
endif()

pybind11_add_module(c2ui_native c2ui_native.cpp)
target_compile_definitions(c2ui_native PRIVATE UNICODE _UNICODE)
if(MSVC)
    target_compile_options(c2ui_native PRIVATE /W4 /utf-8)
endif()

# Install next to the loader so `import c2ui_native` works from Core/API.
install(TARGETS c2ui_native LIBRARY DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/.." )
set_target_properties(c2ui_native PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/.."
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/.."
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/..")
