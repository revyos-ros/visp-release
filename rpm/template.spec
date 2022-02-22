%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-visp
Version:        3.5.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS visp package

License:        GPLv2
URL:            http://www.ros.org/wiki/visp
Source0:        %{name}-%{version}.tar.gz

Requires:       eigen3-devel
Requires:       lapack-devel
Requires:       libX11-devel
Requires:       libjpeg-turbo-devel
Requires:       libpng-devel
Requires:       libv4l-devel
Requires:       libxml2-devel
Requires:       opencv-devel
Requires:       ros-rolling-ros-workspace
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  eigen3-devel
BuildRequires:  lapack-devel
BuildRequires:  libX11-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libv4l-devel
BuildRequires:  libxml2-devel
BuildRequires:  opencv-devel
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
ViSP standing for Visual Servoing Platform is a modular cross platform library
that allows prototyping and developing applications using visual tracking and
visual servoing technics at the heart of the researches done by Inria Lagadic
team. ViSP is able to compute control laws that can be applied to robotic
systems. It provides a set of visual features that can be tracked using real
time image processing or computer vision algorithms. ViSP provides also
simulation capabilities. ViSP can be useful in robotics, computer vision,
augmented reality and computer animation.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Feb 22 2022 Fabien Spindler <Fabien.Spindler@inria.fr> - 3.5.0-1
- Autogenerated by Bloom

* Tue Feb 08 2022 Fabien Spindler <Fabien.Spindler@inria.fr> - 3.4.0-3
- Autogenerated by Bloom

