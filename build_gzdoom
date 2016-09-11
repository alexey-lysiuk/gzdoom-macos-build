#!/bin/sh

set -o errexit

cd "`dirname \"$0\"`/"

ROOT_DIR=`pwd`/
BUILD_DIR=${ROOT_DIR}build/
DIST_DIR=${ROOT_DIR}dist/
LIBS_DIR=${ROOT_DIR}libs/
TP_DIR=${ROOT_DIR}thirdparty/
SYSROOT_DIR=${TP_DIR}macos/MacOSX10.7.sdk
FMOD_DIR=${TP_DIR}fmodex/

export PATH="${LIBS_DIR}bin:${PATH}"
export CFLAGS="-I${LIBS_DIR}include -mmacosx-version-min=10.7 -isysroot ${SYSROOT_DIR}"
export CPPFLAGS="-I${LIBS_DIR}include -mmacosx-version-min=10.7 -isysroot ${SYSROOT_DIR}"
export CXXFLAGS="-I${LIBS_DIR}include -mmacosx-version-min=10.7 -isysroot ${SYSROOT_DIR}"
export LDFLAGS="-L${LIBS_DIR}lib -mmacosx-version-min=10.7 -isysroot ${SYSROOT_DIR}"

function mkcd {
	if [ ! -e $1 ]; then
		mkdir -p $1
	fi
	
	cd $1
}

function mklib {
	mkcd "${BUILD_DIR}$1"
	"${TP_DIR}$1/configure" --prefix="${LIBS_DIR}" --enable-static --disable-shared ${@:2}
	make install
}

mklib ogg
mklib vorbis
mklib flac
mklib mpg123
mklib pkg-config --with-internal-glib
mklib sndfile

mkcd "${BUILD_DIR}openal-soft"
"${TP_DIR}cmake/bin/cmake"               \
	-DCMAKE_INSTALL_PREFIX="${LIBS_DIR}" \
	-DCMAKE_OSX_DEPLOYMENT_TARGET="10.7" \
 	-DCMAKE_OSX_SYSROOT="${SYSROOT_DIR}" \
 	-DLIBTYPE="STATIC"                   \
	-DALSOFT_CPUEXT_SSE4_1="NO"          \
	${TP_DIR}openal-soft
make install

cd "${ROOT_DIR}"

if [ ! -e gzdoom ]; then
	git clone https://github.com/coelckers/gzdoom.git
else
	cd gzdoom
	git pull
fi

CMAKE_EXE_LINKER_FLAGS=-L${LIBS_DIR}/lib\ -logg\ -lvorbis\ -lvorbisenc\ -lFLAC

mkcd "${BUILD_DIR}gzdoom"
"${TP_DIR}cmake/bin/cmake"                               \
	-DCMAKE_PREFIX_PATH="${LIBS_DIR}"                    \
	-DCMAKE_OSX_DEPLOYMENT_TARGET="10.7"                 \
	-DCMAKE_OSX_SYSROOT="${SYSROOT_DIR}"                 \
	-DCMAKE_EXE_LINKER_FLAGS="${CMAKE_EXE_LINKER_FLAGS}" \
	-DFMOD_INCLUDE_DIR=${FMOD_DIR}inc                    \
	-DFMOD_LIBRARY=${FMOD_DIR}lib/libfmodex.dylib        \
	-DDYN_OPENAL=NO                                      \
	"${ROOT_DIR}gzdoom"
make

if [ -e "${DIST_DIR}" ]; then
	rm -r "${DIST_DIR}"
fi

mkdir "${DIST_DIR}"
cp -R gzdoom.app "${DIST_DIR}GZDoom.app"
cp -R "${ROOT_DIR}gzdoom/docs" "${DIST_DIR}Docs"
ln -s /Applications "${DIST_DIR}/Applications"

cd "${ROOT_DIR}gzdoom"
DMG_NAME=GZDoom-`git describe --tags`
DMG_PATH=${ROOT_DIR}/${DMG_NAME}.dmg

if [ -e "${DMG_PATH}" ]; then
	rm "${DMG_PATH}"
fi

hdiutil create -srcfolder "${DIST_DIR}" -volname "${DMG_NAME}" \
	-format UDBZ -fs HFS+ -fsargs "-c c=64,a=16,e=16" "${DMG_PATH}"
