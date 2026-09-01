%define exec_path check_k8s.py
%define app_install_path %{prefix}/check_k8s

# Disable automatic dependency detection for venv paths
%global __requires_exclude ^/opt/plugins/check_k8s/.*$

# Define Python interpreter for byte-code compilation
%global __python3 %{app_install_path}/bin/python -I

Summary: Kubernetes plugin for Nagios
Name: monitor-plugin-check_k8s
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPLv2
Group: op5/system-addons
URL: https://www.itrsgroup.com
Prefix: /opt/plugins
Requires: python3.12
Requires: op5-monitor-user
BuildRequires: python3.12-devel
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Nagios plugin for monitoring Kubernetes Clusters, built using the Python standard library.

%prep
%setup -q -n %{name}-%{version}

%install
%{__install} -D %{exec_path} %{buildroot}%{prefix}/%{exec_path}

# Ship pre-built binary wheels, to be installed in %%post.
%{__install} -Dp -m 0644 -t %{buildroot}%{app_install_path}/wheels dist/*.whl

# Metadata
%{__mkdir} -p -m 0755 %buildroot%prefix/metadata
%{__install} -m 0644 op5build/check_k8s.metadata %buildroot%prefix/metadata/

%pre
# Remove old install and wheels directories created by previous versions
%{__rm} -rf %{prefix}/k8s || :
%{__rm} -rf /opt/monitor/op5/check_k8s || :
%{__rm} -rf %{app_install_path}/wheels || :

%post
cd %{app_install_path}
# Create a new venv
python3.12 -m venv .
# First install the pip version that was used in the build
bin/pip install --upgrade -f wheels --no-index --no-deps pip
# Then install all the remaining packages
bin/pip install --upgrade --no-index wheels/*.whl
# Remove the wheels directory, no longer needed
%{__rm} -rf wheels

%files
%{prefix}/%{exec_path}
%{app_install_path}/wheels
%dir %attr(0755,-,-) %prefix/metadata/
%prefix/metadata/check_k8s.metadata
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Fri Jul 18 2025 Jerick Macario <jmacario@itrsgroup.com>
- Restructure app locations to plugins directory.
* Tue Jul 15 2025 Jerick Macario <jmacario@itrsgroup.com>
- Update Python version to 3.12 and the dependencies.
- Change execution to run under venv
* Tue Jan 18 2022 Erik Sjöström <esjostrom@itrsgroup.com>
- Package metadata.
* Fri Aug 07 2020 Jacob Hansen <jhansen@op5.com> - 0.1.0
- Add OP5-monitor-user requirement
* Fri Aug 16 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init
