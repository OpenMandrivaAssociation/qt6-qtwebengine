#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtwebengine
Version:	6.2.2
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtwebengine-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtwebengine-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Patch0:		qtwebengine-6.2.2-glibc-2.34.patch
Group:		System/Libraries
Summary:	Qt %{major} Quick Timeline plugin
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	qt%{major}-qtdeclarative-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# FIXME this is ridiculous and really really needs to go
BuildRequires:	python2
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Quick timeline plugin

%define libs WebEngineCore WebEngineQuick WebEngineWidgets WebEngineQuickDelegatesQml
%{expand:%(for lib in %{libs}; do
	cat <<EOF
%%global lib${lib} %%mklibname Qt%{major}${lib} %{major}
%%global dev${lib} %%mklibname -d Qt%{major}${lib}
%%package -n %%{lib${lib}}
Summary: Qt %{major} ${lib} library
Group: System/Libraries

%%description -n %%{lib${lib}}
Qt %{major} ${lib} library

%%files -n %%{lib${lib}}
%{_qtdir}/lib/libQt%{major}${lib}.so.*
%{_libdir}/libQt%{major}${lib}.so.*

%%package -n %%{dev${lib}}
Summary: Development files for the Qt %{major} ${lib} library
Requires: %%{lib${lib}} = %{EVRD}
Group: Development/KDE and Qt

%%description -n %%{dev${lib}}
Development files for the Qt %{major} ${lib} library

%%files -n %%{dev${lib}}
%{_qtdir}/lib/libQt%{major}${lib}.so
%{_libdir}/libQt%{major}${lib}.so
%{_qtdir}/lib/libQt%{major}${lib}.prl
%optional %{_qtdir}/include/Qt${lib}
%optional %{_qtdir}/modules/${lib}.json
%optional %{_qtdir}/modules/${lib}Private.json
%optional %{_libdir}/cmake/Qt%{major}${lib}
%optional %{_libdir}/cmake/Qt%{major}${lib}Private
%optional %{_qtdir}/lib/cmake/Qt%{major}${lib}
%optional %{_qtdir}/lib/metatypes/qt%{major}$(echo ${lib}|tr A-Z a-z)_relwithdebinfo_metatypes.json
%optional %{_qtdir}/lib/metatypes/qt%{major}$(echo ${lib}|tr A-Z a-z)private_relwithdebinfo_metatypes.json
%optional %{_qtdir}/mkspecs/modules/qt_lib_$(echo ${lib}|tr A-Z a-z).pri
%optional %{_qtdir}/mkspecs/modules/qt_lib_$(echo ${lib}|tr A-Z a-z)_private.pri
%optional %{_libdir}/cmake/Qt%{major}${lib}Tools
EOF

	if [ "${lib}" = "WebEngineQuick" ]; then
		cat <<EOF
%{_libdir}/cmake/Qt6/*.cmake
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebEngineTestsConfig.cmake
%{_libdir}/cmake/Qt6Designer/*.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtwebenginequickdelegatesplugin[A-Z]*.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtwebenginequickplugin[A-Z]*.cmake
EOF
	fi
done)}

%prep
%autosetup -p1 -n qtwebengine%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir}
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
        ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}

for i in %{buildroot}%{_qtdir}/translations/qtwebengine_locales/*.pak; do
	l=$(basename $i .pak |sed -e 's,-,_,g')
	echo "%lang($l) %{_qtdir}/translations/qtwebengine_locales/$(basename $i)" >>qtwebengine.lang
done

%files -f qtwebengine.lang
%{_qtdir}/libexec/QtWebEngineProcess
%{_qtdir}/libexec/gn
%{_qtdir}/libexec/qwebengine_convert_dict
%{_qtdir}/plugins/designer/libqwebengineview.so
%{_qtdir}/qml/QtWebEngine
%{_qtdir}/resources/icudtl.dat
%{_qtdir}/resources/qtwebengine_devtools_resources.pak
%{_qtdir}/resources/qtwebengine_resources.pak
%{_qtdir}/resources/qtwebengine_resources_100p.pak
%{_qtdir}/resources/qtwebengine_resources_200p.pak

%package examples
Summary:	Sample code demonstrating the use of %{name}
Group:		Development/KDE and Qt

%description examples
Sample code demonstrating the use of %{name}

%files examples
%{_qtdir}/examples/webenginequick
%{_qtdir}/examples/webenginewidgets
