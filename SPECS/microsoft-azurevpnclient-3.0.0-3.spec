Name: microsoft-azurevpnclient
Version: 3.0.0
Release: 3
Summary: Azure VPN Client
License: see /usr/share/doc/microsoft-azurevpnclient/copyright
Distribution: Debian
Requires: compat-openssl11, zenity, ca-certificates >= 2024.2.69_v8.0.303
Group: Converted/net
%undefine _disable_source_fetch
Source0: https://packages.microsoft.com/ubuntu/20.04/prod/pool/main/m/microsoft-azurevpnclient/microsoft-azurevpnclient_%{VERSION}_amd64.deb
%define SHA256Sum0 a5a9424357017365886fee0a9f295310cbf09655470588e115f7bf5a5e1c9608

%define _rpmdir RPMS
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%global _privatelibs libflutter_.*|liburl_launcher_linux_plugin.so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%define gitsource %(git ls-remote --get-url  origin | sed 's/^.*@//')
%define gitversion %(git rev-parse --short HEAD)%(git diff-files --quiet || echo " with changes")

%description
   The Azure VPN Client lets you connect to Azure securely from anywhere in the world. It supports Microsoft Entra ID and certificate-based authentication.

Azure VPN Client repackaged by ShatteredSilicon.
Built from %{gitsource} at %{gitversion}

# _verdir contains the directory name in BUILD that we will use to extract the package
%define _verdir %{NAME}-%{VERSION}

%prep
echo "Source dir: %{_sourcedir}"
echo "Build dir: %{_builddir}"
echo "Build root: %{buildroot}"

# Validate checksum of deb package
echo "%{SHA256Sum0} %{SOURCE0}" | sha256sum -c

# Clean up any previous build
[ -d "%{_verdir}" ] && rm -rf "%{_verdir}"
mkdir "%{_verdir}"

# Extract package into files dir
cd "%{_verdir}"
ar x "%{SOURCE0}"
mkdir files
cd files
tar -xf ../data.tar.xz

%build
cd "%{NAME}-%{VERSION}/files/"
chmod 0644 etc/rsyslog.d/AzureVPNClient.conf

%install
# Clear previous attempts in BUILDROOT
[ -d "%{buildroot}" ] && rm -rf "%{buildroot}"
mkdir "%{buildroot}"
# Just take everything we made the in the %prep stage
mv -T "%{_verdir}/files" "%{buildroot}"

%post
# Allow non-root users to create network interface
/sbin/setcap cap_net_admin=+pe "/opt/microsoft/microsoft-azurevpnclient/microsoft-azurevpnclient"

%clean
rm -rf "%{_builddir}/%{_verdir}"

%files
"/opt/microsoft/microsoft-azurevpnclient/"
%config "/etc/rsyslog.d/AzureVPNClient.conf"
"/usr/share/applications/microsoft-azurevpnclient.desktop"
%doc "/usr/share/doc/microsoft-azurevpnclient/NOTICE.txt.gz"
%doc "/usr/share/doc/microsoft-azurevpnclient/changelog.gz"
%license "/usr/share/doc/microsoft-azurevpnclient/copyright"
"/usr/share/icons/microsoft-azurevpnclient.png"
"/usr/share/polkit-1/rules.d/microsoft-azurevpnclient.rules"
"/var/lib/polkit-1/localauthority/50-local.d/10-microsoft-azurevpnclient.pkla"
