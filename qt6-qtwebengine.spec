%define beta rc
#define snapshot 20200627
%define major 6

# Until we can return to building with clang
%define _disable_lto 1

%define _qtdir %{_libdir}/qt%{major}

# Use this if you get "filename too long" errors:
# Workaround for filenames getting too long for ****ing gn to handle
#define _builddir /tmp/b

Name:		qt6-qtwebengine
Version:	6.10.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# Built with package-source.sh (Source1000)
Source:		qtwebengine-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
Source1:	qtwebengine-chromium-122-%{snapshot}.tar.zst
Source1000:	package-source.sh
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtwebengine-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Patch1:		qtwebengine-6.4.0b3-buildfixes.patch
Patch2:		qt6-qtwebengine-6.2.2-workaround-for-__fp16-build-failure-aarch64.patch
Patch3:		qtwebengine-ffmpeg-8.0.patch
Patch4:		qtwebengine-6.5.0-aarch64-compile.patch
#Patch5:		qtwebengine-6.9.0-gperf-3.2+.patch
Patch6:		qtwebengine-6.10.0-clang21.patch
Patch7:		qtwebengine-6.10-absl-25.08.patch
# Try to restore a sufficient amount of binary compatibility between the
# internalized copy of absl (which can't be disabled yet) and the system
# version (used, among others, by the system version of re2, which DOES
# get used...
#Patch5:		qtwebengine-re2-absl-compat.patch
# Patches 2000 to 3000 are applied to the builtin Chromium sources and
# should be kept in sync with the chromium package where applicable.
Patch2001:	https://sources.debian.org/data/main/c/chromium/124.0.6367.155-1/debian/patches/fixes/widevine-locations.patch
Patch2002:	https://raw.githubusercontent.com/OpenMandrivaAssociation/chromium/master/chromium-extra-widevine-search-paths.patch
Patch2003:	https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-107-proprietary-codecs.patch
Group:		System/Libraries
Summary:	Qt %{major} Web Engine - a web browser library for Qt
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Xml)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Sql)
BuildRequires:	cmake(Qt%{major}PrintSupport)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}OpenGLWidgets)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Positioning)
BuildRequires:	cmake(Qt%{major}WebChannel)
BuildRequires:	cmake(Qt%{major}WebChannelQuick)
BuildRequires:	cmake(Qt%{major}WebSockets)
BuildRequires:	cmake(Qt%{major}Test)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	cmake(Qt%{major}Designer)
BuildRequires:	cmake(Qt%{major}UiPlugin)
BuildRequires:	cmake(Qt%{major}Svg)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickControls2)
BuildRequires:	cmake(Qt%{major}QuickTemplates2)
BuildRequires:	cmake(Qt%{major}QuickWidgets)
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(dri)
BuildRequires:	git-core
BuildRequires:	atomic-devel
BuildRequires:	gn
BuildRequires:	gperf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(snappy)
BuildRequires:	nodejs
BuildRequires:	pkgconfig(cups)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libjxl)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xshmfence)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(nss) >= 3.26
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(glproto)
BuildRequires:	pkgconfig(glib-2.0) >= 2.32.0
BuildRequires:	pkgconfig(harfbuzz) >= 2.4.0
BuildRequires:	pkgconfig(harfbuzz-subset) >= 2.4.0
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(libpng) >= 1.6.0
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(re2)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libwebpmux)
BuildRequires:	pkgconfig(libwebpdemux)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(opus) >= 1.3.1
BuildRequires:	pkgconfig(vpx) >= 1.10.0
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libpulse-mainloop-glib)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(absl_config)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:	python3dist(html5lib)
BuildRequires:	qt6-qttools-designer
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
# FIXME switch to shared library (port patch from qt5)
BuildRequires:	stdc++-static-devel
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Web Engine - a web browser library for Qt

%package designer
Summary: Qt Designer integration for QtWebEngine
Group: Development/C
Requires: qt%{major}-qttools-designer
Supplements: qt%{major}-qttools-designer

%description designer
Qt Designer integration for QtWebEngine

%files designer
%{_qtdir}/plugins/designer/libqwebengineview.so
%{_qtdir}/lib/cmake/Qt6Designer/Qt6QWebEngineViewPlugin*.cmake

%global extra_files_WebEngineCore \
%{_qtdir}/libexec/webenginedriver \
%{_qtdir}/libexec/QtWebEngineProcess \
%dir %{_qtdir}/resources \
%{_qtdir}/resources/qtwebengine_devtools_resources.pak \
%{_qtdir}/resources/qtwebengine_resources.pak \
%{_qtdir}/resources/qtwebengine_resources_100p.pak \
%{_qtdir}/resources/qtwebengine_resources_200p.pak \
%{_qtdir}/resources/v8_context_snapshot.bin

%global extra_reqprov_WebEngineCore \
Requires: %{name} = %{EVRD}

%global extra_devel_files_WebEngineCore \
%{_qtdir}/lib/cmake/Qt6/FindGPerf.cmake \
%{_qtdir}/lib/cmake/Qt6/FindGn.cmake \
%{_qtdir}/lib/cmake/Qt6/FindNinja.cmake \
%{_qtdir}/lib/cmake/Qt6/FindNodejs.cmake \
%{_qtdir}/lib/cmake/Qt6/FindPkgConfigHost.cmake \
%{_qtdir}/lib/cmake/Qt6/FindSnappy.cmake \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtWebEngineTestsConfig.cmake \
%{_qtdir}/libexec/gn \
%{_qtdir}/libexec/qwebengine_convert_dict \
%{_qtdir}/sbom/*

%global extra_devel_reqprov_WebEngineCore \
Requires:	cmake(Qt%{major}Positioning)

%global extra_devel_reqprov_WebEngineWidgets \
Requires:	cmake(Qt%{major}QuickWidgets)

%global extra_devel_files_Pdf \
%{_qtdir}/lib/cmake/Qt6Gui/Qt6QPdfPlugin*.cmake

%global extra_devel_files_PdfQuick \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6PdfQuickplugin*.cmake

%global extra_files_WebEngineQuick \
%{_qtdir}/qml/QtWebEngine

%global extra_devel_files_WebEngineQuick \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6qtwebenginequickdelegatesplugin*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6qtwebenginequickplugin*.cmake

%global extra_files_Pdf \
%{_qtdir}/plugins/imageformats/libqpdf.so

%global extra_files_PdfQuick \
%{_qtdir}/qml/QtQuick/Pdf

%qt6libs WebEngineCore WebEngineQuick WebEngineWidgets WebEngineQuickDelegatesQml Pdf PdfQuick PdfWidgets

%prep
%setup -q -n qtwebengine%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%if 0%{?snapshot:1}
cd src/3rdparty
tar xf %{S:1}
cd ../..
%endif
%autopatch -p1 -M 999
cd src/3rdparty/chromium/media
%autopatch -p1 -m 1000 -M 1010
cd -
cd src/3rdparty/chromium
%autopatch -p1 -m 2000 -M 3000
cd -

# Until we can figure out how to kill the internal absl, let's at least
# try to make it ABI compatible with the system copy (as used by re2...)
cp -f %{_includedir}/absl/base/options.h src/3rdparty/chromium/third_party/abseil-cpp/absl/base/options.h
# Chromium isn't compatible with std::optional though
#sed -i -e 's,#define ABSL_OPTION_USE_STD_OPTIONAL 1,#define ABSL_OPTION_USE_STD_OPTIONAL 0,' src/3rdparty/chromium/third_party/abseil-cpp/absl/base/options.h

# FIXME We probably want
# -DFEATURE_webengine_system_libvpx:BOOL=ON
# but cmake claims it's incompatible with VAAPI
# Need to check if that's true and if necessary port
# related patches to system libvpx

%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DFEATURE_qtpdf_build:BOOL=ON \
	-DFEATURE_qtpdf_quick_build:BOOL=ON \
	-DFEATURE_qtpdf_widgets_build:BOOL=ON \
	-DFEATURE_pdf_v8:BOOL=ON \
	-DFEATURE_pdf_xfa:BOOL=ON \
	-DFEATURE_pdf_xfa_bmp:BOOL=ON \
	-DFEATURE_pdf_xfa_gif:BOOL=ON \
	-DFEATURE_pdf_xfa_png:BOOL=ON \
	-DFEATURE_pdf_xfa_tiff:BOOL=ON \
	-DFEATURE_webengine_proprietary_codecs:BOOL=ON \
	-DFEATURE_webengine_system_ffmpeg:BOOL=ON \
	-DFEATURE_webengine_system_icu:BOOL=ON \
	-DFEATURE_webengine_system_libevent:BOOL=ON \
	-DFEATURE_webengine_system_ninja:BOOL=ON \
	-DFEATURE_webengine_webrtc_pipewire:BOOL=ON \
	-DFEATURE_webengine_vaapi:BOOL=ON \
	-DFEATURE_webengine_vulkan:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build

for i in %{buildroot}%{_qtdir}/translations/qtwebengine_locales/*.pak; do
	l=$(basename $i .pak |sed -e 's,-,_,g')
	echo "%lang($l) %{_qtdir}/translations/qtwebengine_locales/$(basename $i)" >>qtwebengine.lang
done
%qt6_postinstall

%files -f qtwebengine.lang

%package examples
Summary:	Sample code demonstrating the use of %{name}
Group:		Development/KDE and Qt

%description examples
Sample code demonstrating the use of %{name}

%files examples
%{_qtdir}/examples/webenginequick
%{_qtdir}/examples/webenginewidgets
%{_qtdir}/examples/pdf
%{_qtdir}/examples/pdfwidgets
