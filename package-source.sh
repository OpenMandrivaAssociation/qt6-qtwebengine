#!/bin/sh
if [ -n "$1" ]; then
	CHROMIUM="$1"
else
	CHROMIUM=122
fi
rm -rf qtwebengine qtwebengine-chromium
D="$(date +%Y%m%d)"
git clone -b dev --depth 1 git://code.qt.io/qt/qtwebengine.git
cd qtwebengine
git archive -o ../qtwebengine-everywhere-src-6.8-$D.tar --prefix qtwebengine-everywhere-src-6.8-$D/ origin/dev
cd ..
git clone -b ${CHROMIUM}-based --depth 1 git://code.qt.io/qt/qtwebengine-chromium.git
cd qtwebengine-chromium
git archive -o ../qtwebengine-chromium-${CHROMIUM}-$D.tar origin/${CHROMIUM}-based
cd ..
zstd --ultra -22 --rm *.tar
