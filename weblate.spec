Name:           weblate
Version:        0.9
Release:        1
License:        GPL-3+
Summary:        Web based translation
Group:          Productivity/Networking/Web/Frontends
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  bitstream-vera
BuildRequires:  graphviz
BuildRequires:  python-Sphinx
BuildRequires:  graphviz-gd
Url:            http://weblate.org/
Requires:       apache2-mod_wsgi
Requires:       cron
Requires:       python-django >= 1.3
Requires:       python-django-registration
Requires:       python-translate-toolkit
Requires:       python-GitPython >= 0.3
Requires:       python-whoosh
%py_requires
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Vendor:         Michal Čihař <mcihar@suse.com>

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define WLDIR /usr/share/weblate
%define WLDATADIR /var/lib/weblate
%define WLETCDIR /%{_sysconfdir}/weblate

%description
Weblate is web based translation tool with tight Git integration. It features
simple and clean user interface, propagation of translations across subprojects
or automatic linking to source files. 

List of features includes:

* Easy web based translation
* Propagation of translations across sub-projects (for different branches)
* Tight git integration - every change is represented by Git commit
* Usage of Django's admin interface
* Upload and automatic merging of po files
* Links to source files for context
* Allows to use machine translation services
* Message consistency checks
* Tunable access control
* Wide range of supported translation formats (Getext, Qt, Java, Windows, Symbian and more)


%prep
%setup -q

%build
make -C docs html
sed -i 's@^WEB_ROOT = .*@WEB_ROOT = "%{WLDIR}"@g' settings.py 
sed -i 's@^WHOOSH_INDEX = .*@WHOOSH_INDEX = "%{WLDATADIR}"@g' settings.py
sed -i 's@/usr/lib/python.*/site-packages@%{python_sitelib}@g' scripts/apache.conf
sed -i 's@weblate-path@%{WLDIR}@g' scripts/django.wsgi

%install
install -d %{buildroot}/%{WLDIR}
install -d %{buildroot}/%{WLETCDIR}

# Copy all files
cp -a . %{buildroot}/%{WLDIR}

# We ship this separately
rm -rf %{buildroot}/%{WLDIR}/docs
rm -f %{buildroot}/%{WLDIR}/README.rst \
    %{buildroot}/%{WLDIR}/ChangeLog \
    %{buildroot}/%{WLDIR}/INSTALL

# Byte compile python files
%py_compile %{buildroot}/%{WLDIR}

# Move configuration to etc
mv %{buildroot}/%{WLDIR}/settings.py %{buildroot}/%{WLETCDIR}/
ln -s %{WLETCDIR}/settings.py %{buildroot}/%{WLDIR}/settings.py

# Apache config
install -d %{buildroot}/%{_sysconfdir}/apache2/vhosts.d/
install -m 644 scripts/apache.conf %{buildroot}/%{_sysconfdir}/apache2/vhosts.d/weblate.conf

# Whoosh index dir
install -d %{buildroot}/%{WLDATADIR}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/_build/html
%doc README.rst
%config(noreplace) /%{_sysconfdir}/weblate
%config(noreplace) /%{_sysconfdir}/apache2
%{WLDIR}
%attr(0755,wwwrun,www) %{WLDATADIR}

%changelog
