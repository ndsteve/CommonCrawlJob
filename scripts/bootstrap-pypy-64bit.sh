#!/usr/bin/env bash
set -ev

# Install pypy on AWS EMR

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64 LD_RUN_PATH=${LD_RUN_PATH}:/usr/lib64
readonly LIBFFI=libffi-3.2.1 PYPY_RELEASE="release-pypy2.7-v5.3"

sudo yum update -y && sudo yum install -y \
    gcc make python27-devel libffi-devel lib-sqlite3-devel pkgconfig \
    zlib-devel bzip2-devel ncurses-devel expat-devel \
    openssl-devel gc-devel python27-sphinx python27-greenlet tcl-devel

# Install LibFFI
curl "ftp://sourceware.org/pub/libffi/${LIBFFI}.tar.gz" | tar -xzf- && pushd "${LIBFFI}"
    ./configure --prefix=/usr && make && sudo make install
popd

# Install PyPy
mkdir -p /home/hadoop/pypy
curl "https://bitbucket.org/pypy/pypy/get/${PYPY_RELEASE}.tar.gz" | tar -xz
cd pypy*
make

