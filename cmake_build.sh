#!/bin/bash

# Pass all arguments to the cmake command as additional -D flags
HPX_DIR=~/HPX/install/ cmake -G Ninja -S src/ -B build/ -D "CMAKE_INSTALL_PREFIX=install/" -D "CMAKE_BUILD_TYPE=Release" "$@"

# Run the cmake --build command and store the exit code
cmake --build ./build/
build_exit_code=$?

# Check if the exit code is 0 (indicating success)
if [ $build_exit_code -eq 0 ]; then
  # Build was successful, so run the cmake --install command
  cmake --install ./build/
else
  # Build was not successful, so print an error message and exit
  echo "Build failed with exit code $build_exit_code"
  exit 1
fi
