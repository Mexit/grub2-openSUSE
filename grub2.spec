#
# spec file for package grub2
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# needssslcertforbuild


%define _binaries_in_noarch_package_terminate_build 0

Name:           grub2
%ifarch x86_64 ppc64
BuildRequires:  gcc-32bit
BuildRequires:  glibc-32bit
BuildRequires:  glibc-devel-32bit glibc-32bit
%else
BuildRequires:  gcc
BuildRequires:  glibc-devel
%endif
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  device-mapper-devel
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  freetype2-devel
BuildRequires:  fuse-devel
%if 0%{?suse_version} >= 1140
BuildRequires:  dejavu-fonts
BuildRequires:  gnu-unifont
%endif
BuildRequires:  help2man
BuildRequires:  xz
%if 0%{?suse_version} >= 1210
BuildRequires:  makeinfo
%else
BuildRequires:  texinfo
%endif
%if %{defined pythons}
BuildRequires:  %{pythons}
%else
BuildRequires:  python
%endif
BuildRequires:  xz-devel
%ifarch x86_64 aarch64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
BuildRequires:  openssl >= 0.9.8
BuildRequires:  pesign-obs-integration
%endif
%endif
%if 0%{?suse_version} >= 1210
# Package systemd services files grub2-once.service
BuildRequires:  systemd-rpm-macros
%define has_systemd 1
%endif
%if 0%{?suse_version} > 1320
BuildRequires:  update-bootloader-rpm-macros
%endif

# Modules code is dynamically loaded and collected from a _fixed_ path.
%define _libdir %{_exec_prefix}/lib

# Build grub2-emu everywhere (it may be "required" by 'grub2-once')
%define emu 1

%ifarch ppc ppc64 ppc64le
%define grubcpu powerpc
%define platform ieee1275
# emu does not build here yet... :-(
%define emu 0
%endif

%ifarch %{ix86} x86_64
%define grubcpu i386
%define platform pc
%endif

%ifarch s390x
%define grubcpu s390x
%define platform emu
%endif

%ifarch %{arm}
%define grubcpu arm
%define platform uboot
%endif

%ifarch aarch64
%define grubcpu arm64
%define platform efi
%define only_efi 1
%endif

%ifarch riscv64
%define grubcpu riscv64
%define platform efi
%define only_efi 1
%endif

%define grubarch %{grubcpu}-%{platform}

# build efi bootloader on some platforms only:
%if ! 0%{?efi:1}
%global efi %{ix86} x86_64 ia64 aarch64 %{arm} riscv64
%endif

%ifarch %{efi}
%ifarch %{ix86}
%define grubefiarch i386-efi
%else
%ifarch aarch64
%define grubefiarch arm64-efi
%else
%ifarch %{arm}
%define grubefiarch arm-efi
%else
%define grubefiarch %{_target_cpu}-efi
%endif
%endif
%endif
%endif

%ifarch %{ix86}
%define grubxenarch i386-xen
%endif

%ifarch x86_64
%define grubxenarch x86_64-xen
%endif

%if "%{platform}" == "emu"
# force %%{emu} to 1, e.g. for s390
%define emu 1
%endif

%if 0%{?suse_version} == 1110
%define only_efi %{nil}
%define only_x86_64 %{nil}
%endif

Version:        2.04
Release:        39.6
Summary:        Bootloader with support for Linux, Multiboot and more
License:        GPL-3.0-or-later
Group:          System/Boot
URL:            http://www.gnu.org/software/grub/
Source0:        https://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
Source1:        90_persistent
Source2:        grub.default
Source4:        grub2.rpmlintrc
Source6:        grub2-once
Source7:        20_memtest86+
Source8:        README.ibm3215
Source10:       openSUSE-UEFI-CA-Certificate.crt
Source11:       SLES-UEFI-CA-Certificate.crt
Source12:       grub2-snapper-plugin.sh
Source14:       80_suse_btrfs_snapshot
Source15:       grub2-once.service
Source16:       grub2-xen-pv-firmware.cfg
# required hook for systemd-sleep (bsc#941758)
Source17:       grub2-systemd-sleep.sh
Source18:       grub2-check-default.sh
Source1000:     PATCH_POLICY
Patch1:         rename-grub-info-file-to-grub2.patch
Patch2:         grub2-linux.patch
Patch3:         use-grub2-as-a-package-name.patch
Patch4:         info-dir-entry.patch
Patch6:         grub2-iterate-and-hook-for-extended-partition.patch
Patch8:         grub2-ppc-terminfo.patch
Patch9:         grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
Patch10:        grub2-fix-error-terminal-gfxterm-isn-t-found.patch
Patch12:        grub2-fix-menu-in-xen-host-server.patch
Patch15:        not-display-menu-when-boot-once.patch
Patch17:        grub2-pass-corret-root-for-nfsroot.patch
Patch19:        grub2-efi-HP-workaround.patch
Patch21:        grub2-secureboot-add-linuxefi.patch
Patch22:        grub2-secureboot-use-linuxefi-on-uefi.patch
Patch23:        grub2-secureboot-no-insmod-on-sb.patch
Patch24:        grub2-secureboot-provide-linuxefi-config.patch
Patch25:        grub2-secureboot-chainloader.patch
Patch26:        grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch
Patch27:        grub2-linuxefi-fix-boot-params.patch
Patch35:        grub2-linguas.sh-no-rsync.patch
Patch37:        grub2-use-Unifont-for-starfield-theme-terminal.patch
Patch38:        grub2-s390x-01-Changes-made-and-files-added-in-order-to-allow-s390x.patch
Patch39:        grub2-s390x-02-kexec-module-added-to-emu.patch
Patch40:        grub2-s390x-03-output-7-bit-ascii.patch
Patch41:        grub2-s390x-04-grub2-install.patch
Patch42:        grub2-s390x-05-grub2-mkconfig.patch
Patch43:        grub2-use-rpmsort-for-version-sorting.patch
Patch53:        grub2-getroot-treat-mdadm-ddf-as-simple-device.patch
Patch56:        grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
Patch58:        grub2-xen-linux16.patch
Patch59:        grub2-efi-disable-video-cirrus-and-bochus.patch
Patch60:        grub2-editenv-add-warning-message.patch
Patch61:        grub2-vbe-blacklist-preferred-1440x900x32.patch
Patch64:        grub2-grubenv-in-btrfs-header.patch
Patch65:        grub2-mkconfig-aarch64.patch
Patch70:        grub2-default-distributor.patch
Patch71:        grub2-menu-unrestricted.patch
Patch72:        grub2-mkconfig-arm.patch
Patch75:        grub2-s390x-06-loadparm.patch
Patch76:        grub2-s390x-07-add-image-param-for-zipl-setup.patch
Patch77:        grub2-s390x-08-workaround-part-to-disk.patch
Patch78:        grub2-commands-introduce-read_file-subcommand.patch
Patch79:        grub2-efi-chainload-harder.patch
Patch80:        grub2-emu-4-all.patch
Patch81:        grub2-lvm-allocate-metadata-buffer-from-raw-contents.patch
Patch82:        grub2-diskfilter-support-pv-without-metadatacopies.patch
Patch83:        grub2-efi-uga-64bit-fb.patch
Patch84:        grub2-s390x-09-improve-zipl-setup.patch
Patch85:        grub2-getroot-scan-disk-pv.patch
Patch92:        grub2-util-30_os-prober-multiple-initrd.patch
Patch93:        grub2-getroot-support-nvdimm.patch
Patch94:        grub2-install-fix-not-a-directory-error.patch
Patch95:        grub2-verifiers-fix-system-freeze-if-verify-failed.patch
Patch96:        grub-install-force-journal-draining-to-ensure-data-i.patch
Patch97:        grub2-s390x-skip-zfcpdump-image.patch
# Btrfs snapshot booting related patches
Patch101:       grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
Patch102:       grub2-btrfs-02-export-subvolume-envvars.patch
Patch103:       grub2-btrfs-03-follow_default.patch
Patch104:       grub2-btrfs-04-grub2-install.patch
Patch105:       grub2-btrfs-05-grub2-mkconfig.patch
Patch106:       grub2-btrfs-06-subvol-mount.patch
Patch107:       grub2-btrfs-07-subvol-fallback.patch
Patch108:       grub2-btrfs-08-workaround-snapshot-menu-default-entry.patch
Patch109:       grub2-btrfs-09-get-default-subvolume.patch
Patch110:       grub2-btrfs-10-config-directory.patch
Patch111:       0001-btrfs-disable-zstd-support-for-i386-pc.patch
# Support EFI xen loader
Patch120:       grub2-efi-xen-chainload.patch
Patch121:       grub2-efi-chainloader-root.patch
Patch122:       grub2-efi-xen-cmdline.patch
Patch123:       grub2-efi-xen-cfg-unquote.patch
Patch124:       grub2-efi-xen-removable.patch
# Hidden menu entry and hotkey "t" for text console
Patch140:       grub2-Add-hidden-menu-entries.patch
Patch141:       grub2-SUSE-Add-the-t-hotkey.patch
# Linux root device related patches
Patch163:       grub2-zipl-setup-fix-btrfs-multipledev.patch
Patch164:       grub2-suse-remove-linux-root-param.patch
# PPC64 LE support
Patch205:       grub2-ppc64le-disable-video.patch
Patch207:       grub2-ppc64le-memory-map.patch
# PPC 
Patch211:       grub2-ppc64-cas-reboot-support.patch
Patch212:       grub2-install-remove-useless-check-PReP-partition-is-empty.patch
Patch213:       grub2-Fix-incorrect-netmask-on-ppc64.patch
Patch215:       grub2-ppc64-cas-new-scope.patch
Patch218:       grub2-ppc64-cas-fix-double-free.patch
Patch233:       grub2-use-stat-instead-of-udevadm-for-partition-lookup.patch
Patch234:       fix-grub2-use-stat-instead-of-udevadm-for-partition-lookup-with-new-glibc.patch
Patch236:       grub2-efi_gop-avoid-low-resolution.patch
# Support HTTP Boot IPv4 and IPv6 (fate#320129)
Patch281:       0002-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
Patch282:       0003-bootp-New-net_bootp6-command.patch
Patch283:       0004-efinet-UEFI-IPv6-PXE-support.patch
Patch284:       0005-grub.texi-Add-net_bootp6-doument.patch
Patch285:       0006-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
Patch286:       0007-efinet-Setting-network-from-UEFI-device-path.patch
Patch287:       0008-efinet-Setting-DNS-server-from-UEFI-protocol.patch
# Fix GOP BLT support (FATE#322332)
Patch311:       grub2-efi-gop-add-blt.patch
# TPM Support (FATE#315831)
Patch411:       0012-tpm-Build-tpm-as-module.patch
# UEFI HTTP and related network protocol support (FATE#320130)
Patch420:       0001-add-support-for-UEFI-network-protocols.patch
Patch421:       0002-AUDIT-0-http-boot-tracker-bug.patch
# check if default entry need to be corrected for updated distributor version 
# and/or use fallback entry if default kernel entry removed (bsc#1065349)
Patch430:       grub2-mkconfig-default-entry-correction.patch
Patch431:       grub2-s390x-10-keep-network-at-kexec.patch
Patch432:       grub2-s390x-11-secureboot.patch
# Support for UEFI Secure Boot on AArch64 (FATE#326541)
Patch450:       grub2-secureboot-install-signed-grub.patch
Patch501:       grub2-btrfs-help-on-snapper-rollback.patch
# Improved hiDPI device support (FATE#326680)
Patch510:       grub2-video-limit-the-resolution-for-fixed-bimap-font.patch
# Support long menuentries (FATE#325760)
Patch511:       grub2-gfxmenu-support-scrolling-menu-entry-s-text.patch
# RISC-V fixes
Patch601:       risc-v-fix-computation-of-pc-relative-relocation-offset.patch
Patch602:       risc-v-add-clzdi2-symbol.patch
Patch603:       grub-install-define-default-platform-for-risc-v.patch
# Fix gcc-10 build fail
Patch610:       0001-mdraid1x_linux-Fix-gcc10-error-Werror-array-bounds.patch
Patch611:       0002-zfs-Fix-gcc10-error-Werror-zero-length-bounds.patch
# bsc#1166409 - Grub netbooting does not search for grub.cfg files with mac
# address or ip address in filename
Patch700:       0001-normal-Move-common-datetime-functions-out-of-the-nor.patch
Patch701:       0002-kern-Add-X-option-to-printf-functions.patch
Patch702:       0003-normal-main-Search-for-specific-config-files-for-net.patch
Patch703:       0004-datetime-Enable-the-datetime-module-for-the-emu-plat.patch
# bsc#1168994 VUL-0: EMBARGOED: CVE-2020-10713: grub2: parsing overflows can
# bypass secure boot restrictions
Patch704:       0001-yylex-Make-lexer-fatal-errors-actually-be-fatal.patch
# bsc#1173812 VUL-0: EMBARGOED: CVE-2020-14308, CVE-2020-14309, CVE-2020-14310,
# CVE-2020-14311: grub2: avoid integer overflows
Patch705:       0002-safemath-Add-some-arithmetic-primitives-that-check-f.patch
Patch706:       0003-calloc-Make-sure-we-always-have-an-overflow-checking.patch
Patch707:       0004-calloc-Use-calloc-at-most-places.patch
Patch708:       0005-malloc-Use-overflow-checking-primitives-where-we-do-.patch
Patch709:       0006-iso9660-Don-t-leak-memory-on-realloc-failures.patch
Patch710:       0007-font-Do-not-load-more-than-one-NAME-section.patch
# bsc#1174463 VUL-0: EMBARGOED: CVE-2020-15706: grub2: script: Avoid a
# use-after-free when redefining a function during execution
Patch711:       0008-script-Remove-unused-fields-from-grub_script_functio.patch
Patch712:       0009-script-Avoid-a-use-after-free-when-redefining-a-func.patch
# bsc#1174570 VUL-0: EMBARGOED: CVE-2020-15707: grub2: linux: Fix integer
# overflows in initrd size handling
Patch713:       0010-linux-Fix-integer-overflows-in-initrd-size-handling.patch
Patch714:       0001-kern-mm.c-Make-grub_calloc-inline.patch
Patch716:       0002-cmdline-Provide-cmdline-functions-as-module.patch
# bsc#1172745 L3: SLES 12 SP4 - Slow boot of system after updated kernel -
# takes 45 minutes after grub to start loading kernel
Patch717:       0001-ieee1275-powerpc-implements-fibre-channel-discovery-.patch
Patch718:       0002-ieee1275-powerpc-enables-device-mapper-discovery.patch
Patch719:       0001-Unify-the-check-to-enable-btrfs-relative-path.patch
Patch721:       0001-efi-linux-provide-linux-command.patch
# Improve the error handling when grub2-install fails with short mbr gap
# (bsc#1176062)
Patch722:       0001-Warn-if-MBR-gap-is-small-and-user-uses-advanced-modu.patch
Patch723:       0002-grub-install-Avoid-incompleted-install-on-i386-pc.patch
# Secure Boot support in GRUB on aarch64 (jsc#SLE-15864)
Patch730:       0001-Add-support-for-Linux-EFI-stub-loading-on-aarch64.patch
Patch731:       0002-arm64-make-sure-fdt-has-address-cells-and-size-cells.patch
Patch732:       0003-Make-grub_error-more-verbose.patch
Patch733:       0004-arm-arm64-loader-Better-memory-allocation-and-error-.patch
Patch734:       0005-Make-linux_arm_kernel_header.hdr_offset-be-at-the-ri.patch
Patch735:       0006-efi-Set-image-base-address-before-jumping-to-the-PE-.patch
Patch737:       0008-squash-Add-support-for-Linux-EFI-stub-loading-on-aar.patch
Patch738:       0009-squash-Add-support-for-linuxefi.patch
Patch739:       0001-Fix-build-error-in-binutils-2.36.patch
Patch740:       0001-emu-fix-executable-stack-marking.patch
# Boothole2
Patch741:       0001-include-grub-i386-linux.h-Include-missing-grub-types.patch
Patch742:       0002-efi-Make-shim_lock-GUID-and-protocol-type-public.patch
Patch743:       0003-efi-Return-grub_efi_status_t-from-grub_efi_get_varia.patch
Patch744:       0004-efi-Add-a-function-to-read-EFI-variables-with-attrib.patch
Patch745:       0005-efi-Add-secure-boot-detection.patch
Patch746:       0006-efi-Only-register-shim_lock-verifier-if-shim_lock-pr.patch
Patch747:       0007-verifiers-Move-verifiers-API-to-kernel-image.patch
Patch748:       0008-efi-Move-the-shim_lock-verifier-to-the-GRUB-core.patch
Patch749:       0009-kern-Add-lockdown-support.patch
Patch750:       0010-kern-lockdown-Set-a-variable-if-the-GRUB-is-locked-d.patch
Patch751:       0011-efi-Lockdown-the-GRUB-when-the-UEFI-Secure-Boot-is-e.patch
Patch752:       0012-efi-Use-grub_is_lockdown-instead-of-hardcoding-a-dis.patch
Patch753:       0013-acpi-Don-t-register-the-acpi-command-when-locked-dow.patch
Patch754:       0014-mmap-Don-t-register-cutmem-and-badram-commands-when-.patch
Patch755:       0015-commands-Restrict-commands-that-can-load-BIOS-or-DT-.patch
Patch756:       0016-commands-setpci-Restrict-setpci-command-when-locked-.patch
Patch757:       0017-commands-hdparm-Restrict-hdparm-command-when-locked-.patch
Patch758:       0018-gdb-Restrict-GDB-access-when-locked-down.patch
Patch759:       0019-loader-xnu-Don-t-allow-loading-extension-and-package.patch
Patch760:       0020-dl-Only-allow-unloading-modules-that-are-not-depende.patch
Patch761:       0021-usb-Avoid-possible-out-of-bound-accesses-caused-by-m.patch
Patch762:       0022-lib-arg-Block-repeated-short-options-that-require-an.patch
Patch763:       0023-commands-menuentry-Fix-quoting-in-setparams_prefix.patch
Patch764:       0024-kern-parser-Fix-resource-leak-if-argc-0.patch
Patch765:       0025-kern-parser-Fix-a-memory-leak.patch
Patch766:       0026-kern-parser-Introduce-process_char-helper.patch
Patch767:       0027-kern-parser-Introduce-terminate_arg-helper.patch
Patch768:       0028-kern-parser-Refactor-grub_parser_split_cmdline-clean.patch
Patch769:       0029-kern-buffer-Add-variable-sized-heap-buffer.patch
Patch770:       0030-kern-parser-Fix-a-stack-buffer-overflow.patch
Patch771:       0031-util-mkimage-Remove-unused-code-to-add-BSS-section.patch
Patch772:       0032-util-mkimage-Use-grub_host_to_target32-instead-of-gr.patch
Patch773:       0033-util-mkimage-Always-use-grub_host_to_target32-to-ini.patch
Patch774:       0034-util-mkimage-Unify-more-of-the-PE32-and-PE32-header-.patch
Patch775:       0035-util-mkimage-Reorder-PE-optional-header-fields-set-u.patch
Patch776:       0036-util-mkimage-Improve-data_size-value-calculation.patch
Patch777:       0037-util-mkimage-Refactor-section-setup-to-use-a-helper.patch
Patch778:       0038-util-mkimage-Add-an-option-to-import-SBAT-metadata-i.patch
Patch779:       0039-grub-install-common-Add-sbat-option.patch
Patch780:       0040-shim_lock-Only-skip-loading-shim_lock-verifier-with-.patch
Patch781:       0041-squash-Add-secureboot-support-on-efi-chainloader.patch
Patch782:       0042-squash-grub2-efi-chainload-harder.patch
Patch783:       0043-squash-Don-t-allow-insmod-when-secure-boot-is-enable.patch
Patch784:       0044-squash-kern-Add-lockdown-support.patch
Patch785:       0045-squash-Add-support-for-Linux-EFI-stub-loading-on-aar.patch
Patch786:       0046-squash-verifiers-Move-verifiers-API-to-kernel-image.patch
Patch787:       0001-kern-efi-sb-Add-chainloaded-image-as-shim-s-verifiab.patch

Requires:       gettext-runtime
%if 0%{?suse_version} >= 1140
%ifnarch s390x
Recommends:     os-prober
%endif
# xorriso not available using grub2-mkrescue (bnc#812681)
# downgrade to suggest as minimal system can't afford pulling in tcl/tk and half of the x11 stack (bsc#1102515)
Suggests:       libburnia-tools
Suggests:       mtools
%endif
%if ! 0%{?only_efi:1}
Requires:       grub2-%{grubarch} = %{version}-%{release}
%endif
%ifarch s390x
# required utilities by grub2-s390x-04-grub2-install.patch
# use 'showconsole' to determine console device. (bnc#876743)
Requires:       /sbin/showconsole
Requires:       kexec-tools
# for /sbin/zipl used by grub2-zipl-setup
Requires:       s390-tools
%endif
%ifarch ppc64 ppc64le
Requires:       powerpc-utils
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if 0%{?only_x86_64:1}
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{ix86} x86_64 ppc ppc64 ppc64le s390x aarch64 %{arm} riscv64
%endif

%description
This is the second version of the GRUB (Grand Unified Bootloader), a
highly configurable and customizable bootloader with modular
architecture.  It support rich scale of kernel formats, file systems,
computer architectures and hardware devices.

This package includes user space utlities to manage GRUB on your system.


Authors:
--------
    Gordon Matzigkeit
    Yoshinori K. Okuji
    Colin Watson
    Colin D. Bennett
    Vesa Jääskeläinen
    Robert Millan
    Carles Pina

%package branding-upstream

Summary:        Upstream branding for GRUB2's graphical console
Group:          System/Fhs
Requires:       %{name} = %{version}

%description branding-upstream
Upstream branding for GRUB2's graphical console

%if ! 0%{?only_efi:1}
%package %{grubarch}

Summary:        Bootloader with support for Linux, Multiboot and more
Group:          System/Boot
%if "%{platform}" != "emu"
BuildArch:      noarch
%endif
Requires:       %{name} = %{version}
Requires(post):	%{name} = %{version}
%if 0%{?update_bootloader_requires:1}
%update_bootloader_requires
%else
Requires:       perl-Bootloader
Requires(post): perl-Bootloader
%endif

%description %{grubarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for %{platform} systems.

%package %{grubarch}-debug
Summary:        Debug symbols for %{grubarch}
Group:          System/Boot
%if "%{platform}" != "emu"
BuildArch:      noarch
%endif
Requires:       %{name}-%{grubarch} = %{version}

%description %{grubarch}-debug
Debug information for %{name}-%{grubarch}

Information on how to debug grub can be found online:
https://www.cnblogs.com/coryxie/archive/2013/03/12/2956807.html

%endif

%ifarch %{efi}

%package %{grubefiarch}

Summary:        Bootloader with support for Linux, Multiboot and more
Group:          System/Boot
BuildArch:      noarch
# Require efibootmgr
# Without it grub-install is broken so break the package as well if unavailable
Requires:       efibootmgr
Requires(post): efibootmgr
Requires:       %{name} = %{version}
Requires(post):	%{name} = %{version}
%if 0%{?update_bootloader_requires:1}
%update_bootloader_requires
%else
Requires:       perl-Bootloader >= 0.706
Requires(post): perl-Bootloader >= 0.706
%endif
Provides:       %{name}-efi = %{version}-%{release}
Obsoletes:      %{name}-efi < %{version}-%{release}

%description %{grubefiarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.

%package %{grubefiarch}-debug
Summary:        Debug symbols for %{grubefiarch}
Group:          System/Boot
%if "%{platform}" != "emu"
BuildArch:      noarch
%endif
Requires:       %{name}-%{grubefiarch} = %{version}

%description %{grubefiarch}-debug
Debug symbols for %{name}-%{grubefiarch}

Information on how to debug grub can be found online:
https://www.cnblogs.com/coryxie/archive/2013/03/12/2956807.html

%endif

%ifarch %{ix86} x86_64

%package %{grubxenarch}

Summary:        Bootloader with support for Linux, Multiboot and more
Group:          System/Boot
Provides:       %{name}-xen = %{version}-%{release}
Obsoletes:      %{name}-xen < %{version}-%{release}
BuildArch:      noarch

%description %{grubxenarch}
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It supports rich variety of kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for XEN systems.

%endif

%package snapper-plugin

Summary:        Grub2's snapper plugin
Group:          System/Fhs
Requires:       %{name} = %{version}
Requires:       libxml2-tools
Supplements:    packageand(snapper:grub2)
BuildArch:      noarch

%description snapper-plugin
Grub2's snapper plugin for advanced btrfs snapshot boot menu management

%if 0%{?has_systemd:1}
%package systemd-sleep-plugin

Summary:        Grub2's systemd-sleep plugin
Group:          System/Fhs
Requires:       grub2
Requires:       util-linux
Supplements:    packageand(systemd:grub2)
BuildArch:      noarch

%description systemd-sleep-plugin
Grub2's systemd-sleep plugin for directly booting hibernated kernel image in
swap partition while in resuming
%endif

%prep
# We create (if we build for efi) two copies of the sources in the Builddir
%setup -q -n grub-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch12 -p1
%patch15 -p1
%patch17 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch35 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch53 -p1
%patch56 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch64 -p1
%patch65 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch140 -p1
%patch141 -p1
%patch163 -p1
%patch164 -p1
%patch205 -p1
%patch207 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch215 -p1
%patch218 -p1
%patch233 -p1
%patch234 -p1
%patch236 -p1
%patch281 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch285 -p1
%patch286 -p1
%patch287 -p1
%patch311 -p1
%patch411 -p1
%patch420 -p1
%patch421 -p1
%patch430 -p1
%patch431 -p1
%patch432 -p1
%patch450 -p1
%patch501 -p1
%patch510 -p1
%patch511 -p1
%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch610 -p1
%patch611 -p1
%patch700 -p1
%patch701 -p1
%patch702 -p1
%patch703 -p1
%patch704 -p1
%patch705 -p1
%patch706 -p1
%patch707 -p1
%patch708 -p1
%patch709 -p1
%patch710 -p1
%patch711 -p1
%patch712 -p1
%patch713 -p1
%patch714 -p1
%patch716 -p1
%patch717 -p1
%patch718 -p1
%patch719 -p1
%patch721 -p1
%patch722 -p1
%patch723 -p1
%patch730 -p1
%patch731 -p1
%patch732 -p1
%patch733 -p1
%patch734 -p1
%patch735 -p1
%patch737 -p1
%patch738 -p1
%patch739 -p1
%patch740 -p1
%patch741 -p1
%patch742 -p1
%patch743 -p1
%patch744 -p1
%patch745 -p1
%patch746 -p1
%patch747 -p1
%patch748 -p1
%patch749 -p1
%patch750 -p1
%patch751 -p1
%patch752 -p1
%patch753 -p1
%patch754 -p1
%patch755 -p1
%patch756 -p1
%patch757 -p1
%patch758 -p1
%patch759 -p1
%patch760 -p1
%patch761 -p1
%patch762 -p1
%patch763 -p1
%patch764 -p1
%patch765 -p1
%patch766 -p1
%patch767 -p1
%patch768 -p1
%patch769 -p1
%patch770 -p1
%patch771 -p1
%patch772 -p1
%patch773 -p1
%patch774 -p1
%patch775 -p1
%patch776 -p1
%patch777 -p1
%patch778 -p1
%patch779 -p1
%patch780 -p1
%patch781 -p1
%patch782 -p1
%patch783 -p1
%patch784 -p1
%patch785 -p1
%patch786 -p1
%patch787 -p1

%build
# collect evidence to debug spurious build failure on SLE15
ulimit -a
# patches above may update the timestamp of grub.texi
# and via build-aux/mdate-sh they end up in grub2.info, breaking build-compare
[ -z "$SOURCE_DATE_EPOCH" ] ||\
  [ `stat -c %Y docs/grub.texi` -lt $SOURCE_DATE_EPOCH ] ||\
  touch -d@$SOURCE_DATE_EPOCH docs/grub.texi

# This simplifies patch handling without need to use git to create patch
# that renames file
mv docs/grub.texi docs/grub2.texi

cp %{SOURCE8} .
mkdir build
%ifarch %{efi}
mkdir build-efi
%endif
%ifarch %{ix86} x86_64
mkdir build-xen
%endif
%if %{emu}
mkdir build-emu
%endif

export PYTHON=%{_bindir}/python3
[ -x $PYTHON ] || unset PYTHON   # try 'python', if 'python3' is unavailable
# autogen calls autoreconf -vi
./autogen.sh
# Not yet:
%define common_conf_options TARGET_LDFLAGS=-static --program-transform-name=s,grub,%{name},
# This does NOT work on SLE11:
%define _configure ../configure

# We don't want to let rpm override *FLAGS with default a.k.a bogus values.
CFLAGS="-fno-strict-aliasing -fno-inline-functions-called-once "
CXXFLAGS=" "
FFLAGS=" "
export CFLAGS CXXFLAGS FFLAGS

%if %{emu}
cd build-emu
%define arch_specific --enable-device-mapper --disable-grub-mount
TLFLAGS="-fPIC"

# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
../configure TARGET_LDFLAGS=$TLFLAGS	\
	--prefix=%{_prefix}		\
	--libdir=%{_datadir}		\
	--sysconfdir=%{_sysconfdir}	\
        --target=%{_target_platform}    \
        --with-platform=emu     \
	%{arch_specific}                \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}
cd ..
if [ "%{platform}" = "emu" ]; then
  rmdir build
  mv build-emu build
fi
%endif

%ifarch %{ix86} x86_64
cd build-xen
../configure                           \
        TARGET_LDFLAGS=-static         \
        --prefix=%{_prefix}            \
        --libdir=%{_datadir}           \
        --sysconfdir=%{_sysconfdir}    \
        --target=%{_target_platform}   \
        --with-platform=xen            \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}

./grub-mkstandalone --grub-mkimage=./grub-mkimage -o grub.xen -O %{grubxenarch} -d grub-core/ "/boot/grub/grub.cfg=%{SOURCE16}"

cd ..
%endif

%ifarch %{efi}
cd build-efi
../configure   				                \
        TARGET_LDFLAGS=-static                          \
	--prefix=%{_prefix}				\
	--libdir=%{_datadir}				\
	--sysconfdir=%{_sysconfdir}			\
        --target=%{_target_platform}                    \
        --with-platform=efi                             \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}

#TODO: add efifwsetup module

FS_MODULES="btrfs ext2 xfs jfs reiserfs"
CD_MODULES=" all_video boot cat chain configfile echo true \
		efinet font gfxmenu gfxterm gzio halt iso9660 \
		jpeg minicmd normal part_apple part_msdos part_gpt \
		password_pbkdf2 png reboot search search_fs_uuid \
		search_fs_file search_label sleep test video fat loadenv"
PXE_MODULES="efinet tftp http"
CRYPTO_MODULES="luks gcry_rijndael gcry_sha1 gcry_sha256"

%ifarch x86_64
CD_MODULES="${CD_MODULES} linuxefi" 
%else
CD_MODULES="${CD_MODULES} linux" 
%endif

# SBAT metadata
%if 0%{?is_opensuse} == 1
distro_id="opensuse"
distro_name="The openSUSE Project"
%else
distro_id="sle"
distro_name="SUSE Linux Enterprise"
%endif
upstream_sbat=1
distro_sbat=1
echo "sbat,1,SBAT Version,sbat,1,https://github.com/rhboot/shim/blob/main/SBAT.md" > sbat.csv
echo "grub,${upstream_sbat},Free Software Foundation,grub,%{version},https://www.gnu.org/software/grub/" >> sbat.csv
echo "grub.${distro_id},${distro_sbat},${distro_name},%{name},%{version},mail:security-team@suse.de" >> sbat.csv

GRUB_MODULES="${CD_MODULES} ${FS_MODULES} ${PXE_MODULES} ${CRYPTO_MODULES} mdraid09 mdraid1x lvm serial"
./grub-mkimage -O %{grubefiarch} -o grub.efi --prefix= --sbat sbat.csv \
		-d grub-core ${GRUB_MODULES}
%ifarch x86_64
./grub-mkimage -O %{grubefiarch} -o grub-tpm.efi --prefix= --sbat sbat.csv \
		-d grub-core ${GRUB_MODULES} tpm
%endif

%ifarch x86_64 aarch64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
if test -e %{_sourcedir}/_projectcert.crt ; then
    prjsubject=$(openssl x509 -in %{_sourcedir}/_projectcert.crt -noout -subject_hash)
    prjissuer=$(openssl x509 -in %{_sourcedir}/_projectcert.crt -noout -issuer_hash)
    opensusesubject=$(openssl x509 -in %{SOURCE10} -noout -subject_hash)
    slessubject=$(openssl x509 -in %{SOURCE11} -noout -subject_hash)
    if test "$prjissuer" = "$opensusesubject" ; then
        cert=%{SOURCE10}
    fi
    if test "$prjissuer" = "$slessubject" ; then
        cert=%{SOURCE11}
    fi
    if test "$prjsubject" = "$prjissuer" ; then
        cert=%{_sourcedir}/_projectcert.crt
    fi
fi
if test -z "$cert" ; then
    echo "cannot identify project, assuming openSUSE signing"
    cert=%{SOURCE10}
fi

openssl x509 -in $cert -outform DER -out grub.der
%endif
%endif

cd ..
%endif

%if ! 0%{?only_efi:1}
cd build

# 64-bit x86-64 machines use 32-bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64 
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if "%{platform}" != "emu"
%define arch_specific --enable-device-mapper
TLFLAGS="-static"

# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
../configure TARGET_LDFLAGS="$TLFLAGS"	\
	--prefix=%{_prefix}		\
	--libdir=%{_datadir}		\
	--sysconfdir=%{_sysconfdir}	\
        --target=%{_target_platform}    \
        --with-platform=%{platform}     \
	%{arch_specific}                \
        --program-transform-name=s,grub,%{name},
make %{?_smp_mflags}
%endif
cd ..
%endif

%install

%ifarch %{ix86} x86_64
cd build-xen
%make_install
install -m 644 grub.xen %{buildroot}/%{_datadir}/%{name}/%{grubxenarch}/.
# provide compatibility sym-link for VM definitions pointing to old location
install -d %{buildroot}%{_libdir}/%{name}/%{grubxenarch}
ln -srf %{buildroot}%{_datadir}/%{name}/%{grubxenarch}/grub.xen %{buildroot}%{_libdir}/%{name}/%{grubxenarch}/grub.xen
cat <<-EoM >%{buildroot}%{_libdir}/%{name}/%{grubxenarch}/DEPRECATED
	This directory and its contents was moved to %{_datadir}/%{name}/%{grubxenarch}.
	Individual symbolic links are provided for a smooth transition.
	Please update your VM definition files to use the new location!
EoM
cd ..
%endif

%ifarch %{efi}
cd build-efi
%make_install
install -m 644 grub.efi %{buildroot}/%{_datadir}/%{name}/%{grubefiarch}/.
%ifarch x86_64
install -m 644 grub-tpm.efi %{buildroot}/%{_datadir}/%{name}/%{grubefiarch}/.
%endif

# Create grub.efi link to system efi directory
# This is for tools like kiwi not fiddling with the path
%define sysefibasedir %{_datadir}/efi
%define sysefidir %{sysefibasedir}/%{_target_cpu} 
install -d %{buildroot}/%{sysefidir}
ln -sr %{buildroot}/%{_datadir}/%{name}/%{grubefiarch}/grub.efi %{buildroot}%{sysefidir}/grub.efi
%ifarch x86_64
# provide compatibility sym-link for previous shim-install and the like
install -d %{buildroot}/usr/lib64/efi
ln -srf %{buildroot}/%{_datadir}/%{name}/%{grubefiarch}/grub.efi %{buildroot}/usr/lib64/efi/grub.efi
cat <<-EoM >%{buildroot}/usr/lib64/efi/DEPRECATED
	This directory and its contents was moved to %{_datadir}/efi/x86_64.
	Individual symbolic links are provided for a smooth transition and
	may vanish at any point in time.  Please use the new location!
EoM
%endif

%ifarch x86_64 aarch64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
export BRP_PESIGN_FILES="%{_datadir}/%{name}/%{grubefiarch}/grub.efi"
%ifarch x86_64
BRP_PESIGN_FILES="${BRP_PESIGN_FILES} %{_datadir}/%{name}/%{grubefiarch}/grub-tpm.efi"
%endif
install -m 444 grub.der %{buildroot}/%{sysefidir}/
%endif
%endif

cd ..
%endif

%if ! 0%{?only_efi:1}
cd build
%make_install
cd ..
%endif

if [ "%{platform}" = "emu" ]; then
  # emu-lite is currently broken (and not needed), don't install!
  rm -f %{buildroot}/%{_bindir}/%{name}-emu-lite
elif [ -d build-emu/grub-core ]; then
  cd build-emu/grub-core
  install -m 755 grub-emu %{buildroot}/%{_bindir}/%{name}-emu
  if false; then
    # this needs to go to '-emu'-package; until that is ready, don't install!
    install -m 755 grub-emu-lite %{buildroot}/%{_bindir}/%{name}-emu-lite
  else
    rm -f %{buildroot}/%{_bindir}/%{name}-emu-lite
  fi
  install -m 644 grub-emu.1 %{buildroot}/%{_mandir}/man1/%{name}-emu.1
  cd ../..
fi

# *.module files are installed with executable bits due to the way grub2 build
# system works. Clear executable bits to not confuse find-debuginfo.sh
find %{buildroot}/%{_datadir}/%{name} \
       \( -name '*.module' -o -name '*.image' -o -name '*.exec' \) -print0 | \
       xargs --no-run-if-empty -0 chmod a-x

# Script that makes part of grub.cfg persist across updates
install -m 755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/grub.d/

# Script to generate memtest86+ menu entry
install -m 755 %{SOURCE7} %{buildroot}/%{_sysconfdir}/grub.d/

# Ghost config file
install -d %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg

# Remove devel files
rm %{buildroot}/%{_datadir}/%{name}/*/*.h
%if 0%{?suse_version} >= 1140
rm %{buildroot}/%{_datadir}/%{name}/*.h
%endif

# Defaults
install -m 644 -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/default/grub
install -m 755 -D %{SOURCE6} %{buildroot}/%{_sbindir}/grub2-once
install -m 755 -D %{SOURCE12} %{buildroot}/%{_libdir}/snapper/plugins/grub
install -m 755 -D %{SOURCE14} %{buildroot}/%{_sysconfdir}/grub.d/80_suse_btrfs_snapshot
%if 0%{?has_systemd:1}
install -m 644 -D %{SOURCE15} %{buildroot}/%{_unitdir}/grub2-once.service
install -m 755 -D %{SOURCE17} %{buildroot}/%{_libdir}/systemd/system-sleep/grub2.sleep
%endif
install -m 755 -D %{SOURCE18} %{buildroot}/%{_sbindir}/grub2-check-default

R="%{buildroot}"
%ifarch %{ix86} x86_64
%else
rm -f $R%{_sysconfdir}/grub.d/20_memtest86+
%endif

%ifarch ppc ppc64 ppc64le
rm -f $R%{_sysconfdir}/grub.d/95_textmode
%else
rm -f $R%{_sysconfdir}/grub.d/20_ppc_terminfo
%endif

%ifarch s390x
mv $R%{_sysconfdir}/{grub.d,default}/zipl2grub.conf.in
chmod 600 $R%{_sysconfdir}/default/zipl2grub.conf.in

%define dracutlibdir %{_prefix}/lib/dracut
%define dracutgrubmoddir %{dracutlibdir}/modules.d/99grub2
install -m 755 -d $R%{dracutgrubmoddir}
for f in module-setup.sh grub2.sh; do
  mv $R%{_datadir}/%{name}/%{grubarch}/dracut-$f $R%{dracutgrubmoddir}/$f
done
mv $R%{_datadir}/%{name}/%{grubarch}/dracut-zipl-refresh \
   $R%{_datadir}/%{name}/zipl-refresh
rm -f $R%{_sysconfdir}/grub.d/30_os-prober

perl -ni -e '
  sub END() {
    print "\n# on s390x always:\nGRUB_DISABLE_OS_PROBER=true\n";
  }
  if ( s{^#?(GRUB_TERMINAL)=(console|gfxterm)}{$1=console} ) {
    $_ .= "GRUB_GFXPAYLOAD_LINUX=text\n";
  }
  if (	m{^# The resolution used on graphical} ||
	m{^# # note that you can use only modes} ||
	m{^# you can see them in real GRUB} ||
	m{^#?GRUB_GFXMODE=} ) {
    next;
  }
  s{openSUSE}{SUSE Linux Enterprise Server} if (m{^GRUB_DISTRIBUTOR});
  print;
'  %{buildroot}/%{_sysconfdir}/default/grub
%else
%endif

%find_lang %{name}
%fdupes %buildroot%{_bindir}
%fdupes %buildroot%{_libdir}
%fdupes %buildroot%{_datadir}

%pre
%service_add_pre grub2-once.service

%post
%service_add_post grub2-once.service

%if ! 0%{?only_efi:1}

%post %{grubarch}
%if 0%{?update_bootloader_check_type_reinit_post:1} 
%update_bootloader_check_type_reinit_post grub2
%else
# To check by current loader settings
if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
  . %{_sysconfdir}/sysconfig/bootloader
fi

# If the grub is the current loader, we'll handle the grub2 testing entry
if [ "x${LOADER_TYPE}" = "xgrub" ]; then

  exec >/dev/null 2>&1

  # check if entry for grub2's core.img exists in the config
  # if yes, we will correct obsoleted path and update grub2 stuff and config to make it work
  # if no, do nothing
  if [ -f /boot/grub/menu.lst ]; then

    # If grub config contains obsolete core.img path, remove and use the new one
    if /usr/bin/grep -l "^\s*kernel\s*.*/boot/%{name}/core.img" /boot/grub/menu.lst; then
      /sbin/update-bootloader --remove --image /boot/%{name}/core.img || true
      /sbin/update-bootloader --add --image /boot/%{name}/i386-pc/core.img --name "GNU GRUB 2" || true
    fi

    # Install grub2 stuff and config to make the grub2 testing entry to work with updated version
    if /usr/bin/grep -l "^\s*kernel\s*.*/boot/%{name}/i386-pc/core.img" /boot/grub/menu.lst; then
      # Determine the partition with /boot
      BOOT_PARTITION=$(df -h /boot | sed -n '2s/[[:blank:]].*//p')
      # Generate core.img, but don't let it be installed in boot sector
      %{name}-install --no-bootsector $BOOT_PARTITION || true
      # Create a working grub2 config, otherwise that entry is un-bootable
      /usr/sbin/grub2-mkconfig -o /boot/%{name}/grub.cfg
    fi
  fi

elif [ "x${LOADER_TYPE}" = "xgrub2" ]; then

  # It's enought to call update-bootloader to install grub2 and update it's config
  # Use new --reinit, if not available use --refresh
  # --reinit: install and update bootloader config
  # --refresh: update bootloader config
  /sbin/update-bootloader --reinit 2>&1 | grep -q 'Unknown option: reinit' &&
  /sbin/update-bootloader --refresh || true
fi
%endif

%posttrans %{grubarch}
%{?update_bootloader_posttrans}

%endif

%ifarch %{efi}

%post %{grubefiarch}
%if 0%{?update_bootloader_check_type_reinit_post:1} 
%update_bootloader_check_type_reinit_post grub2-efi
%else
# To check by current loader settings
if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
  . %{_sysconfdir}/sysconfig/bootloader
fi

if [ "x${LOADER_TYPE}" = "xgrub2-efi" ]; then

  if [ -d /boot/%{name}-efi ]; then
    # Migrate settings to standard prefix /boot/grub2
    for i in custom.cfg grubenv; do
      [ -f /boot/%{name}-efi/$i ] && cp -a /boot/%{name}-efi/$i /boot/%{name} || :
    done

  fi

  # It's enough to call update-bootloader to install grub2 and update it's config
  # Use new --reinit, if not available use --refresh
  # --reinit: install and update bootloader config
  # --refresh: update bootloader config
  /sbin/update-bootloader --reinit 2>&1 | grep -q 'Unknown option: reinit' &&
  /sbin/update-bootloader --refresh || true
fi

if [ -d /boot/%{name}-efi ]; then
  mv /boot/%{name}-efi /boot/%{name}-efi.rpmsave
fi

exit 0
%endif

%posttrans %{grubefiarch}
%{?update_bootloader_posttrans}

%endif

%preun
%service_del_preun grub2-once.service
# We did not add core.img to grub1 menu.lst in new update-bootloader macro as what
# the old %%post ever did, then the %%preun counterpart which removed the added core.img
# entry from old %%post can be skipped entirely if having new macro in use.
%if ! 0%{?update_bootloader_posttrans:1}%{?only_efi:1}
if [ $1 = 0 ]; then
  # To check by current loader settings
  if [ -f %{_sysconfdir}/sysconfig/bootloader ]; then
    . %{_sysconfdir}/sysconfig/bootloader
  fi

  if [ "x${LOADER_TYPE}" = "xgrub" ]; then

    exec >/dev/null 2>&1

    if [ -f /boot/grub/menu.lst ]; then

      # Remove grub2 testing entry in menu.lst if has any
      for i in /boot/%{name}/core.img /boot/%{name}/i386-pc/core.img; do
        if /usr/bin/grep -l "^\s*kernel\s*.*$i" /boot/grub/menu.lst; then
          /sbin/update-bootloader --remove --image "$i" || true
        fi
      done
    fi

    # Cleanup config, to not confuse some tools determining bootloader in use
    rm -f /boot/%{name}/grub.cfg

    # Cleanup installed files
    # Unless grub2 provides grub2-uninstall, we don't remove any file because
    # we have no idea what's been installed. (And a blind remove is dangerous
    # to remove user's or other package's file accidently ..)
  fi
fi
%endif

%postun
%service_del_postun grub2-once.service

%files -f %{name}.lang
%defattr(-,root,root,-)
%if 0%{?suse_version} < 1500
%doc COPYING
%else
%license COPYING
%endif
%doc NEWS README
%doc THANKS TODO ChangeLog
%doc docs/autoiso.cfg docs/osdetect.cfg
%ifarch s390x
%doc README.ibm3215
%endif
%dir /boot/%{name}
%ghost /boot/%{name}/grub.cfg
%{_sysconfdir}/bash_completion.d/grub
%config(noreplace) %{_sysconfdir}/default/grub
%dir %{_sysconfdir}/grub.d
%{_sysconfdir}/grub.d/README
%config(noreplace) %{_sysconfdir}/grub.d/00_header
%config(noreplace) %{_sysconfdir}/grub.d/10_linux
%config(noreplace) %{_sysconfdir}/grub.d/20_linux_xen
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%config(noreplace) %{_sysconfdir}/grub.d/90_persistent
%ifnarch ppc ppc64 ppc64le
%config(noreplace) %{_sysconfdir}/grub.d/95_textmode
%endif
%ifarch %{ix86} x86_64
%config(noreplace) %{_sysconfdir}/grub.d/20_memtest86+
%endif
%ifarch ppc ppc64 ppc64le
%config(noreplace) %{_sysconfdir}/grub.d/20_ppc_terminfo
%endif
%ifarch s390x
%config(noreplace) %{_sysconfdir}/default/zipl2grub.conf.in
%{dracutlibdir}
%{_sbindir}/%{name}-zipl-setup
%{_datadir}/%{name}/zipl-refresh
%endif
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-once
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-check-default
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-file
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-mkrescue
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-syslinux2cfg
%if 0%{?has_systemd:1}
%{_unitdir}/grub2-once.service
%endif
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/themes
%if 0%{?suse_version} >= 1140
%{_datadir}/%{name}/*.pf2
%endif
%{_datadir}/%{name}/grub-mkconfig_lib
%{_infodir}/grub-dev.info*
%{_infodir}/%{name}.info*
%{_mandir}/man1/%{name}-editenv.1.*
%{_mandir}/man1/%{name}-file.1.*
%{_mandir}/man1/%{name}-fstest.1.*
%{_mandir}/man1/%{name}-kbdcomp.1.*
%{_mandir}/man1/%{name}-menulst2cfg.1.*
%{_mandir}/man1/%{name}-mkfont.1.*
%{_mandir}/man1/%{name}-mkimage.1.*
%{_mandir}/man1/%{name}-mklayout.1.*
%{_mandir}/man1/%{name}-mknetdir.1.*
%{_mandir}/man1/%{name}-mkpasswd-pbkdf2.1.*
%{_mandir}/man1/%{name}-mkrelpath.1.*
%{_mandir}/man1/%{name}-mkrescue.1.*
%{_mandir}/man1/%{name}-mkstandalone.1.*
%{_mandir}/man1/%{name}-render-label.1.*
%{_mandir}/man1/%{name}-script-check.1.*
%{_mandir}/man1/%{name}-syslinux2cfg.1.*
%{_mandir}/man8/%{name}-install.8.*
%{_mandir}/man8/%{name}-mkconfig.8.*
%{_mandir}/man8/%{name}-probe.8.*
%{_mandir}/man8/%{name}-reboot.8.*
%{_mandir}/man8/%{name}-set-default.8.*
%if %{emu}
%{_bindir}/%{name}-emu
%{_mandir}/man1/%{name}-emu.1.*
%endif
%ifnarch s390x
%config(noreplace) %{_sysconfdir}/grub.d/30_os-prober
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-mount
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-sparc64-setup
%{_mandir}/man1/%{name}-glue-efi.1.*
%{_mandir}/man1/%{name}-mount.1.*
%{_mandir}/man8/%{name}-bios-setup.8.*
%{_mandir}/man8/%{name}-macbless.8.*
%{_mandir}/man8/%{name}-ofpathname.8.*
%{_mandir}/man8/%{name}-sparc64-setup.8.*
%endif

%files branding-upstream
%defattr(-,root,root,-)
%{_datadir}/%{name}/themes/starfield

%if ! 0%{?only_efi:1}

%files %{grubarch}
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/%{grubarch}
%ifarch ppc ppc64 ppc64le
# This is intentionally "grub.chrp" and not "%%{name}.chrp"
%{_datadir}/%{name}/%{grubarch}/grub.chrp
%{_datadir}/%{name}/%{grubarch}/bootinfo.txt
%endif
%ifnarch ppc ppc64 ppc64le s390x %{arm}
%{_datadir}/%{name}/%{grubarch}/*.image
%endif
%{_datadir}/%{name}/%{grubarch}/*.img
%{_datadir}/%{name}/%{grubarch}/*.lst
%{_datadir}/%{name}/%{grubarch}/*.mod
%ifarch x86_64
%{_datadir}/%{name}/%{grubarch}/efiemu*.o
%endif
%{_datadir}/%{name}/%{grubarch}/kernel.exec
%{_datadir}/%{name}/%{grubarch}/modinfo.sh

%files %{grubarch}-debug
%defattr(-,root,root,-)
%{_datadir}/%{name}/%{grubarch}/gdb_grub
%{_datadir}/%{name}/%{grubarch}/gmodule.pl
%{_datadir}/%{name}/%{grubarch}/*.module

%endif

%ifarch %{efi}

%files %{grubefiarch}
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/%{grubefiarch}
%{_datadir}/%{name}/%{grubefiarch}/grub.efi
%ifarch x86_64
%{_datadir}/%{name}/%{grubefiarch}/grub-tpm.efi
%endif
%{_datadir}/%{name}/%{grubefiarch}/*.img
%{_datadir}/%{name}/%{grubefiarch}/*.lst
%{_datadir}/%{name}/%{grubefiarch}/*.mod
%{_datadir}/%{name}/%{grubefiarch}/kernel.exec
%{_datadir}/%{name}/%{grubefiarch}/modinfo.sh
%dir %{sysefibasedir}
%dir %{sysefidir}
%{sysefidir}/grub.efi
%if 0%{?suse_version} < 1600
%ifarch x86_64
# provide compatibility sym-link for previous shim-install and kiwi
%dir /usr/lib64/efi
/usr/lib64/efi/DEPRECATED
/usr/lib64/efi/grub.efi
%endif
%endif

%ifarch x86_64 aarch64
%if 0%{?suse_version} >= 1230 || 0%{?suse_version} == 1110
%{sysefidir}/grub.der
%endif
%endif

%files %{grubefiarch}-debug
%defattr(-,root,root,-)
%{_datadir}/%{name}/%{grubefiarch}/gdb_grub
%{_datadir}/%{name}/%{grubefiarch}/gmodule.pl
%{_datadir}/%{name}/%{grubefiarch}/*.module

%endif

%files snapper-plugin
%defattr(-,root,root,-)
%dir %{_libdir}/snapper
%dir %{_libdir}/snapper/plugins
%config(noreplace) %{_sysconfdir}/grub.d/80_suse_btrfs_snapshot
%{_libdir}/snapper/plugins/grub

%ifarch %{ix86} x86_64
%files %{grubxenarch}
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/%{grubxenarch}
%{_datadir}/%{name}/%{grubxenarch}/*
# provide compatibility sym-link for VM definitions pointing to old location
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{grubxenarch}
%endif

%if 0%{?has_systemd:1}
%files systemd-sleep-plugin
%defattr(-,root,root,-)
%dir %{_libdir}/systemd/system-sleep
%{_libdir}/systemd/system-sleep/grub2.sleep
%endif

%changelog
* Thu Mar 11 2021 Michael Chang <mchang@suse.com>
- Fix chainloading windows on dual boot machine (bsc#1183073)
  * 0001-kern-efi-sb-Add-chainloaded-image-as-shim-s-verifiab.patch
* Fri Feb 26 2021 Michael Chang <mchang@suse.com>
- VUL-0: grub2,shim: implement new SBAT method (bsc#1182057)
  * 0031-util-mkimage-Remove-unused-code-to-add-BSS-section.patch
  * 0032-util-mkimage-Use-grub_host_to_target32-instead-of-gr.patch
  * 0033-util-mkimage-Always-use-grub_host_to_target32-to-ini.patch
  * 0034-util-mkimage-Unify-more-of-the-PE32-and-PE32-header-.patch
  * 0035-util-mkimage-Reorder-PE-optional-header-fields-set-u.patch
  * 0036-util-mkimage-Improve-data_size-value-calculation.patch
  * 0037-util-mkimage-Refactor-section-setup-to-use-a-helper.patch
  * 0038-util-mkimage-Add-an-option-to-import-SBAT-metadata-i.patch
  * 0039-grub-install-common-Add-sbat-option.patch
- Fix CVE-2021-20225 (bsc#1182262)
  * 0022-lib-arg-Block-repeated-short-options-that-require-an.patch
- Fix CVE-2020-27749 (bsc#1179264)
  * 0024-kern-parser-Fix-resource-leak-if-argc-0.patch
  * 0025-kern-parser-Fix-a-memory-leak.patch
  * 0026-kern-parser-Introduce-process_char-helper.patch
  * 0027-kern-parser-Introduce-terminate_arg-helper.patch
  * 0028-kern-parser-Refactor-grub_parser_split_cmdline-clean.patch
  * 0029-kern-buffer-Add-variable-sized-heap-buffer.patch
  * 0030-kern-parser-Fix-a-stack-buffer-overflow.patch
- Fix CVE-2021-20233 (bsc#1182263)
  * 0023-commands-menuentry-Fix-quoting-in-setparams_prefix.patch
- Fix CVE-2020-25647 (bsc#1177883)
  * 0021-usb-Avoid-possible-out-of-bound-accesses-caused-by-m.patch
- Fix CVE-2020-25632 (bsc#1176711)
  * 0020-dl-Only-allow-unloading-modules-that-are-not-depende.patch
- Fix CVE-2020-27779, CVE-2020-14372 (bsc#1179265) (bsc#1175970)
  * 0001-include-grub-i386-linux.h-Include-missing-grub-types.patch
  * 0002-efi-Make-shim_lock-GUID-and-protocol-type-public.patch
  * 0003-efi-Return-grub_efi_status_t-from-grub_efi_get_varia.patch
  * 0004-efi-Add-a-function-to-read-EFI-variables-with-attrib.patch
  * 0005-efi-Add-secure-boot-detection.patch
  * 0006-efi-Only-register-shim_lock-verifier-if-shim_lock-pr.patch
  * 0007-verifiers-Move-verifiers-API-to-kernel-image.patch
  * 0008-efi-Move-the-shim_lock-verifier-to-the-GRUB-core.patch
  * 0009-kern-Add-lockdown-support.patch
  * 0010-kern-lockdown-Set-a-variable-if-the-GRUB-is-locked-d.patch
  * 0011-efi-Lockdown-the-GRUB-when-the-UEFI-Secure-Boot-is-e.patch
  * 0012-efi-Use-grub_is_lockdown-instead-of-hardcoding-a-dis.patch
  * 0013-acpi-Don-t-register-the-acpi-command-when-locked-dow.patch
  * 0014-mmap-Don-t-register-cutmem-and-badram-commands-when-.patch
  * 0015-commands-Restrict-commands-that-can-load-BIOS-or-DT-.patch
  * 0016-commands-setpci-Restrict-setpci-command-when-locked-.patch
  * 0017-commands-hdparm-Restrict-hdparm-command-when-locked-.patch
  * 0018-gdb-Restrict-GDB-access-when-locked-down.patch
  * 0019-loader-xnu-Don-t-allow-loading-extension-and-package.patch
  * 0040-shim_lock-Only-skip-loading-shim_lock-verifier-with-.patch
  * 0041-squash-Add-secureboot-support-on-efi-chainloader.patch
  * 0042-squash-grub2-efi-chainload-harder.patch
  * 0043-squash-Don-t-allow-insmod-when-secure-boot-is-enable.patch
  * 0044-squash-kern-Add-lockdown-support.patch
  * 0045-squash-Add-support-for-Linux-EFI-stub-loading-on-aar.patch
  * 0046-squash-verifiers-Move-verifiers-API-to-kernel-image.patch
- Drop patch supersceded by the new backport
  * 0001-linuxefi-fail-kernel-validation-without-shim-protoco.patch
  * 0001-shim_lock-Disable-GRUB_VERIFY_FLAGS_DEFER_AUTH-if-se.patch
  * 0007-linuxefi-fail-kernel-validation-without-shim-protoco.patch
- Add SBAT metadata section to grub.efi
- Drop shim_lock module as it is part of core of grub.efi
  * grub2.spec
* Mon Feb 22 2021 Michael Chang <mchang@suse.com>
- Fix build error in binutils 2.36 (bsc#1181741)
  * 0001-Fix-build-error-in-binutils-2.36.patch
- Fix executable stack in grub-emu (bsc#1181696)
  * 0001-emu-fix-executable-stack-marking.patch
* Thu Feb 18 2021 Michael Chang <mchang@suse.com>
- Restore compatibilty sym-links
  * grub2.spec
- Use rpmlintrc to filter out rpmlint 2.0 error (bsc#1179044)
  * grub2.rpmlintrc
* Wed Jan 27 2021 Michael Chang <mchang@suse.com>
- Complete Secure Boot support on aarch64 (jsc#SLE-15020)
  * 0001-Add-support-for-Linux-EFI-stub-loading-on-aarch64.patch
  * 0002-arm64-make-sure-fdt-has-address-cells-and-size-cells.patch
  * 0003-Make-grub_error-more-verbose.patch
  * 0004-arm-arm64-loader-Better-memory-allocation-and-error-.patch
  * 0005-Make-linux_arm_kernel_header.hdr_offset-be-at-the-ri.patch
  * 0006-efi-Set-image-base-address-before-jumping-to-the-PE-.patch
  * 0007-linuxefi-fail-kernel-validation-without-shim-protoco.patch
  * 0008-squash-Add-support-for-Linux-EFI-stub-loading-on-aar.patch
  * 0009-squash-Add-support-for-linuxefi.patch
* Thu Jan 21 2021 Michael Chang <mchang@suse.com>
- Fix rpmlint 2.0 error for having arch specific path in noarch package aiming
  for compatibility with old package (bsc#1179044)
  * grub2.spec
- Fix non POSIX sed argument which failed in sed from busybox (bsc#1181091)
  * grub2-check-default.sh
* Mon Nov  2 2020 Michael Chang <mchang@suse.com>
- Fix boot failure in blocklist installation (bsc#1178278)
  * Modified 0002-grub-install-Avoid-incompleted-install-on-i386-pc.patch
* Thu Oct 22 2020 Michael Chang <mchang@suse.com>
- Fix grub2-install error with "failed to get canonical path of
  `/boot/grub2/i386-pc'." (bsc#1177957)
  * Modified 0002-grub-install-Avoid-incompleted-install-on-i386-pc.patch
* Wed Oct 14 2020 Michael Chang <mchang@suse.com>
- Fix https boot interrupted by unrecognised network address error message
  (bsc#1172952)
  * 0001-add-support-for-UEFI-network-protocols.patch
* Tue Oct 13 2020 Michael Chang <mchang@suse.com>
- grub2.spec: Fix bare words used as string in expression which is no longer
  allowed in rpm 4.16
* Fri Sep 25 2020 Michael Chang <mchang@suse.com>
- Improve the error handling when grub2-install fails with short mbr gap
  (bsc#1176062)
  * 0001-Warn-if-MBR-gap-is-small-and-user-uses-advanced-modu.patch
  * 0002-grub-install-Avoid-incompleted-install-on-i386-pc.patch
* Wed Sep  9 2020 Michael Chang <mchang@suse.com>
- Make efi hand off the default entry point of the linux command (bsc#1176134)
  * 0001-efi-linux-provide-linux-command.patch
* Thu Aug 27 2020 Michael Chang <mchang@suse.com>
- Fix verification requested but nobody cares error when loading external
  module in secure boot off (bsc#1175766)
  * 0001-shim_lock-Disable-GRUB_VERIFY_FLAGS_DEFER_AUTH-if-se.patch
* Sat Aug 22 2020 Michael Chang <mchang@suse.com>
- Make consistent check to enable relative path on btrfs (bsc#1174567)
  * 0001-Unify-the-check-to-enable-btrfs-relative-path.patch
* Fri Aug 21 2020 Michael Chang <mchang@suse.com>
- Add fibre channel device's ofpath support to grub-ofpathname and search hint
  to speed up root device discovery (bsc#1172745)
  * 0001-ieee1275-powerpc-implements-fibre-channel-discovery-.patch
  * 0002-ieee1275-powerpc-enables-device-mapper-discovery.patch
* Tue Aug 18 2020 Michael Chang <mchang@suse.com>
- Fix for CVE-2020-15705 (bsc#1174421)
  * 0001-linuxefi-fail-kernel-validation-without-shim-protoco.patch
  * 0002-cmdline-Provide-cmdline-functions-as-module.patch
* Thu Aug 13 2020 Michael Chang <mchang@suse.com>
- Make grub-calloc inline to avoid symbol not found error as the system may not
  use updated grub to boot the system (bsc#1174782) (bsc#1175060) (bsc#1175036)
  * 0001-kern-mm.c-Make-grub_calloc-inline.patch
* Mon Jul 27 2020 Michael Chang <mchang@suse.com>
- Fix for CVE-2020-10713 (bsc#1168994)
  * 0001-yylex-Make-lexer-fatal-errors-actually-be-fatal.patch
- Fix for CVE-2020-14308 CVE-2020-14309, CVE-2020-14310, CVE-2020-14311
  (bsc#1173812)
  * 0002-safemath-Add-some-arithmetic-primitives-that-check-f.patch
  * 0003-calloc-Make-sure-we-always-have-an-overflow-checking.patch
  * 0004-calloc-Use-calloc-at-most-places.patch
  * 0005-malloc-Use-overflow-checking-primitives-where-we-do-.patch
  * 0006-iso9660-Don-t-leak-memory-on-realloc-failures.patch
  * 0007-font-Do-not-load-more-than-one-NAME-section.patch
- Fix CVE-2020-15706 (bsc#1174463)
  * 0008-script-Remove-unused-fields-from-grub_script_functio.patch
  * 0009-script-Avoid-a-use-after-free-when-redefining-a-func.patch
- Fix CVE-2020-15707 (bsc#1174570)
  * 0010-linux-Fix-integer-overflows-in-initrd-size-handling.patch
- Use overflow checking primitives where the arithmetic expression for buffer
  allocations may include unvalidated data
- Use grub_calloc for overflow check and return NULL when it would occur
  * 0001-add-support-for-UEFI-network-protocols.patch
  * 0003-bootp-New-net_bootp6-command.patch
  * grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  * grub2-btrfs-09-get-default-subvolume.patch
  * grub2-gfxmenu-support-scrolling-menu-entry-s-text.patch
  * grub2-grubenv-in-btrfs-header.patch
* Thu Jul 16 2020 Michel Normand <normand@linux.vnet.ibm.com>
- No 95_textmode for PowerPC (boo#1174166)
* Mon May 18 2020 Michael Chang <mchang@suse.com>
- Skip zfcpdump kernel from the grub boot menu (bsc#1166513)
  * grub2-s390x-skip-zfcpdump-image.patch
* Tue May  5 2020 Michael Chang <mchang@suse.com>
- Fix boot failure as journaled data not get drained due to abrupt power
  off after grub-install (bsc#1167756)
  * grub-install-force-journal-draining-to-ensure-data-i.patch
* Thu Apr 16 2020 Michael Chang <mchang@suse.com>
- Fix executable stack in grub-probe and other grub utility (bsc#1169137)
  * grub2-btrfs-06-subvol-mount.patch
* Tue Mar 24 2020 Michael Chang <mchang@suse.com>
- Fix GCC 10 build fail (bsc#1158189)
  * 0001-mdraid1x_linux-Fix-gcc10-error-Werror-array-bounds.patch
  * 0002-zfs-Fix-gcc10-error-Werror-zero-length-bounds.patch
* Fri Mar 20 2020 Michael Chang <mchang@suse.com>
- Backport to support searching for specific config files for netboot
  (bsc#1166409)
  * 0001-normal-Move-common-datetime-functions-out-of-the-nor.patch
  * 0002-kern-Add-X-option-to-printf-functions.patch
  * 0003-normal-main-Search-for-specific-config-files-for-net.patch
  * 0004-datetime-Enable-the-datetime-module-for-the-emu-plat.patch
* Mon Mar 16 2020 Ludwig Nussel <lnussel@suse.de>
- move *.module files to separate -debug subpackage (boo#1166578)
* Thu Mar 12 2020 Fabian Vogt <fvogt@suse.com>
- Fix EFI console detection to make it a runtime decision (bsc#1164385)
  * grub2-SUSE-Add-the-t-hotkey.patch
* Tue Mar 10 2020 Ludwig Nussel <lnussel@suse.de>
- Downgrade mtools to Suggests for consistency with xorriso (boo#1165839)
- remove info requirements, file triggers are used now (boo#1152105)
* Fri Feb 28 2020 rw@suse.com
- Add secure boot support for s390x.  (jsc#SLE-9425)
  * grub2-s390x-11-secureboot.patch
* Tue Feb 18 2020 Michael Chang <mchang@suse.com>
- Fix grub hangs after loading rogue image without valid signature for uefi
  secure boot (bsc#1159102)
  * grub2-verifiers-fix-system-freeze-if-verify-failed.patch
* Tue Feb  4 2020 Michael Chang <mchang@suse.com>
- From Stefan Seyfried <seife@novell.slipkontur.de> : Fix grub2-install fails
  with "not a directory" error (boo#1161641, bsc#1162403)
  * grub2-install-fix-not-a-directory-error.patch
* Wed Nov 27 2019 olaf@aepfle.de
- Correct awk pattern in 20_linux_xen (bsc#900418, bsc#1157912)
- Correct linux and initrd handling in 20_linux_xen (bsc#1157912)
  M grub2-efi-xen-cfg-unquote.patch
  M grub2-efi-xen-chainload.patch
  M grub2-efi-xen-cmdline.patch
  M grub2-efi-xen-removable.patch
* Wed Oct 30 2019 Michael Chang <mchang@suse.com>
- Disable btrfs zstd support for i386-pc to workaround core.img too large to be
  embedded in btrfs bootloader area or MBR gap (boo#1154809)
  * 0001-btrfs-disable-zstd-support-for-i386-pc.patch
* Mon Oct 28 2019 Bernhard Wiedemann <bwiedemann@suse.com>
- Fix grub2.sleep to load old kernel after hibernation (boo#1154783)
* Tue Oct 22 2019 Andreas Schwab <schwab@suse.de>
- Enable support for riscv64
- Backports from upstream:
  * risc-v-fix-computation-of-pc-relative-relocation-offset.patch
  * risc-v-add-clzdi2-symbol.patch
  * grub-install-define-default-platform-for-risc-v.patch
* Thu Oct 17 2019 Michael Chang <mchang@suse.com>
- Version bump to 2.04
  * removed
  - translations-20170427.tar.xz
  * grub2.spec
  - Make signed grub-tpm.efi specific to x86_64-efi build, the platform
    currently shipped with tpm module from upstream codebase
  - Add shim_lock to signed grub.efi in x86_64-efi build
  - x86_64: linuxefi now depends on linux, both will verify kernel via
    shim_lock
  - Remove translation tarball and po file hacks as it's been included in
    upstream tarball
  * rediff
  - grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
  - grub2-commands-introduce-read_file-subcommand.patch
  - grub2-secureboot-add-linuxefi.patch
  - 0001-add-support-for-UEFI-network-protocols.patch
  - grub2-efi-HP-workaround.patch
  - grub2-secureboot-install-signed-grub.patch
  - grub2-linux.patch
  - use-grub2-as-a-package-name.patch
  - grub2-pass-corret-root-for-nfsroot.patch
  - grub2-secureboot-use-linuxefi-on-uefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - grub2-secureboot-provide-linuxefi-config.patch
  - grub2-secureboot-chainloader.patch
  - grub2-s390x-01-Changes-made-and-files-added-in-order-to-allow-s390x.patch
  - grub2-s390x-02-kexec-module-added-to-emu.patch
  - grub2-s390x-04-grub2-install.patch
  - grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  - grub2-efi-chainloader-root.patch
  - grub2-ppc64le-disable-video.patch
  - grub2-ppc64-cas-reboot-support.patch
  - grub2-Fix-incorrect-netmask-on-ppc64.patch
  - 0003-bootp-New-net_bootp6-command.patch
  - 0006-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
  - 0012-tpm-Build-tpm-as-module.patch
  - grub2-emu-4-all.patch
  - grub2-btrfs-09-get-default-subvolume.patch
  - grub2-ppc64le-memory-map.patch
  - grub2-ppc64-cas-fix-double-free.patch
  - 0008-efinet-Setting-DNS-server-from-UEFI-protocol.patch
  * drop upstream patches
  - grub2-fix-locale-en.mo.gz-not-found-error-message.patch
  - grub2-fix-build-with-flex-2.6.4.patch
  - grub2-accept-empty-module.patch
  - 0001-Fix-packed-not-aligned-error-on-GCC-8.patch
  - 0001-Fix-PCIe-LER-when-GRUB2-accesses-non-enabled-MMIO-da.patch
  - unix-exec-avoid-atexit-handlers-when-child-exits.patch
  - 0001-xfs-Accept-filesystem-with-sparse-inodes.patch
  - grub2-binutils2.31.patch
  - grub2-msdos-fix-overflow.patch
  - 0001-tsc-Change-default-tsc-calibration-method-to-pmtimer.patch
  - grub2-efi-Move-grub_reboot-into-kernel.patch
  - grub2-efi-Free-malloc-regions-on-exit.patch
  - grub2-move-initrd-upper.patch
  - 0002-Add-Virtual-LAN-support.patch
  - 0001-ofnet-Initialize-structs-in-bootpath-parser.patch
  - 0001-misc-fix-invalid-character-recongition-in-strto-l.patch
  - 0001-tpm-Core-TPM-support.patch
  - 0002-tpm-Measure-kernel-initrd.patch
  - 0003-tpm-Add-BIOS-boot-measurement.patch
  - 0004-tpm-Rework-linux-command.patch
  - 0005-tpm-Rework-linux16-command.patch
  - 0006-tpm-Measure-kernel-and-initrd-on-BIOS-systems.patch
  - 0007-tpm-Measure-the-kernel-commandline.patch
  - 0008-tpm-Measure-commands.patch
  - 0009-tpm-Measure-multiboot-images-and-modules.patch
  - 0010-tpm-Fix-boot-when-there-s-no-TPM.patch
  - 0011-tpm-Fix-build-error.patch
  - 0013-tpm-i386-pc-diskboot-img.patch
  - grub2-freetype-pkgconfig.patch
  - 0001-cpio-Disable-gcc9-Waddress-of-packed-member.patch
  - 0002-jfs-Disable-gcc9-Waddress-of-packed-member.patch
  - 0003-hfs-Fix-gcc9-error-Waddress-of-packed-member.patch
  - 0004-hfsplus-Fix-gcc9-error-with-Waddress-of-packed-membe.patch
  - 0005-acpi-Fix-gcc9-error-Waddress-of-packed-member.patch
  - 0006-usbtest-Disable-gcc9-Waddress-of-packed-member.patch
  - 0007-chainloader-Fix-gcc9-error-Waddress-of-packed-member.patch
  - 0008-efi-Fix-gcc9-error-Waddress-of-packed-member.patch
* Tue Oct 15 2019 rw@suse.com
- Consistently find btrfs snapshots on s390x.  (bsc#1136970)
  * grub2-s390x-04-grub2-install.patch
* Fri Aug 16 2019 Michael Chang <mchang@suse.com>
- Fix fallback embed doesn't work when no post mbr gap at all (boo#1142229)
  * Refresh grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
* Thu Jul 18 2019 mchang@suse.com
- Revert grub2-ieee1275-FCP-methods-for-WWPN-and-LUNs.patch until merged by
  upstream (bsc#1134287, bsc#1139345, LTC#177836, LTC#174229).
* Mon Jun 24 2019 Michal Suchanek <msuchanek@suse.de>
- Fix iteration of FCP LUNs (bsc#1134287, bsc#1139345, LTC#177836, LTC#174229).
  * Refresh grub2-ieee1275-FCP-methods-for-WWPN-and-LUNs.patch
* Mon Jun 17 2019 mchang@suse.com
- Use grub2-install to handle signed grub installation for UEFI secure
  boot and also provide options to override default (bsc#1136601)
  * grub2-secureboot-install-signed-grub.patch
- Remove arm64 linuxefi patches as it's not needed for secure boot
  * 0001-efi-refactor-grub_efi_allocate_pages.patch
  * 0002-Remove-grub_efi_allocate_pages.patch
  * 0003-arm64-efi-move-EFI_PAGE-definitions-to-efi-memory.h.patch
  * 0004-efi-Add-central-copy-of-grub_efi_find_mmap_size.patch
  * 0005-efi-Add-grub_efi_get_ram_base-function-for-arm64.patch
  * 0006-Add-support-for-EFI-handover-on-ARM64.patch
* Fri Jun 14 2019 mchang@suse.com
- Avoid high resolution when trying to keep current mode (bsc#1133842)
  * grub2-video-limit-the-resolution-for-fixed-bimap-font.patch
- Make GRUB_SAVEDEFAULT working with btrfs (bsc#1128592)
  * grub2-grubenv-in-btrfs-header.patch
* Fri May 17 2019 rw@suse.com
- Check/refresh zipl-kernel before hibernate on s390x.  (bsc#940457)
  (Getting rid of hardcoded 'vmlinuz', which failed on PPC as well.)
  * grub2-systemd-sleep.sh
* Fri May 17 2019 rw@suse.com
- Try to refresh zipl-kernel on failed kexec.  (bsc#1127293)
  * grub2-s390x-04-grub2-install.patch
- Fully support "previous" zipl-kernel,
  with 'mem=1G' being available on dedicated entries.  (bsc#928131)
  * grub2-s390x-09-improve-zipl-setup.patch
- Refresh
  * grub2-zipl-setup-fix-btrfs-multipledev.patch
* Fri May  3 2019 mchang <mchang@suse.com>
- Fix GCC 9 build failure (bsc#1121208)
  * 0001-cpio-Disable-gcc9-Waddress-of-packed-member.patch
  * 0002-jfs-Disable-gcc9-Waddress-of-packed-member.patch
  * 0003-hfs-Fix-gcc9-error-Waddress-of-packed-member.patch
  * 0004-hfsplus-Fix-gcc9-error-with-Waddress-of-packed-membe.patch
  * 0005-acpi-Fix-gcc9-error-Waddress-of-packed-member.patch
  * 0006-usbtest-Disable-gcc9-Waddress-of-packed-member.patch
  * 0007-chainloader-Fix-gcc9-error-Waddress-of-packed-member.patch
  * 0008-efi-Fix-gcc9-error-Waddress-of-packed-member.patch
* Tue Mar 19 2019 mchang <mchang@suse.com>
- Use %%doc for older products for compatibility, or may end up with
  unsuccessful build result
  * grub2.spec
* Tue Mar 19 2019 mchang <mchang@suse.com>
- Revert grub2-ieee1275-open-raw-mode.patch for regression of crashing lvm on
  multipath SAN (bsc#1113702)
  * deleted grub2-ieee1275-open-raw-mode.patch
- Add exception handling to FCP lun enumeration (bsc#1113702)
  * grub2-ieee1275-FCP-methods-for-WWPN-and-LUNs.patch
* Wed Feb 20 2019 mchang@suse.com
- Fix LOADER_TYPE parsing in grub2-once (boo#1122569)
* Tue Feb 12 2019 mchang@suse.com
- Create compatibility sym-link of grub.xen in the old location to which
  old VM definition is pointing (bsc#1123942)
* Mon Jan 28 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Add patch to fix ARM boot, when kernel become too big:
  * grub2-move-initrd-upper.patch (boo#1123350)
* Fri Jan 25 2019 Jan Engelhardt <jengelh@inai.de>
- Replace old $RPM_* shell vars.
* Fri Jan 25 2019 mchang@suse.com
- Support long menu entry by scrolling its text left and right through
  the key stroke ctrl+l and ctrl+r (FATE#325760)
  * grub2-gfxmenu-support-scrolling-menu-entry-s-text.patch
* Thu Jan 24 2019 mchang@suse.com
- Improved hiDPI device support (FATE#326680)
  * grub2-video-limit-the-resolution-for-fixed-bimap-font.patch
* Wed Jan 23 2019 rw@suse.com
- Build platform-packages 'noarch' and move to '/usr/share/efi'
  for SUSE Manager.  (FATE#326960)
  * grub2-efi-xen-chainload.patch (bsc#1122563)
  * grub2-efi-xen-removable.patch (refresh)
* Thu Dec 20 2018 mchang@suse.com
- Support for UEFI Secure Boot on AArch64 (FATE#326541)
  * 0001-efi-refactor-grub_efi_allocate_pages.patch
  * 0002-Remove-grub_efi_allocate_pages.patch
  * 0003-arm64-efi-move-EFI_PAGE-definitions-to-efi-memory.h.patch
  * 0004-efi-Add-central-copy-of-grub_efi_find_mmap_size.patch
  * 0005-efi-Add-grub_efi_get_ram_base-function-for-arm64.patch
  * 0006-Add-support-for-EFI-handover-on-ARM64.patch
* Mon Nov 26 2018 mchang@suse.com
- Change default tsc calibration method to pmtimer on EFI (bsc#1114754)
  * 0001-tsc-Change-default-tsc-calibration-method-to-pmtimer.patch
* Fri Oct 19 2018 mchang@suse.com
- ieee1275: Fix double free in CAS reboot (bsc#1111955)
  * grub2-ppc64-cas-fix-double-free.patch
* Thu Oct  4 2018 glin@suse.com
- Support NVDIMM device names (bsc#1110073)
  * grub2-getroot-support-nvdimm.patch
* Wed Oct  3 2018 mchang@suse.com
- Translate caret back to space as the initrd stanza could use space to
  delimit multiple files loaded (bsc#1101942)
  * grub2-util-30_os-prober-multiple-initrd.patch
* Wed Sep 26 2018 mchang@suse.com
- ieee1275: implement FCP methods for WWPN and LUNs (bsc#1093145)
  * grub2-ieee1275-FCP-methods-for-WWPN-and-LUNs.patch
* Thu Sep 13 2018 mchang@suse.com
- Fix broken network interface with random address and same name (bsc#1084508)
  * 0001-ofnet-Initialize-structs-in-bootpath-parser.patch
* Fri Aug 31 2018 mchang@suse.com
- Fix outputting invalid btrfs subvol path on non btrfs filesystem due to bogus
  return code handling. (bsc#1106381)
  * modified grub2-btrfs-10-config-directory.patch
* Thu Aug 23 2018 mchang@suse.com
- Fix overflow in sector count calculation (bsc#1105163)
  * grub2-msdos-fix-overflow.patch
* Thu Aug  9 2018 mchang@suse.com
- Downgrade libburnia-tools to suggest as minimal system can't afford pulling
  in tcl/tk and half of the x11 stack (bsc#1102515)
  * modified grub2.spec
* Wed Aug  8 2018 dimstar@opensuse.org
- Add grub2-binutils2.31.patch: x86-64: Treat R_X86_64_PLT32 as
  R_X86_64_PC32. Starting from binutils commit bd7ab16b x86-64
  assembler generates R_X86_64_PLT32, instead of R_X86_64_PC32, for
  32-bit PC-relative branches.  Grub2 should treat R_X86_64_PLT32
  as R_X86_64_PC32.
* Mon Aug  6 2018 josef.moellers@suse.com
- The grubxenarch packages are now architecture-independent.
  [bsc#953297, grub2.spec, grub2-rpmlintrc]
* Tue Jul 24 2018 mchang@suse.com
- Fix config_directory on btrfs to follow path scheme (bsc#1063443)
  * grub2-btrfs-10-config-directory.patch
- Fix grub2-install --root-directory does not work for /boot/grub2/<arch> on
  separate btrfs subvolume (boo#1098420)
  * grub2-btrfs-06-subvol-mount.patch
- Fix setparams doesn't work as expected from boot-last-label NVRAM var, after
  inital CAS reboot on ieee1275 (bsc#1088830)
  * grub2-ppc64-cas-new-scope.patch
* Mon Jul 16 2018 mchang@suse.com
- Fix install on xfs error (bsc#1101283)
  * 0001-xfs-Accept-filesystem-with-sparse-inodes.patch
* Tue Jul 10 2018 jbohac@suse.cz
- grub2.spec: change %%config to %%config(noreplace)
  Don't overwrite user changes to config files on upgrades.
* Wed Jul  4 2018 josef.moellers@suse.com
- Marked %%{_sysconfdir}/grub.d/40_custom as (noreplace)
  [bsc#1079332, grub2.spec]
* Wed Jun 27 2018 josef.moellers@suse.com
- Replace "GRUB_DISABLE_LINUX_RECOVERY" by "GRUB_DISABLE_RECOVERY"
  in /etc/default/grub and remove test from s390x install
  section in upec file.
  [bsc#1042433, grub.default, grub2.spec]
* Wed Jun 20 2018 josef.moellers@suse.com
- Added "# needssslcertforbuild", which got lost somewhere,
  to spec file
  [grub2.spec]
* Fri Jun 15 2018 josef.moellers@suse.com
- Replace confusing menu on btrfs "snapper rollback" by help text.
  [bsc#1027588, grub2-btrfs-help-on-snapper-rollback.patch]
* Thu May 24 2018 kukuk@suse.de
- Use %%license instead of %%doc [bsc#1082318]
* Wed May 16 2018 Thomas.Blume@suse.com
- grub2-emu on s390 keep network during kexec boot (bsc#1089493)
  * grub2-s390x-10-keep-network-at-kexec.patch
* Fri May  4 2018 idonmez@suse.com
- Add grub2-freetype-pkgconfig.patch to fix build with new freetype
  use pkgconfig to find Freetype libraries.
* Tue Apr 17 2018 mchang@suse.com
- Fallback to raw mode if Open Firmware returns invalid ihandler (bsc#1071559)
  * grub2-ieee1275-open-raw-mode.patch
* Thu Apr 12 2018 mchang@suse.com
- Fix error of essential directory not found on UEFI Xen host (bsc#1085842)
  * add grub2-efi-xen-removable.patch
  * rediff grub2-suse-remove-linux-root-param.patch
* Tue Apr 10 2018 jdelvare@suse.de
- Fix corruption of "grub2-install --help" and grub2-install manual
  page (bsc#1086670)
  * unix-exec-avoid-atexit-handlers-when-child-exits.patch
* Mon Apr  2 2018 mchang@suse.com
- Fix Nvidia GPU in legacy I/O slot 2 disappears during system
  startup (bsc#1082914)
  * 0001-Fix-PCIe-LER-when-GRUB2-accesses-non-enabled-MMIO-da.patch
* Fri Mar 30 2018 mchang@suse.com
- Fix packed-not-aligned error on GCC 8 (bsc#1084632)
  * 0001-Fix-packed-not-aligned-error-on-GCC-8.patch
* Mon Mar 26 2018 msuchanek@suse.com
- Fix incorrect netmask on ppc64 (bsc#1085419)
  * grub2-Fix-incorrect-netmask-on-ppc64.patch
* Mon Mar 12 2018 mchang@suse.com
- Fix UEFI HTTPS Boot from ISO installation image (bsc#1076132)
  * 0001-add-support-for-UEFI-network-protocols.patch
* Tue Mar  6 2018 mchang@suse.com
- fix wrong command output when default subvolume is toplevel tree with
  id 5 (bsc#1078775)
  * grub2-btrfs-09-get-default-subvolume.patch
- insert mdraid modules to support software RAID (bsc#1078775)
  * grub2-xen-pv-firmware.cfg
* Thu Mar  1 2018 iforster@suse.com
- Rename grub2-btrfs-workaround-grub2-once.patch to
  grub2-grubenv-in-btrfs-header.patch
- Store GRUB environment variable health_checker_flag in Btrfs header
* Tue Feb 13 2018 mchang@suse.com
- Fix incorrect check preventing the script from running (bsc#1078481)
  * 80_suse_btrfs_snapshot
* Wed Feb  7 2018 mchang@suse.com
- Fix disappeared snapshot menu entry (bsc#1078481)
  * 80_suse_btrfs_snapshot
* Tue Feb  6 2018 mchang@suse.com
- Fix unquoted string error and add some more checks (bsc#1079330)
  * grub2-check-default.sh
* Mon Feb  5 2018 olaf@aepfle.de
- The %%prep section applies patches, the %%build section builds.
  Remove mixup of patching and building from %%prep for quilt setup
  Related to bsc#1065703
* Tue Jan 23 2018 mchang@suse.com
- Check if default entry need to be corrected for updated distributor version
  and/or use fallback entry if default kernel entry removed (bsc#1065349)
  * grub2-check-default.sh
  * grub2-mkconfig-default-entry-correction.patch
- Fix grub2-mkconfig warning when disk is LVM PV (bsc#1071239)
  * grub2-getroot-scan-disk-pv.patch
* Fri Dec  8 2017 mchang@suse.com
-  Filter out autofs and securityfs from /proc/self/mountinfo to speed
  up nfsroot test in large number of autofs mounts (bsc#1069094)
  * modified grub2-pass-corret-root-for-nfsroot.patch
* Tue Nov 28 2017 mchang@suse.com
- Fix http(s) boot security review (bsc#1058090)
  * 0002-AUDIT-0-http-boot-tracker-bug.patch
* Tue Nov 14 2017 mchang@suse.com
- 0001-add-support-for-UEFI-network-protocols.patch:
  * Workaround http data access in firmware
  * Fix DNS device path parsing for efinet device
  * Relaxed UEFI Protocol requirement
  * Support Intel OPA (Omni-Path Architecture) PXE Boot (bsc#1015589)
* Wed Nov  8 2017 olaf@aepfle.de
- grub2-xen-pv-firmware.cfg: remove linemode=1 from cmdline for
  SUSE installer. openQA expects ncurses interface. (bsc#1066919)
* Mon Nov  6 2017 jmatejek@suse.com
- use python3 for autogen.sh (fate#323526)
* Tue Oct 31 2017 msuchanek@suse.com
- Do not check that PReP partition does not contain an ELF during installation
  (bsc#1065738).
  * grub2-install-remove-useless-check-PReP-partition-is-empty.patch
* Tue Sep 26 2017 mchang@suse.com
- Build diskboot_tpm.img as separate image to diskboot.img to prevent failure
  in booting on some bogus firmware. To use the TPM image you have to use
  suse-enable-tpm option of grub2-install (bsc#1052401)
  * 0013-tpm-i386-pc-diskboot-img.patch
* Wed Sep 20 2017 mlatimer@suse.com
- Use /boot/<arch>/loader/linux to determine if install media
  is SUSE instead of /contents file (bsc#1054453)
* Tue Sep 19 2017 mlatimer@suse.com
- Use the pvops-enabled default kernel if the traditional xen
  pv kernel and initrd are not found (bsc#1054453)
* Fri Sep  8 2017 agraf@suse.com
- Fix reboot in UEFI environments (bsc#1047331)
  * Add grub2-efi-Move-grub_reboot-into-kernel.patch
  * Refresh grub2-efi-Free-malloc-regions-on-exit.patch
* Sun Sep  3 2017 mchang@suse.com
- Add preliminary patch for UEFI HTTPS and related network protocol support
  (fate#320130)
  * 0001-add-support-for-UEFI-network-protocols.patch
* Sun Sep  3 2017 mchang@suse.com
- grub2-s390x-04-grub2-install.patch : remove arybase dependency in
  grub2-zipl-setup by not referencing to $[ (bsc#1055280)
* Wed Aug 23 2017 rw@suse.com
- Fix minor oversights in and the exit value of the grub2-install
  helper on s390x.  (bsc#1055343, fate#323298)
  * grub2-s390x-09-improve-zipl-setup.patch
* Mon Jul 24 2017 bwiedemann@suse.com
- Make grub2.info build reproducible (boo#1047218)
* Tue Jul  4 2017 arvidjaar@gmail.com
- add grub2-fix-build-with-flex-2.6.4.patch - fix build with flex 2.6.4+
  that removed explicit (void) cast from fprintf call in yy_fatal_error.
* Thu Jun  1 2017 mchang@suse.com
- Support LVM physical volume created without metadatacopies (bsc#1027526)
  * grub2-diskfilter-support-pv-without-metadatacopies.patch
- Fix page fault exception when grub loads with Nvidia cards (bsc#1038533)
  * grub2-efi-uga-64bit-fb.patch
- Require 'kexec-tools' for System z. (bsc#944358)
  * modified grub2.spec
* Thu May 11 2017 mchang@suse.com
- grub2-xen-pv-firmware.cfg: insmod lvm module as it's not auto-loaded
  to support booting from lvm volume (bsc#1004324)
- Grub not working correctly with xen and btrfs snapshots (bsc#1026511)
  * Add grub2-btrfs-09-get-default-subvolume.patch
  * grub2-xen-pv-firmware.cfg : search path in default subvolume
* Thu Apr 27 2017 arvidjaar@gmail.com
- new upstream version 2.02
  * rediff
  - use-grub2-as-a-package-name.patch
  * drop upstream patches
  - grub2-fix-uninitialized-variable-in-btrfs-with-GCC7.patch
  - grub2-add-FALLTHROUGH-annotations.patch
- update translations
* Sun Mar 26 2017 arvidjaar@gmail.com
- update grub2-btrfs-workaround-grub2-once.patch to also store saved_entry
  in additional environment block (boo#1031025)
* Wed Mar 22 2017 arvidjaar@gmail.com
- fix building with GCC (bsc#1030247)
  * add grub2-fix-uninitialized-variable-in-btrfs-with-GCC7.patch
  * grub2-add-FALLTHROUGH-annotations.patch
* Mon Mar 20 2017 mchang@suse.com
- Fix out of memory error on lvm detection (bsc#1016536) (bsc#1027401)
  * grub2-lvm-allocate-metadata-buffer-from-raw-contents.patch
- Fix boot failure if /boot is separate btrfs partition (bsc#1023160)
  * grub2-btrfs-06-subvol-mount.patch
* Fri Mar 17 2017 mchang@suse.com
- 0004-tpm-Rework-linux-command.patch : Fix out of bound memory copy
  (bsc#1029187)
* Thu Mar 16 2017 arvidjaar@gmail.com
- new upstream version 2.02~rc2
  * rediff
  - use-grub2-as-a-package-name.patch
  - grub2-linguas.sh-no-rsync.patch
  * drop upstream patches
  - 0001-efi-strip-off-final-NULL-from-File-Path-in-grub_efi_.patch
* Mon Mar  6 2017 mchang@suse.com
- TPM Support (FATE#315831)
  * 0001-tpm-Core-TPM-support.patch
  * 0002-tpm-Measure-kernel-initrd.patch
  * 0003-tpm-Add-BIOS-boot-measurement.patch
  * 0004-tpm-Rework-linux-command.patch
  * 0005-tpm-Rework-linux16-command.patch
  * 0006-tpm-Measure-kernel-and-initrd-on-BIOS-systems.patch
  * 0007-tpm-Measure-the-kernel-commandline.patch
  * 0008-tpm-Measure-commands.patch
  * 0009-tpm-Measure-multiboot-images-and-modules.patch
  * 0010-tpm-Fix-boot-when-there-s-no-TPM.patch
  * 0011-tpm-Fix-build-error.patch
  * 0012-tpm-Build-tpm-as-module.patch
- grub2.spec : Add grub-tpm.efi for Secure Boot
* Fri Mar  3 2017 mchang@suse.com
- Fix invalid Xen EFI config files if xen_args include GRUB2 quoting
  (bsc#900418) (bsc#951748)
  * grub2-efi-xen-cfg-unquote.patch
- Fix linuxefi erroneously initialize linux's boot_params with non-zero
  values. (bsc#1025563)
  * grub2-linuxefi-fix-boot-params.patch
- Removed grub2-fix-multi-device-root-kernel-argument.patch as it has
  regression on how GRUB_DISABLE_LINUX_UUID=true interpreted (bsc#1015138)
* Wed Mar  1 2017 mchang@suse.com
- Fix for openQA UEFI USB Boot failure with upstream patch (bsc#1026344)
  * added 0001-efi-strip-off-final-NULL-from-File-Path-in-grub_efi_.patch
  * removed 0001-Revert-efi-properly-terminate-filepath-with-NULL-in-.patch
* Thu Feb 23 2017 mchang@suse.com
- Temporary fix for openQA UEFI USB Boot failure (bsc#1026344)
  * 0001-Revert-efi-properly-terminate-filepath-with-NULL-in-.patch
* Fri Feb 17 2017 mchang@suse.com
- grub2.spec: fix s390x file list.
* Thu Feb 16 2017 msuchanek@suse.com
- require efibootmgr in efi package (boo#1025520)
* Wed Feb 15 2017 mchang@suse.com
- Merge changes from SLE12
- add grub2-emu-4-all.patch
  * Build 'grub2-emu' wherever possible, to allow a better
    implementation of that feature.
- add grub2-s390x-06-loadparm.patch,
- add grub2-commands-introduce-read_file-subcommand.patch:
  * allow s390x to telecontrol grub2.  (bsc#891946, bsc#892852)
- add grub2-s390x-06-loadparm.patch:
  * ignore case and fix transliteration of parameter.  (bsc#891946)
- add grub2-s390x-07-add-image-param-for-zipl-setup.patch
  * Add --image switch to force zipl update to specific kernel
    (bsc#928131)
- add grub2-s390x-08-workaround-part-to-disk.patch
  * Ignore partition tables on s390x. (bsc#935127)
- add grub2-efi-chainload-harder.patch:
  * allow XEN to be chain-loaded despite firmware flaws.  (bnc#887793)
  * Do not use shim lock protocol for reading pe header, it won't be
  available when secure boot disabled (bsc#943380)
  * Make firmware flaw condition be more precisely detected and add
  debug message for the case
  * Check msdos header to find PE file header (bsc#954126)
- grub2-s390x-04-grub2-install.patch:
  * streamline boot to grub menu.  (bsc#898198)
  * Force '/usr' to read-only before calling kexec. (bsc#932951)
- grub2-once:
  * add '--enum' option to enumerate boot-entries in a way
    actually understood by 'grub2'.  (bsc#892852, bsc#892811)
  * Examine variables from grub environment in 'grub2-once'. (fate#319632)
* Fri Feb 10 2017 arvidjaar@gmail.com
- new upstream version 2.02~rc1
  * rediff
  - use-grub2-as-a-package-name.patch
  - grub2-s390x-04-grub2-install.patch
  - grub2-accept-empty-module.patch
  - grub2-btrfs-04-grub2-install.patch
  - grub2-btrfs-06-subvol-mount.patch
  * drop upstream patches
  - 0001-dns-fix-buffer-overflow-for-data-addresses-in-recv_h.patch
  - 0001-build-Use-AC_HEADER_MAJOR-to-find-device-macros.patch
  - 0002-configure-fix-check-for-sys-sysmacros.h-under-glibc-.patch
  - 0001-Fix-fwpath-in-efi-netboot.patch
  - 0001-arm64-Move-firmware-fdt-search-into-global-function.patch
  - 0002-arm-efi-Use-fdt-from-firmware-when-available.patch
  - grub2-arm64-mknetdir-add-suport-for-arm64-efi.patch
  - 0001-10_linux-Fix-grouping-of-tests-for-GRUB_DEVICE.patch
  - 0002-20_linux_xen-fix-test-for-GRUB_DEVICE.patch
  - 0001-xen-make-xen-loader-callable-multiple-times.patch
  - 0002-xen-avoid-memleaks-on-error.patch
  - 0003-xen-reduce-number-of-global-variables-in-xen-loader.patch
  - 0004-xen-add-elfnote.h-to-avoid-using-numbers-instead-of-.patch
  - 0005-xen-synchronize-xen-header.patch
  - 0006-xen-factor-out-p2m-list-allocation-into-separate-fun.patch
  - 0007-xen-factor-out-allocation-of-special-pages-into-sepa.patch
  - 0008-xen-factor-out-allocation-of-page-tables-into-separa.patch
  - 0009-xen-add-capability-to-load-initrd-outside-of-initial.patch
  - 0010-xen-modify-page-table-construction.patch
  - 0011-xen-add-capability-to-load-p2m-list-outside-of-kerne.patch
  * add
  - fix-grub2-use-stat-instead-of-udevadm-for-partition-lookup-with-new-glibc.patch
    fix compilation with new glibc
* Thu Feb  9 2017 mchang@suse.com
- Fix build error on glibc-2.25
  * 0001-build-Use-AC_HEADER_MAJOR-to-find-device-macros.patch
  * 0002-configure-fix-check-for-sys-sysmacros.h-under-glibc-.patch
- Fix fwpath in efi netboot (fate#321993) (bsc#1022294)
  * 0001-Fix-fwpath-in-efi-netboot.patch
* Fri Feb  3 2017 mchang@suse.com
- grub2-systemd-sleep.sh: Fix prematurely abort by commands error return code
  and skip the offending menu entry (bsc#1022880)
* Wed Feb  1 2017 agraf@suse.com
- Add support for BLT only EFI GOP adapters (FATE#322332)
  * grub2-efi-gop-add-blt.patch
* Wed Jan 25 2017 schwab@linux-m68k.org
- info-dir-entry.patch: Update info dir entry to follow renaming to grub2
* Mon Jan 16 2017 matwey.kornilov@gmail.com
- Add serial module to efi image.
  Serial terminal is still useful even with EFI Secure Boot
* Wed Jan 11 2017 mchang@suse.com
- Support %%posttrans with marcos provided by update-bootloader-rpm-macros
  package (bsc#997317)
* Wed Jan  4 2017 mchang@suse.com
- Remove outdated README.openSUSE (bsc#907693)
* Fri Dec 30 2016 sor.alexei@meowr.ru
- 20_memtest86+: avoid adding memtest86+ to the list with UEFI
  booting.
* Fri Oct 28 2016 mchang@suse.com
- Fix new line character in distributor (bsc#1007212)
  * modified grub2-default-distributor.patch
* Fri Oct 21 2016 mchang@suse.com
- From Juergen Gross <jgross@suse.com>: grub-xen: support booting huge
  pv-domains (bsc#1004398) (bsc#899465)
  * 0001-xen-make-xen-loader-callable-multiple-times.patch
  * 0002-xen-avoid-memleaks-on-error.patch
  * 0003-xen-reduce-number-of-global-variables-in-xen-loader.patch
  * 0004-xen-add-elfnote.h-to-avoid-using-numbers-instead-of-.patch
  * 0005-xen-synchronize-xen-header.patch
  * 0006-xen-factor-out-p2m-list-allocation-into-separate-fun.patch
  * 0007-xen-factor-out-allocation-of-special-pages-into-sepa.patch
  * 0008-xen-factor-out-allocation-of-page-tables-into-separa.patch
  * 0009-xen-add-capability-to-load-initrd-outside-of-initial.patch
  * 0010-xen-modify-page-table-construction.patch
  * 0011-xen-add-capability-to-load-p2m-list-outside-of-kerne.patch
* Tue Oct 11 2016 dmueller@suse.com
- add support for netboot on arm64-efi platforms (bsc#998097)
  * grub2-arm64-mknetdir-add-suport-for-arm64-efi.patch
* Fri Sep  2 2016 mchang@suse.com
- use $PRETTY_NAME instead of $NAME $VERSION for $GRUB_DISTRIBUTOR
  in openSUSE Tumbleweed (bsc#995549)
  * modified grub2-default-distributor.patch
- grub2.spec: add http module to grub.efi (fate#320129)
* Wed Aug 31 2016 matz@suse.com
- binutils 2.27 creates empty modules without a symtab.
  Add patch grub2-accept-empty-module.patch to not reject them.
* Sat Aug 20 2016 arvidjaar@gmail.com
- since version 1.7 cryptsetup defaults to SHA256 for LUKS - include
  gcry_sha256 in signed EFI image
* Fri Aug 12 2016 mchang@suse.com
- Workaround default entry in snapshot menu (bsc#956046)
  * grub2-btrfs-08-workaround-snapshot-menu-default-entry.patch
- grub2.spec: Add true command to grub.efi (bsc#993274)
* Wed Aug  3 2016 mchang@suse.com
- grub.default: Empty GRUB_CMDLINE_LINUX_DEFAULT, the value will be fully
  taken from YaST settings. (bsc#989803)
* Wed Aug  3 2016 mchang@suse.com
- Add patches from Roberto Sassu <rsassu@suse.de>
- Fix grub2-10_linux-avoid-multi-device-root-kernel-argument.patch,
  device path is not tested if GRUB_DISABLE_LINUX_UUID="true"
  - added grub2-fix-multi-device-root-kernel-argument.patch
  (bsc#960776)
- grub2-zipl-setup: avoid multi-device root= kernel argument
  * added grub2-zipl-setup-fix-btrfs-multipledev.patch
  (bsc#960776)
- Add SUSE_REMOVE_LINUX_ROOT_PARAM configuration option
  to /etc/default/grub, to remove root= and rootflags= from the
  kernel command line in /boot/grub2/grub.cfg and /boot/zipl/config
  - added grub2-suse-remove-linux-root-param.patch
  (bsc#962585)
* Tue Aug  2 2016 mchang@suse.com
- Support HTTP Boot IPv4 and IPv6 (fate#320129)
  * 0001-misc-fix-invalid-character-recongition-in-strto-l.patch
  * 0002-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
  * 0003-bootp-New-net_bootp6-command.patch
  * 0004-efinet-UEFI-IPv6-PXE-support.patch
  * 0005-grub.texi-Add-net_bootp6-doument.patch
  * 0006-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
  * 0007-efinet-Setting-network-from-UEFI-device-path.patch
  * 0008-efinet-Setting-DNS-server-from-UEFI-protocol.patch
- Fix heap corruption after dns lookup
  * 0001-dns-fix-buffer-overflow-for-data-addresses-in-recv_h.patch
* Mon Jun 27 2016 ro@suse.de
- fix filelist for s390x
* Tue Jun 21 2016 mchang@suse.com
- Fix grub2-editenv error on encrypted lvm installation (bsc#981621)
  * modified grub2-btrfs-workaround-grub2-once.patch
- Add missing closing bracket in 'grub2-snapper-plugin.sh'.
- Fix snapshot booting on s390x (bsc#955115)
  * modified grub2-snapper-plugin.sh
- Fallback to old subvol name scheme to support old snapshot config
  (bsc#953538)
  * added grub2-btrfs-07-subvol-fallback.patch
* Thu Jun  2 2016 arvidjaar@gmail.com
- update grub2-once with patch from Björn Voigt - skip comments in
  /etc/sysconfig/bootloader (boo#963610)
* Fri May 20 2016 jengelh@inai.de
- Make sure all systemd unit files are passed to %%service_ macros.
* Thu May 19 2016 agraf@suse.com
- Add patch to free memory on exit in efi environments (bsc#980739)
  * grub2-efi-Free-malloc-regions-on-exit.patch
* Mon May  2 2016 olaf@aepfle.de
- Remove xen-devel from BuildRequires
  required headers are included in grub-2.0.2
* Thu Apr 28 2016 agraf@suse.com
- Add support for "t" hotkey to switch to text mode (bsc#976836)
  * added grub2-SUSE-Add-the-t-hotkey.patch
- Add support for hidden menu entries (bsc#976836)
  * added grub2-Add-hidden-menu-entries.patch
* Tue Apr 19 2016 mchang@suse.com
- Correct show user defined comments in menu for snapshots (bsc#956698)
  * modified grub2-snapper-plugin.sh
* Mon Mar 21 2016 mchang@suse.com
- Fix GRUB_DISABLE_LINUX_UUID to be ignore and also fallback kernel device
  won't be used if fs uuid not detected (bsc#971867)
  * added 0001-10_linux-Fix-grouping-of-tests-for-GRUB_DEVICE.patch
  * added 0002-20_linux_xen-fix-test-for-GRUB_DEVICE.patch
* Tue Mar  1 2016 arvidjaar@gmail.com
- new upstream version 2.02~beta3
  * highlights of user visible changes not yet present in openSUSE package
  - arm-uboot now generates position independent self relocating image, so
    single binary should run on all supported systems
  - loader for Xen on aarch64. grub-mkconfig support was not in time for
    beta3 yet.
  - improved ZFS support (extensible_dataset, large_blocks, embedded_data,
    hole_birth features)
  - support for IPv6 Router Advertisements
  - support for persistent memory (we do not overwrite it and pass correct
    information to OS)
  - try to display more specific icons for os-prober generated menu entries
  - grub-install detects EFI bit size and selects correct platform (x86_64-efi
    or i386-efi) independent of OS bit size; needs kernel 4.0 or higher.
  - LVM RAID1 support
  - xnu loader fixes which should make OS X menu entry generated by os-prober
    work again
  - key modifiers (Ctrl-X etc) should work on EFI too
  - ... and lot of fixes over entire tree
  * rediff
  - rename-grub-info-file-to-grub2.patch
  - use-grub2-as-a-package-name.patch
  - grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
  - grub2-fix-menu-in-xen-host-server.patch
  - grub2-efi-HP-workaround.patch
  - grub2-secureboot-chainloader.patch
  - grub2-s390x-02-kexec-module-added-to-emu.patch
  - grub2-s390x-04-grub2-install.patch
  - grub2-s390x-05-grub2-mkconfig.patch
  - grub2-efi-xen-chainload.patch
  - grub2-mkconfig-aarch64.patch
  - grub2-btrfs-04-grub2-install.patch
  - grub2-ppc64-cas-reboot-support.patch
  - 0002-Add-Virtual-LAN-support.patch
  * fix grub2-secureboot-add-linuxefi.patch - use grub_memset and
    grub_memcpy instead of memset and memcpy (caused errors due to
    compiler warning)
  * drop upstream patches
  - 0001-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
  - 0001-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch
  - 0001-efidisk-move-device-path-helpers-in-core-for-efinet.patch
  - 0002-efinet-skip-virtual-IPv4-and-IPv6-devices-when-enume.patch
  - 0003-efinet-open-Simple-Network-Protocol-exclusively.patch
  - 0001-efinet-Check-for-immediate-completition.patch
  - 0001-efinet-enable-hardware-filters-when-opening-interfac.patch
  - grub2-xen-legacy-config-device-name.patch
  - grub2-getroot-support-NVMe-device-names.patch
  - grub2-netboot-hang.patch
  - grub2-btrfs-fix-incorrect-address-reference.patch
  - aarch64-reloc.patch
  - grub2-glibc-2.20.patch (related code dropped upstream)
  - grub2-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
  - grub2-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
  - grub2-getroot-fix-get-btrfs-fs-prefix-big-endian.patch
  - grub2-ppc64-qemu.patch
  - grub2-xfs-Add-helper-for-inode-size.patch
  - grub2-xfs-Fix-termination-loop-for-directory-iteration.patch
  - grub2-xfs-Convert-inode-numbers-to-cpu-endianity-immediate.patch
  - grub2-xfs-V5-filesystem-format-support.patch
  - 0001-Add-bootargs-parser-for-open-firmware.patch
  - grub2-arm64-set-correct-length.patch
  - grub2-arm64-setjmp-Add-missing-license-macro.patch
  - grub2-arm64-efinet-handle-get_status-on-buggy-firmware-properly.patch
  - 0001-unix-password-Fix-file-descriptor-leak.patch
  - 0002-linux-getroot-fix-descriptor-leak.patch
  - 0003-util-grub-mount-fix-descriptor-leak.patch
  - 0004-linux-ofpath-fix-descriptor-leak.patch
  - 0005-grub-fstest-fix-descriptor-leak.patch
  - ppc64le.patch
  - libgcc-prereq.patch
  - libgcc.patch
  - 0001-Fix-security-issue-when-reading-username-and-passwor.patch
  - 0001-menu-fix-line-count-calculation-for-long-lines.patch
  - grub2-arm64-Reduce-timer-event-frequency-by-10.patch
  - 0001-unix-do-not-close-stdin-in-grub_passwd_get.patch
  - 0001-grub-core-kern-i386-tsc.c-calibrate_tsc-Ensure-that.patch
  - 0002-i386-tsc-Fix-unused-function-warning-on-xen.patch
  - 0003-acpi-do-not-skip-BIOS-scan-if-EBDA-length-is-zero.patch
  - 0004-tsc-Use-alternative-delay-sources-whenever-appropria.patch
  - 0005-i386-fix-TSC-calibration-using-PIT.patch
  - biendian.patch
  - ppc64_opt.patch
  * drop workarounds for gdb_grub and grub.chrp, they are now installed under fixed name
  * do not patch docs/Makefile.in, it is regenerated anyway
* Tue Mar  1 2016 agraf@suse.com
- Make mkconfig search for zImage on arm
  * grub2-mkconfig-arm.patch
* Sun Feb 28 2016 agraf@suse.com
- Add support to directly pass an EFI FDT table to a kernel on 32bit arm
  * 0001-arm64-Move-firmware-fdt-search-into-global-function.patch
  * 0002-arm-efi-Use-fdt-from-firmware-when-available.patch
* Fri Jan 29 2016 mchang@suse.com
- Add config option to set efi xen loader command line option (bsc#957383)
  * added grub2-efi-xen-cmdline.patch
* Thu Jan 28 2016 dvaleev@suse.com
- Drop ppc64le patches. Build stage1 as BE for Power
  Droped patches:
  - grub2-ppc64le-01-Add-Little-Endian-support-for-Power64-to-the-build.patch
  - grub2-ppc64le-02-Build-grub-as-O1-until-we-add-savegpr-and-restgpr-ro.patch
  - grub2-ppc64le-03-disable-creation-of-vsx-and-altivec-instructions.patch
  - grub2-ppc64le-04-powerpc64-LE-s-linker-knows-how-to-handle-the-undefi.patch
  - grub2-ppc64le-05-grub-install-can-now-recognize-and-install-a-LE-grub.patch
  - grub2-ppc64le-06-set-the-ABI-version-to-0x02-in-the-e_flag-of-the-PPC.patch
  - grub2-ppc64le-07-Add-IEEE1275_ADDR-helper.patch
  - grub2-ppc64le-08-Fix-some-more-warnings-when-casting.patch
  - grub2-ppc64le-09-Add-powerpc64-types.patch
  - grub2-ppc64le-10-powerpc64-is-not-necessarily-BigEndian-anymore.patch
  - grub2-ppc64le-11-Fix-warnings-when-building-powerpc-linux-loader-64bi.patch
  - grub2-ppc64le-12-GRUB_ELF_R_PPC_-processing-is-applicable-only-for-32.patch
  - grub2-ppc64le-13-Fix-powerpc-setjmp-longjmp-64bit-issues.patch
  - grub2-ppc64le-14-Add-powerpc64-ieee1275-trampoline.patch
  - grub2-ppc64le-15-Add-64bit-support-to-powerpc-startup-code.patch
  - grub2-ppc64le-16-Add-grub_dl_find_section_addr.patch
  - grub2-ppc64le-17-Add-ppc64-relocations.patch
  - grub2-ppc64le-18-ppc64-doesn-t-need-libgcc-routines.patch
  - grub2-ppc64le-19-Use-FUNC_START-FUNC_END-for-powerpc-function-definit.patch
  - grub2-ppc64le-20-.TOC.-symbol-is-special-in-ppc64le-.-It-maps-to-the-.patch
  - grub2-ppc64le-21-the-.toc-section-in-powerpc64le-modules-are-sometime.patch
  - grub2-ppc64le-22-all-parameter-to-firmware-calls-should-to-be-BigEndi.patch
  - grub2-ppc64le-fix-64bit-trampoline-in-dyn-linker.patch
  - grub2-ppc64le-timeout.patch
  - grub2-ppc64-build-ppc64-32bit.patch
- Added patches:
  - biendian.patch
  - grub2-ppc64-cas-reboot-support.patch
  - libgcc-prereq.patch
  - libgcc.patch
  - ppc64_opt.patch
  - ppc64le.patch
* Wed Jan 20 2016 mchang@suse.com
- Backport upstream patches for HyperV gen2 TSC timer calbration without
  RTC (bsc#904647)
  * added 0001-grub-core-kern-i386-tsc.c-calibrate_tsc-Ensure-that.patch
  * added 0002-i386-tsc-Fix-unused-function-warning-on-xen.patch
  * added 0003-acpi-do-not-skip-BIOS-scan-if-EBDA-length-is-zero.patch
  * added 0004-tsc-Use-alternative-delay-sources-whenever-appropria.patch
  * added 0005-i386-fix-TSC-calibration-using-PIT.patch
* Mon Dec 28 2015 arvidjaar@gmail.com
- Add 0001-menu-fix-line-count-calculation-for-long-lines.patch (bsc#943585)
* Thu Dec 17 2015 olaf@aepfle.de
- grub2-xen-pv-firmware.cfg: fix hd boot (boo#926795)
* Wed Dec 16 2015 arvidjaar@gmail.com
- Add 0001-Fix-security-issue-when-reading-username-and-passwor.patch
  Fix for CVE-2015-8370 [boo#956631]
* Wed Dec  9 2015 arvidjaar@gmail.com
- Update grub2-efi-xen-chainload.patch - fix copying of Linux kernel
  and initrd to ESP (boo#958193)
* Mon Dec  7 2015 olaf@aepfle.de
- Rename grub2-xen.cfg to grub2-xen-pv-firmware.cfg (boo#926795)
* Fri Dec  4 2015 olaf@aepfle.de
- grub2-xen.cfg: to handle grub1 menu.lst in PV guest (boo#926795)
* Thu Nov 26 2015 mchang@suse.com
- Expand list of grub.cfg search path in PV Xen guest for systems
  installed to btrfs snapshot. (bsc#946148) (bsc#952539)
  * modified grub2-xen.cfg
- drop grub2-fix-Grub2-with-SUSE-Xen-package-install.patch (bsc#774666)
* Wed Nov 18 2015 arvidjaar@gmail.com
- Add 0001-unix-do-not-close-stdin-in-grub_passwd_get.patch
  Fix reading password by grub2-mkpasswd-pbdk2 without controlling
  tty, e.g. when called from Xfce menu (boo#954519)
* Sun Nov  1 2015 arvidjaar@gmail.com
- Modify grub2-linguas.sh-no-rsync.patch to re-enable en@quot catalog
  (boo#953022).  Other autogenerated catalogs still fail to build due
  to missing C.UTF-8 locale.
* Fri Oct 30 2015 mchang@suse.com
- Allow to execute menuentry unrestricted as default (fate#318574)
  * added grub2-menu-unrestricted.patch
* Thu Oct 29 2015 mchang@suse.com
- Add missing quoting for linuxefi (bsc#951962)
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
  * refreshed grub2-secureboot-provide-linuxefi-config.patch
* Sun Oct 18 2015 eich@suse.com
- Include custom.cfg into the files scanned by grub2-once.
  Allows to chose manually added entries as well (FATE#319632).
* Wed Oct  7 2015 mchang@suse.com
- Upstream patches for fixing file descriptor leakage (bsc#943784)
  * added 0001-unix-password-Fix-file-descriptor-leak.patch
  * added 0002-linux-getroot-fix-descriptor-leak.patch
  * added 0003-util-grub-mount-fix-descriptor-leak.patch
  * added 0004-linux-ofpath-fix-descriptor-leak.patch
  * added 0005-grub-fstest-fix-descriptor-leak.patch
* Tue Oct  6 2015 mchang@suse.com
- Do not force ro option in linuxefi patch (bsc#948555)
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
  * refrehed grub2-secureboot-provide-linuxefi-config.patch
* Wed Sep 23 2015 dmueller@suse.com
- add 0001-efinet-Check-for-immediate-completition.patch,
  0001-efinet-enable-hardware-filters-when-opening-interfac.patch,
  grub2-arm64-efinet-handle-get_status-on-buggy-firmware-properly.patch
  (bsc#947203)
* Mon Sep 14 2015 mchang@suse.com
- Set default GRUB_DISTRIBUTOR from /etc/os-release if it is empty
  or not set by user (bsc#942519)
  * added grub2-default-distributor.patch
  * modified grub.default
* Tue Aug 18 2015 mchang@suse.com
- add systemd-sleep-plugin subpackage (bsc#941758)
- evaluate the menu entry's title string by printf
  * modified grub2-once
  * added grub2-systemd-sleep.sh
* Fri Jul 31 2015 mchang@suse.com
- fix for 'rollback' hint (bsc#901487)
  * modified grub2-btrfs-05-grub2-mkconfig.patch:
* Fri Jul 17 2015 mchang@suse.com
- Replace 12.1 with 12 SP1 for the list of snapshots (bsc#934252)
  * modified grub2-snapper-plugin.sh
* Thu Jun 18 2015 mchang@suse.com
- Fix btrfs subvol detection on BigEndian systems (bsc#933541)
  * modified grub2-btrfs-06-subvol-mount.patch
- Fix grub2-mkrelpath outputs wrong path on BigEndian system
  * added grub2-getroot-fix-get-btrfs-fs-prefix-big-endian.patch
* Fri Jun 12 2015 mchang@suse.com
- If we have a post entry and the description field is empty, we should use the
  "Pre" number and add that description to the post entry. (fate#317972)
- Show user defined comments in grub2 menu for snapshots (fate#318101)
  * modified grub2-snapper-plugin.sh
* Sun Jun  7 2015 arvidjaar@gmail.com
- add 0001-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
  make sure firmware path starts with '/' (boo#902982)
* Fri Jun  5 2015 mchang@suse.com
- Fix btrfs patch on BigEndian systems (bsc#933541)
  * modified grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  * modified grub2-btrfs-06-subvol-mount.patch
* Wed Jun  3 2015 agraf@suse.com
- Fix license for setjmp module
  * added grub2-arm64-setjmp-Add-missing-license-macro.patch
* Thu May 21 2015 mchang@suse.com
- Fix install into snapper controlled btrfs subvolume and can't
  load grub modules from separate subvolume (fate#318392)
  * added grub2-btrfs-06-subvol-mount.patch
  * grub2-snapper-plugin.sh: use absolute subvol name
* Tue May 19 2015 arvidjaar@gmail.com
- also Recommends mtools for grub2-mkrescue (used to create EFI
  boot image) in addition to libburnia-tools.
* Mon May 11 2015 mchang@suse.com
- Support booting opensuse installer as PV DomU (boo#926795)
  * added grub2-xen.cfg for tracking default pvgrub2 xen configs rather than
    generating it from spec file
  * grub2-xen.cfg: from Olaf Hering <ohering@suse.com>
* Sun May 10 2015 arvidjaar@gmail.com
- replace grub2-efinet-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
  with upstream version:
  * 0001-efidisk-move-device-path-helpers-in-core-for-efinet.patch
  * 0002-efinet-skip-virtual-IPv4-and-IPv6-devices-when-enume.patch
  * 0003-efinet-open-Simple-Network-Protocol-exclusively.patch
  Fixes EFI network boot in some QEMU configurations.
* Wed Apr 29 2015 dmueller@suse.com
- fix grub2-mkconfig-aarch64.patch: fix arch detection broken
  by malformed patch rediffing
* Wed Apr 15 2015 mchang@suse.com
- Cleanup patch not applied
  * remove grub2-enable-theme-for-terminal-window.patch
  * grub2.rpmlintrc: remove addFilter("patch-not-applied")
* Thu Apr  2 2015 mchang@suse.com
- Merge changes from SLE12
- Do not pass root= when root is on nfs (bnc#894374)
  * modified grub2-pass-corret-root-for-nfsroot.patch
  * modified grub2-secureboot-provide-linuxefi-config.patch
  * modified grub2-secureboot-use-linuxefi-on-uefi.patch
- Fix xen pvops kernel not appear on menu (bnc#895286)
  * modified grub2-fix-menu-in-xen-host-server.patch
- Workaround grub2-once (bnc#892358)
  * added grub2-btrfs-workaround-grub2-once.patch
  * added grub2-once.service
  * modified grub2-once
- Fix busy-loop and hang while network booting (bnc#870613)
  * added grub2-netboot-hang.patch
- Add warning in grubenv file about editing it directly (bnc#887008)
  * added grub2-editenv-add-warning-message.patch
- Fix broken graphics with efifb on QEMU/KVM and nomodeset (bnc#884558)
  * added grub2-efi-disable-video-cirrus-and-bochus.patch
- Disable video support on Power (bnc#877142)
  * added grub2-ppc64le-disable-video.patch
- Track occupied memory so it can be released on exit (bnc#885026)
  * added grub2-ppc64le-memory-map.patch
- Fix grub.xen config searching path on boot partition (bnc#884828)
- Add linux16 and initrd16 to grub.xen (bnc#884830)
  * added grub2-xen-linux16.patch
- VLAN tag support (fate#315753)
  * added 0001-Add-bootargs-parser-for-open-firmware.patch
  * added 0002-Add-Virtual-LAN-support.patch
- Use chainloader to boot xen.efi under UEFI (bnc#871857)
  * added grub2-efi-xen-chainload.patch
- Use device part of chainloader target, if present (bnc#871857)
  * added grub2-efi-chainloader-root.patch
- Create only hypervisor pointed by /boot/xen.gz symlink (bnc#877040)
  * modified grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
- Fix xen and native entries differ in grub.cfg (bnc#872014)
  * modified grub2-linux.patch
- Fix install error on ddf md device (bnc#872360)
  * added grub2-getroot-treat-mdadm-ddf-as-simple-device.patch
- Fix booting from NVMe device (bnc#873132)
  * added grub2-getroot-support-NVMe-device-names.patch
- Document peculiarities of s390 terminals
  * added README.ibm3215
- Grub2 for System z (fate#314213)
  * added grub2-s390x-02-kexec-module-added-to-emu.patch
  * added grub2-s390x-03-output-7-bit-ascii.patch
  * added grub2-s390x-04-grub2-install.patch
  * added grub2-s390x-05-grub2-mkconfig.patch
* Mon Mar 16 2015 schwab@suse.de
- grub2-arm64-set-correct-length.patch: arm64: set correct length of
  device path end entry
* Wed Mar  4 2015 mchang@suse.com
- grub2-efi-HP-workaround.patch:
  * try to read config from all-uppercase prefix as last resort.
    (bnc#872503) (boo#902982)
* Mon Feb 16 2015 arvidjaar@gmail.com
- add luks, gcry_rijndael, gcry_sha1 to signed EFI image to support
  LUKS partition in default setup (boo#917427)
* Thu Feb  5 2015 mchang@suse.com
- enable i386-xen (boo#891043)
* Wed Feb  4 2015 mchang@suse.com
- Downgrade os-prober dependency to Recommends (boo#898610)
* Thu Dec 25 2014 mchang@suse.com
- grub2-snapper-plugin.sh: cleanup grub-snapshot.cfg not referring
  to any snapshot (boo#909359)
* Thu Dec 25 2014 mpluskal@suse.com
- Require efibootmgr also on i586
* Tue Dec 16 2014 schwab@suse.de
- Require efibootmgr also on aarch64
* Thu Dec 11 2014 schwab@suse.de
- grub2-snapper-plugin.sh: fix use of printf without format string; fix
  quoting
* Wed Dec 10 2014 schwab@suse.de
- grub2-arm64-Reduce-timer-event-frequency-by-10.patch: fix periodic timer
  on arm64
* Thu Dec  4 2014 agraf@suse.com
- enable 32bit arm targets for uboot and efi
* Sat Nov 29 2014 Led <ledest@gmail.com>
- Replace 'echo -e' command in grub2-snapper-plugin.sh script to
  'printf' command. '-e' option of 'echo' command may be
  unsupported in some POSIX-complete shells.
* Fri Nov 14 2014 Led <ledest@gmail.com>
- fix bashism in post script
* Thu Oct 30 2014 jdelvare@suse.de
- grub2.spec: Fix conditional construct which wasn't supported by
  older versions of rpmbuild (caused error message
  "parseExpressionBoolean returns -1".)
* Thu Oct 30 2014 mchang@suse.com
- fix errors when boot is btrfs with Windows partition scheme. The
  first partition is created on cylinder boundary that can't offer
  enough room for core.img and also the installation has to be in
  logical paritition which made MBR the only location to install.
  (bnc#841247)
  * add grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch
* Tue Sep 30 2014 mchang@suse.com
- packaging 20_memtest86+ and 20_ppc_terminfo in corresponing grubarch
  package
* Mon Sep 29 2014 fcastelli@suse.com
- Add '80_suse_btrfs_snapshot' required to show btrfs snapshots inside
  of the boot menu.
* Sun Sep 28 2014 arvidjaar@gmail.com
- fix btrfs on big endian systems (ppc/ppc64)
  * add grub2-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
* Sun Sep 21 2014 arvidjaar@gmail.com
- update translations
- fix possible access to uninitialized pointer in linux loader
  * add grub2-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
  * drop superceded grub2-ppc64le-23-grub-segfaults-if-initrd-is-specified-before-specify.patch
* Thu Sep 18 2014 mchang@suse.com
- fix grub.xen not able to handle legacy menu.lst hdX names (bnc#863821)
  * add grub2-xen-legacy-config-device-name.patch from arvidjaar
- fix the performance of grub2 uefi pxe is bad (bnc#871555)
  * add grub2-efinet-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
* Tue Sep 16 2014 schwab@suse.de
- grub2-mkconfig-aarch64.patch: Look for Image-* instead of vmlinuz-* on
  aarch64
* Mon Sep 15 2014 arvidjaar@gmail.com
- add grub2-glibc-2.20.patch - fix build with glibc 2.20+
  (use _DEFAULT_SOURCE to avoid warning)
* Fri Sep 12 2014 mchang@suse.com
- fix xen pvops kernel not appear on menu (bnc#895286)
  * refresh grub2-fix-menu-in-xen-host-server.patch
* Wed Sep 10 2014 mchang@suse.com
- fix extraneous comma in printf shell command (bnc#895884)
  * refresh grub2-btrfs-04-grub2-install.patch
* Wed Aug 27 2014 schwab@suse.de
- aarch64-reloc.patch: replace with upstream solution
* Mon Aug 25 2014 mchang@suse.com
- remove unused patch, which's supersceded by new snapper rollback
  support patches
  * 0001-script-provide-overridable-root-by-subvol.patch
  * 0002-script-create-menus-for-btrfs-snapshot.patch
* Fri Aug 22 2014 mchang@suse.com
- fix openqa boot error on separate boot partition
  * refresh grub2-btrfs-05-grub2-mkconfig.patch
* Thu Aug 21 2014 mchang@suse.com
- update snapper plugin for rollback support
  * refresh grub2-snapper-plugin.sh
* Fri Aug 15 2014 mchang@suse.com
- snapper rollback support patches.
- rename patch
  * 0002-btrfs-add-ability-to-boot-from-subvolumes.patch to
    grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
  * 0004-btrfs-export-subvolume-envvars.patch to
    grub2-btrfs-02-export-subvolume-envvars.patch
- added patches
  * grub2-btrfs-03-follow_default.patch
  * grub2-btrfs-04-grub2-install.patch
  * grub2-btrfs-05-grub2-mkconfig.patch
- remove patch
  * 0003-cmdline-add-envvar-loader_cmdline_append.patch
* Thu Aug 14 2014 mchang@suse.com
- grub2-btrfs-fix-incorrect-address-reference.patch
  * Fix incorrect address reference in GRUB_BTRFS_EXTENT_REGULAR
    range check (bnc#869748)
* Wed Aug 13 2014 mchang@suse.com
- grub2-vbe-blacklist-preferred-1440x900x32.patch
  * Blacklist preferred resolution 1440x900x32 which is broken on
    many Thinkpads (bnc#888727)
* Tue Aug 12 2014 schwab@suse.de
- Enable building on aarch64
- aarch64-reloc.patch: support R_AARCH64_PREL32 relocation
- Build host tools with RPM_OPT_FLAGS
* Mon Aug 11 2014 dvaleev@suse.com
- Fix the 64-bit trampoline code in dynamic linker (bnc#890999)
  grub2-ppc64le-fix-64bit-trampoline-in-dyn-linker.patch
* Tue Jul 29 2014 tiwai@suse.de
- Prefer a higher resolution in efi_gop driver if the mode taking
  over is too small like 640x480 (bnc#887972):
  grub2-efi_gop-avoid-low-resolution.patch
* Wed Jul  9 2014 dvlaeev@suse.com
- Fix ppc64le build by fixing
  grub2-xfs-V5-filesystem-format-support.patch
* Wed Jun 25 2014 jack@suse.cz
- xfs V5 superblock support (bnc#880166 bnc#883942)
- added patches:
  * grub2-xfs-Add-helper-for-inode-size.patch
  * grub2-xfs-Fix-termination-loop-for-directory-iteration.patch
  * grub2-xfs-Convert-inode-numbers-to-cpu-endianity-immediate.patch
  * grub2-xfs-V5-filesystem-format-support.patch
* Fri Jun 20 2014 jeffm@suse.com
- grub2: use stat instead of udevadm for partition lookup (bnc#883635)
  * Added grub2-use-stat-instead-of-udevadm-for-partition-lookup.patch
* Tue Apr 15 2014 tchvatal@suse.com
- Fix sorting of RC kernels to be older than first regular of the
  series. Fixes bnc#827531.
- added patches:
  * grub2-use-rpmsort-for-version-sorting.patch
* Thu Apr 10 2014 dvaleev@suse.com
- Build GRUB2 for ppc64le as LittleEndian and 64bit
- Fix timeout issue on ppc64le (bnc#869166)
- Add powerpc-utils requires to grub2-powerpc-ieee1275
- added patches:
  * grub2-ppc64-build-ppc64-32bit.patch
  * grub2-ppc64-qemu.patch
  * grub2-ppc64le-01-Add-Little-Endian-support-for-Power64-to-the-build.patch
  * grub2-ppc64le-02-Build-grub-as-O1-until-we-add-savegpr-and-restgpr-ro.patch
  * grub2-ppc64le-03-disable-creation-of-vsx-and-altivec-instructions.patch
  * grub2-ppc64le-04-powerpc64-LE-s-linker-knows-how-to-handle-the-undefi.patch
  * grub2-ppc64le-05-grub-install-can-now-recognize-and-install-a-LE-grub.patch
  * grub2-ppc64le-06-set-the-ABI-version-to-0x02-in-the-e_flag-of-the-PPC.patch
  * grub2-ppc64le-07-Add-IEEE1275_ADDR-helper.patch
  * grub2-ppc64le-08-Fix-some-more-warnings-when-casting.patch
  * grub2-ppc64le-09-Add-powerpc64-types.patch
  * grub2-ppc64le-10-powerpc64-is-not-necessarily-BigEndian-anymore.patch
  * grub2-ppc64le-11-Fix-warnings-when-building-powerpc-linux-loader-64bi.patch
  * grub2-ppc64le-12-GRUB_ELF_R_PPC_-processing-is-applicable-only-for-32.patch
  * grub2-ppc64le-13-Fix-powerpc-setjmp-longjmp-64bit-issues.patch
  * grub2-ppc64le-14-Add-powerpc64-ieee1275-trampoline.patch
  * grub2-ppc64le-15-Add-64bit-support-to-powerpc-startup-code.patch
  * grub2-ppc64le-16-Add-grub_dl_find_section_addr.patch
  * grub2-ppc64le-17-Add-ppc64-relocations.patch
  * grub2-ppc64le-18-ppc64-doesn-t-need-libgcc-routines.patch
  * grub2-ppc64le-19-Use-FUNC_START-FUNC_END-for-powerpc-function-definit.patch
  * grub2-ppc64le-20-.TOC.-symbol-is-special-in-ppc64le-.-It-maps-to-the-.patch
  * grub2-ppc64le-21-the-.toc-section-in-powerpc64le-modules-are-sometime.patch
  * grub2-ppc64le-22-all-parameter-to-firmware-calls-should-to-be-BigEndi.patch
  * grub2-ppc64le-23-grub-segfaults-if-initrd-is-specified-before-specify.patch
  * grub2-ppc64le-timeout.patch
- removed patches:
  * grub2-powerpc-libgcc.patch
  * grub2-ppc64le-core-bigendian.patch
  * grub2-ppc64le-platform.patch
* Thu Apr 10 2014 mchang@suse.com
- add grub2-x86_64-xen subpackage (bnc#863821)
* Sat Apr  5 2014 arvidjaar@gmail.com
- rename grub2.chrp back into grub.chrp, otherwise it is not found by
  grub tools
- replace grub2-use-DejaVuSansMono-for-starfield-theme.patch with
  grub2-use-Unifont-for-starfield-theme-terminal.patch - use Unifont
  font for terminal window
* Thu Feb 27 2014 mchang@suse.com
- grub2-snapper-plugin: fix important snapshots are not marked as such
  in grub2 menu, also display the snapshot entries in the format
  "important distribution version (kernel_version, timestamp, pre/post)"
  (bnc#864842)
* Mon Feb 24 2014 mchang@suse.com
- refresh grub2-fix-menu-in-xen-host-server.patch (bnc#859361)
  * prevent 10_linux from booting xen kernel without pv_opt support
    on systems other than xen PV domU guest
  * prevent 20_linux_xen.in from setting up nested virt running from
    Xen domU
- refresh grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
  * adjust accordingly
* Thu Feb 20 2014 jw@suse.com
- updating grub2-once
  - added --list switch.
  - improved --help and error handling.
* Tue Feb 11 2014 mchang@suse.com
- add Supplements: packageand(snapper:grub2) in grub2-snapper-plugin
  to install it while both snapper and grub2 are installed
* Wed Feb  5 2014 mchang@suse.com
- add grub2-snapper-plugin.sh (fate#316232)
  * grub2's snapper plugin for advanced btrfs snapshot menu management
  * package as grub2-snapper-plugin.noarch
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * when booting btrfs snapshots disabled, deleting snapshot master config
    if it's not customized
* Fri Jan 31 2014 dvaleev@suse.com
- Enable grub2 for PowerPC LE (ppc64le)
- Add ppc64le to exclusive arches
- Don't require gcc-32bit (PowerLE don't have 32bit toolchain)
- added patches:
  * grub2-powerpc-libgcc.patch
    Provide 32bit libgcc functions for PowerLE
  * grub2-ppc64le-core-bigendian.patch
    Build grub kernel and images as BE on ppc64le (BL is BE there)
  * grub2-ppc64le-platform.patch
    Enable ppc64le platform
* Fri Jan 24 2014 jjolly@suse.com
- Add changes to allow build for s390x arch: added
  grub2-s390x-01-Changes-made-and-files-added-in-order-to-allow-s390x.patch
* Wed Jan 22 2014 mchang@suse.com
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * Fix bootable snapshots not found while root is on Btrfs subvolume
  (bnc#859587)
  * Create missing slave config in /.snapshots/<num>/
  * Prefix with SUSE_ for related options
* Fri Jan 17 2014 mchang@suse.com
- refresh 0001-script-provide-overridable-root-by-subvol.patch
  * Introduce $boot_prefix for setting prefix on seeking other /boot
  directory.
- refresh 0002-script-create-menus-for-btrfs-snapshot.patch
  * Support existing snapshots by creating their missing slave configs.
  * Temporarily default to disable this feature until receiving more
  tests from QA.
  * Introduce GRUB_ENABLE_CUSTOM_SNAPSHOT_SUBMENU to allow custom
  submenu for listing snapshots rather than the default one.
* Wed Jan 15 2014 arvidjaar@gmail.com
- package autoiso.cfg and osdetect.cfg as documentation
- add 0001-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch -
  fix configure test for DejaVu font
- add dejavu-fonts to BR (needed to build starfield theme)
- package starfield theme as grub2-branding-upstream
- add grub2-use-DejaVuSansMono-for-starfield-theme.patch - use fixed width
  font for starfield theme
- clarify that grub2 subpackage contains only user space tools
* Wed Jan 15 2014 mchang@suse.com
- add new patches for booting btrfs snapshot (fate#316522) (fate#316232)
  * 0001-script-provide-overridable-root-by-subvol.patch
  * 0002-script-create-menus-for-btrfs-snapshot.patch
* Fri Dec 27 2013 arvidjaar@gmail.com
- update to grub-2.02 beta2
  * drop upstream patches
  - grub2-fix-unquoted-string-in-class.patch (different)
  - grub2-cdpath.patch (modified)
  - grub2-fix-parsing-of-short-LVM-PV-names.patch
  - grub2-fix-descriptor-leak-in-grub_util_is_imsm.patch
  - grub2-install-opt-skip-fs-probe.patch (file it patched no more exists,
    functionality included upstream)
  - grub2-fix-x86_64-efi-startup-stack-alignment.patch
  - grub2-fix-x86_64-efi-callwrap-stack-alignment.patch
  - 0001-Fix-build-with-FreeType-2.5.1.patch
  * rediff
  - grub2-linux.patch
  - use-grub2-as-a-package-name.patch (do not patch generated configure)
  - grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch
  - grub2-fix-locale-en.mo.gz-not-found-error-message.patch (upstream added
    explicit exclusion for en_* language only; I do not see reason to stop
    with error in this case for any language).
  - not-display-menu-when-boot-once.patch
  - grub2-secureboot-provide-linuxefi-config.patch
  - grub2-pass-corret-root-for-nfsroot.patch
  - 0002-btrfs-add-ability-to-boot-from-subvolumes.patch
  - grub2-fix-menu-in-xen-host-server.patch
  - grub2-fix-Grub2-with-SUSE-Xen-package-install.patch
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - rename-grub-info-file-to-grub2.patch
  * drop Makefile.util.am and Makefile.core.am, they are now generated
    during build
  * call ./autogen.sh again now when it does not need autogen anymore; drop
    autoreconf call, it is called by autogen.sh
  * drop 0001-btrfs-rename-skip_default-to-follow_default.patch - is not
    needed anymore due to upstream changes
  * package /usr/bin/grub2-file, /usr/bin/grub2-syslinux2cfg and
    /usr/sbin/grub2-macbless
  * use grub-install --no-bootsector instead of --grub-setup=/bin/true
    in postinstall script
* Tue Dec 17 2013 mchang@suse.com
- add new patches for booting btrfs snapshot (fate#316522) (fate#316232)
  * 0001-btrfs-rename-skip_default-to-follow_default.patch
  * 0002-btrfs-add-ability-to-boot-from-subvolumes.patch
  * 0003-cmdline-add-envvar-loader_cmdline_append.patch
  * 0004-btrfs-export-subvolume-envvars.patch
* Tue Dec 10 2013 arvidjaar@gmail.com
- add patch 0001-Fix-build-with-FreeType-2.5.1.patch - fix build with
  freetype2 >= 2.5.1 (backport from fd0df6d098b1e6a4f60275c48a3ec88d15ba1fbb)
* Sun Dec  1 2013 arvidjaar@gmail.com
- reset executable bits on *module, *.exec and *.image files. They are not
  executable.
* Fri Nov 22 2013 glin@suse.com
- add grub2-fix-x86_64-efi-startup-stack-alignment.patch and
  grub2-fix-x86_64-efi-callwrap-stack-alignment.patch: fix the
  stack alignment of x86_64 efi. (bnc#841426)
* Wed Sep 11 2013 mchang@suse.com
- use new update-bootloader option --reinit to install and update
  bootloader config
- refresh grub2-secureboot-no-insmod-on-sb.patch to fobid module
  loading completely.
* Mon Sep  9 2013 lnussel@suse.de
- replace openSUSE UEFI certificate with new 2048 bit certificate.
* Sat Jul 27 2013 arvidjaar@gmail.com
- add grub2-fix-parsing-of-short-LVM-PV-names.patch - fix PV detection in
  grub-probe when PV name is less than 10 charaters
- add grub2-fix-descriptor-leak-in-grub_util_is_imsm.patch - fix decriptor
  leak which later caused LVM warnings during grub-probe invocation
- remove --enable-grub-emu-usb - it is not needed on physical platform
* Tue Jul  9 2013 mchang@suse.com
- refresh grub2-fix-menu-in-xen-host-server.patch: In domU we
  have to add xen kernel to config. (bnc#825528)
* Wed Jun 26 2013 elchevive@opensuse.org
- updated existent translations and include new ones
  (es, lt, pt_BR, sl, tr)
* Sun Jun 16 2013 arvidjaar@gmail.com
- update to current upstream trunk rev 5042
  * drop upstream patches
  - grub2-correct-font-path.patch
  - grub2-fix-mo-not-copied-to-grubdir-locale.patch
  - grub2-stdio.in.patch
  - grub2-fix-build-error-on-flex-2.5.37.patch
  - grub2-quote-messages-in-grub.cfg.patch
  - 30_os-prober_UEFI_support.patch
  - grub2-fix-enumeration-of-extended-partition.patch
  - grub2-add-device-to-os_prober-linux-menuentry.patch
  - grub2-fix-tftp-endianness.patch
  - efidisk-ahci-workaround
  - grub2-grub-mount-return-failure-if-FUSE-failed.patch
  * rediff
  - rename-grub-info-file-to-grub2.patch
  - grub2-linux.patch
  - use-grub2-as-a-package-name.patch
  - grub2-iterate-and-hook-for-extended-partition.patch
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - grub2-secureboot-chainloader.patch
  * add
  - grub2-linguas.sh-no-rsync.patch
    + disable rsync in linguas.sh so it can be used during RPM build
    + disable auto-generated catalogs, they fail at the moment due to
    missing C.UTF-8 locale
  * update Makefile.util.am and Makefile.core.am
  * grub2-mknetdir is now in /usr/bin
  * generate po/LINGUAS for message catalogs using distributed linguas.sh
  * remove po/stamp-po during setup to trigger message catalogs rebuild
  * package bootinfo.txt on PPC (used by grub2-mkrescue)
* Sat Apr 13 2013 arvidjaar@gmail.com
- BuildRequires: help2man to generate man pages and package them too
* Fri Apr  5 2013 arvidjaar@gmail.com
- add grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch (bnc#810912)
  * use linuxefi in 30_os-prober if secure boot is enabled
* Wed Apr  3 2013 arvidjaar@gmail.com
- update rename-grub-info-file-to-grub2.patch
  * do not rename docs/grub2.texi here, do it in %%%%prep (we do it there
    conditionally already). It simplifies patch refreshing using quilt
    which does not support file rename.
* Wed Apr  3 2013 mchang@suse.com
- refresh grub2-secureboot-chainloader.patch: Fix wrongly aligned
  buffer address (bnc#811608)
* Thu Mar 28 2013 mchang@suse.com
- package Secure Boot CA file as /usr/lib64/efi/grub.der which
  could be used to verify signed image from build server
- add openSUSE-UEFI-CA-Certificate.crt, openSUSE Secure Boot CA
- add SLES-UEFI-CA-Certificate.crt, SUSE Linux Enterprise Secure
  Boot CA
* Mon Mar 25 2013 dvaleev@suse.com
- extraconfigure macro is not defined on ppc
* Sat Mar 23 2013 arvidjaar@gmail.com
- corretly set chainloaded image device handle in secure boot mode (bnc#809038)
* Wed Mar 13 2013 mchang@suse.com
- remove all compatible links in grub2-efi as now all concerned
  utilities are fixed
- superseding grub2-efi by grub2-x86_64-efi and grub2-i386-efi on
  x86_64 and ix86 respectively
- make grub2-x86_64-efi and grub2-i386-efi providing grub2-efi
  capability to not break package dependency
- handle upgrade from 12.2 by preseving grubenv and custom.cfg to
  new directory /boot/grub2, rename /boot/grub2-efi to
  /boot/grub2-efi.rpmsave to avoid confusion.
* Mon Mar 11 2013 arvidjaar@gmail.com
- move post scripts into corresponding subpackages to ensure they are
  run after updated binaries are installed. Currently it may happen
  that update-bootlader picks up old binaries.
- move requires for perl-Bootloader to target subpackages. Make sure
  efi requires minimal version that supports /boot/grub2.
- add requires(post) to force order of installation: grub2 => grub2-arch
  => grub2-efi
- split efi post in two parts. One that updates configuration and is part
  of grub2-efiarch and second that migrates settings and is part of
  grub2-efi. Only custom.cfg and grubenv may need migration. device.map
  is not relevant for EFI and new grub.cfg had been created at this point.
* Mon Mar 11 2013 mchang@suse.com
- add grub2-fix-tftp-endianness.patch from upstream (bnc#808582)
- add efinet and tftp to grub.efi (bnc#808582)
* Thu Mar  7 2013 seife+obs@b1-systems.com
- convert spec file to UTF-8
* Thu Mar  7 2013 mchang@suse.com
- add lvm to grub.efi (bnc#807989)
- add loadenv to grub.efi (bnc#807992)
* Mon Mar  4 2013 arvidjaar@gmail.com
- grub2-grub-mount-return-failure-if-FUSE-failed.patch - return error
  if fuse_main failed (bnc#802983)
* Mon Feb 25 2013 fcrozat@suse.com
- Fix build for SLES 11.
* Tue Feb 19 2013 duwe@suse.com
  Fix up bogus items from the previous merge:
  - efi_libdir = _libdir = /usr/lib
  - package /usr/lib/grub2 dir only once
  - move grub.efi to /usr/lib/grub2/%%{grubefiarch}/
  - create a symlink so that scripts can find it there.
* Thu Feb 14 2013 duwe@suse.com
- merge internal+external BS changes into superset spec file,
  remove obsolete dependencies
- merge SLES+openSUSE patches, restrict "grub-efi" to 12.2
- add efidisk-ahci-workaround (bnc#794674)
- fix unquoted-string-in-class.patch (bnc#788322)
* Fri Feb  8 2013 mchang@suse.com
- adapt to pesign-obs-integration changes
* Thu Feb  7 2013 mchang@suse.com
- grub.efi signing on build server.
* Thu Jan 31 2013 duwe@suse.com
- switch to out of source / subdir build
* Wed Jan 30 2013 mchang@suse.com
- sync from SLE-11 SP3 to date
- set empty prefix to grub.efi for looking up in current directory
- grub2-cdpath.patch: fix the grub.cfg not found when booting from
  optical disk
- put grub.efi in grub2's source module directory
- create links in system's efi directory to grub.efi
- arvidjaar: do not overwrite device path in grub2-cdpath.patch
* Wed Jan 30 2013 arvidjaar@gmail.com
- remove obsolete reference to /boot/grub2-efi and /usr/sbin/grub2-efi
  from grub2-once
- add GRUB_SAVEDFAULT description to /etc/default/grub
* Tue Jan 29 2013 mchang@suse.com
- set empty prefix to grub.efi for looking up in current directory
- remove grubcd.efi, as grub.efi can now be used for cdrom booting
* Mon Jan 28 2013 snwint@suse.de
- add fat module to grubcd
- explicitly set empty prefix to get grub to set $prefix to the currrent
  directory
* Fri Jan 18 2013 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- add grub2-secureboot-chainloader.patch, which expands the efi
  chainloader to be able to verify images via shim lock protocol.
* Fri Jan 18 2013 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485).
- update for cdrom boot support.
- grub2-cdpath.patch: fix the grub.cfg not found when booting from
  optical disk.
- grubcd.efi: the efi image used for optial disk booting, with
  reduced size and $prefix set to /EFI/BOOT.
* Tue Jan  8 2013 mchang@suse.com
- add grub2-fix-unquoted-string-in-class.patch (bnc#788322)
* Tue Jan  8 2013 arvidjaar@gmail.com
- add grub2-add-device-to-os_prober-linux-menuentry.patch (bnc#796919)
* Sun Jan  6 2013 arvidjaar@gmail.com
- add patch grub2-fix-enumeration-of-extended-partition.patch to
  fix enumeration of extended partitions with non-standard EBR (bnc#779534)
* Fri Jan  4 2013 arvidjaar@gmail.com
- add support for chainloading another UEFI bootloader to
  30_os-prober (bnc#775610)
* Fri Dec 21 2012 mchang@suse.com
- put 32-bit grub2 modules to /usr/lib/grub2
- put 64-bit grub2 modules to /usr/lib64/grub2 (x86_64-efi)
- put grub.efi to /usr/lib64/efi(x86_64) or /usr/lib/efi(i586)
* Tue Dec 18 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- add grub2-secureboot-chainloader.patch, which expands the efi
  chainloader to be able to verify images via shim lock protocol.
* Fri Nov 30 2012 mchang@suse.com
- replace %%{sles_version} by %%{suse_version}
- use correct product name
* Mon Nov 26 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- added secureboot patches which introduces new linuxefi module
  that is able to perform verifying signed images via exported
  protocol from shim. The insmod command will not function if
  secure boot enabled (as all modules should built in grub.efi
  and signed).
  - grub2-secureboot-add-linuxefi.patch
  - grub2-secureboot-use-linuxefi-on-uefi.patch
  - grub2-secureboot-no-insmod-on-sb.patch
  - grub2-secureboot-provide-linuxefi-config.patch
- Makefile.core.am : support building linuxefi module
- Make grub.efi image that is with all relevant modules incorporated
  and signed, it will be the second stage to the shim loader which
  will verified it when secureboot enabled.
- Make grub.efi's path to align with shim loader's default loader
  lookup path.
- The changes has been verified not affecting any factory instalation,
  but will allow us to run & test secure boot setup manually with shim.
* Thu Nov 22 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- In SLE-11 SP3, don't include any other architecture binaries
  except EFI, so we split packages by architecture binaries to
  meet the requirement.
  - grub2 : common utilties and config etc
  - grub2-efi : provide compatibilty to grub2-efi package
  - grub2-i386-pc : binaries for x86 legacy pc firmware
  - grub2-i386-efi : binaries for ia32 EFI firmware
  - grub2-x86_64-efi : binaries for x86_64 firmware
  - grub2-powerpc-ieee1275: binaries for powerpc open firmware
* Tue Nov 20 2012 arvidjaar@gmail.com
- update grub2-quote-messages-in-grub.cfg.patch to use upstream commit
* Mon Nov 19 2012 arvidjaar@gmail.com
- quote localized "Loading ..." messages in grub.cfg (bnc#790195)
* Mon Nov  5 2012 aj@suse.de
- We really only need makeinfo, so require that one where it exists.
* Thu Nov  1 2012 mchang@suse.com
- ship a Secure Boot UEFI compatible bootloader (fate#314485)
- Secure boot support in installer DVD (fate#314489)
- prime support for package on SLE-11 (SP3)
  - remove buildrequire to libuse and ncurses 32-bit devel packages
    as they are needed by grub-emu which we don't support
  - remove buildrequire to freetype2-devel-32bit as it's not need
    by grub2-mkfont and others
  - buildrequire to xz instead of lzma
  - buildrequire to texinfo instead of makeinfo
  - remove buildrequire to autogen as it's not available in SLE-11
  - add Makefile.util.am Makefile.core.am generated by autogen
  - run autoreconf -vi instead of ./autogen.sh
  - For SLE-11 remove buildrequire to gnu-unifont as it's not
    yet available. Also do not package pf fonts created from it.
  - workaround SLE-11 patch utility not rename file for us
  - add -fno-inline-functions-called-once to CFLAGS to fix build
    error on gcc 4.3.x
  - not require os-prober for SLE-11, as package not yet ready
* Sat Oct 27 2012 arvidjaar@gmail.com
- grub2-efi now depends on exact grub2 version
* Thu Oct 25 2012 arvidjaar@gmail.com
- build grub2-efi with standard "grub2" prefix (bnc#782891)
  - remove use-grub2-efi-as-a-package-name.patch
  - migrate settings from /boot/grub2-efi to /boot/grub2 in efi post
  - provide some compatibility links grub2-efi-xxx for perl-Bootloader
  - workaround for /boot/grub2-efi linkk and /boot/grub2/grub.cfg
    missing on update from older versions
* Thu Oct 25 2012 mchang@suse.com
- add grub2-fix-build-error-on-flex-2.5.37.patch
* Thu Oct 18 2012 arvidjaar@gmail.com
- modify patch grub2-iterate-and-hook-for-extended-partition.patch to
  ignore extended partitions other then primary (bnc#785341)
* Wed Sep 26 2012 mchang@suse.com
- refresh grub2-fix-locale-en.mo.gz-not-found-error-message.patch
  with the correct fix in upstream bugzilla #35880 by Colin Watson
  (bnc#771393)
* Fri Sep 21 2012 mchang@suse.com
- grub2-fix-locale-en.mo.gz-not-found-error-message.patch (bnc#771393)
* Wed Sep 19 2012 arvidjaar@gmail.com
- add 20_memtest86+ (bnc#780622)
* Tue Sep 18 2012 mchang@suse.com
- Fix un-bootable grub2 testing entry in grub's menu.lst (bnc#779370)
- Not add new grub2 testing entry if it's not found in menu.lst
- Update grub2 stuff and config if there's grub2 entry in menu.lst
- Check for current bootloader as update-bootloader acts on it
* Thu Aug 30 2012 mchang@suse.com
- add grub2-fix-Grub2-with-SUSE-Xen-package-install.patch (bnc#774666)
- add grub2-pass-corret-root-for-nfsroot.patch (bnc#774548)
* Mon Aug 20 2012 mchang@suse.com
- disable grub2-enable-theme-for-terminal-window.patch to use
  default black background due to current background has poor
  contrast to the font color (bnc#776244).
* Fri Aug 10 2012 jslaby@suse.de
- rename grub2once to grub2-once
* Wed Aug  1 2012 mchang@suse.com
- add grub2once (bnc#771587)
- add not-display-menu-when-boot-once.patch
* Sat Jul 28 2012 aj@suse.de
- Fix build with missing gets declaration (glibc 2.16)
* Fri Jul 27 2012 tittiatcoke@gmail.com
- Add grub2-enable-theme-for-terminal-window.patch (bnc#770107)
* Thu Jul 19 2012 mchang@suse.com
- add grub2-fix-menu-in-xen-host-server.patch (bnc#757895)
* Wed Jul 18 2012 mchang@suse.com
- add grub2-fix-error-terminal-gfxterm-isn-t-found.patch
- add grub2-fix-mo-not-copied-to-grubdir-locale.patch
* Wed Jul 18 2012 aj@suse.de
- We only need makeinfo, not texinfo for building.
* Tue Jul 17 2012 jslaby@suse.de
- fix build by adding texinfo to buildrequires.
* Fri Jul  6 2012 mchang@suse.com
- grub2-GRUB_CMDLINE_LINUX_RECOVERY-for-recovery-mode.patch. We
  don't run in sigle user mode for recovery, instead use different
  set kernel command line options which could be specified by this
  GRUB_CMDLINE_LINUX_RECOVERY setting.
* Wed Jul  4 2012 mchang@suse.com
- add use-grub2-efi-as-a-package-name.patch (bnc#769916)
* Fri Jun 29 2012 dvaleev@suse.com
- Add configuration support for serial terminal consoles. This will
  set the maximum screen size so that text is not overwritten.
* Fri Jun 29 2012 dvaleev@suse.com
- don't enable grub-emu-usb on ppc ppc641
* Thu Jun 28 2012 jslaby@suse.de
- update to 2.0 final
  * see ChangeLog for changes
* Mon Jun 25 2012 adrian@suse.de
- enable xz/lzma support for image file generation
* Sun Jun 24 2012 jslaby@suse.de
- update to 2.0 beta6, a snapshot from today
  * see ChangeLog for changes
* Fri Jun 22 2012 mchang@suse.com
- do not package grub.cfg, as it's generated at runtime and the
  presence of it would confuse pygrub (bnc#768063)
* Wed May 16 2012 mchang@suse.com
- fix build error on 12.1 caused by autogen aborts because of
  absence of guile package
* Wed May  2 2012 mchang@suse.com
- grub2-automake-1-11-2.patch : fix grub2 build error on newer
  autotools (automake >= 1.11.2)
- call ./autogen.sh
* Thu Apr 19 2012 mchang@suse.com
- grub2-probe-disk-mountby.patch : fix grub2-probe fails on
  probing mount-by devices under /dev/disk/by-(id|uuid|path).
  (bnc#757746)
* Thu Mar 29 2012 mchang@suse.com
- Add Requires to os-prober as script depends on it for probing
  foreign os (bnc#753229)
* Wed Mar 21 2012 mchang@suse.com
- Mark %%config(noreplace) to /etc/default/grub (bnc#753246)
* Fri Mar 16 2012 aj@suse.de
- Fix build with gcc 4.7 (needs -fno-strict-aliasing for zfs code).
* Tue Mar 13 2012 mchang@suse.com
- Fix error in installation to extended partition (bnc#750897)
  add grub2-iterate-and-hook-for-extended-partition.patch
  add grub2-install-opt-skip-fs-probe.patch
* Mon Mar 12 2012 tittiatcoke@gmail.com
- Added BuildRequires for gnu-unifont in order to create the
  necessary fonts for a graphical boot menu.
* Mon Feb 20 2012 andrea.turrini@gmail.com
- fixed typos in grub2.spec
* Mon Jan  2 2012 mchang@suse.com
- platforms without efi should not specify exclusion of it
* Thu Dec 29 2011 mchang@suse.com
- set --target=%%{_target_plaform) explicitly to %%configure in case
  it wouldn't do that for us implicitly
- when making x86_64-efi image not use i386 target build and keep
  use of x86_64. otherwise it would have error "invalid ELF header"
* Fri Dec  2 2011 coolo@suse.com
- add automake as buildrequire to avoid implicit dependency
* Mon Nov 28 2011 jslaby@suse.de
- remove doubly packaged files
- remove INSTALL from docs
- handle duplicate bindir files
* Mon Oct 31 2011 meissner@suse.de
- make efi exclusion more complete
* Thu Oct 27 2011 aj@suse.de
- efibootmgr only exists on x86-64 and ia64.
* Tue Oct 25 2011 aj@suse.de
- Add requires from efi subpackage to main package (bnc#72596)
* Mon Oct 24 2011 jslaby@suse.de
- update it and pl translations
- cleanup spec file
  * don't package efi files to non-efi package
* Thu Aug 25 2011 aj@suse.de
- Fix directory ownership.
* Tue Aug 23 2011 aj@suse.de
- Build an efi subpackage [bnc#713595].
* Tue Aug  2 2011 dvaleev@novell.com
- enable ppc build
- patch unused-but-set-variable
* Tue Jul 12 2011 aj@suse.de
- Create submenu for all besides primary Linux kernels.
- Only run preun section during package install but not during
  upgrade.
* Tue Jul 12 2011 aj@suse.de
- Update README.openSUSE
* Tue May 31 2011 jslaby@suse.de
- update translations
- update to 1.99 final
  * See NEWS file for changes
* Sat May  7 2011 jslaby@suse.de
- fix build with gcc 4.6
- build in parallel (fixed finally in 1.99)
- add translations from translations project
- update to 1.99-rc2
  * See NEWS file for changes
* Wed Oct 27 2010 jslaby@suse.de
- fix vanishing of /boot/grub2/* if /boot/grub/device.map
  doesn't exist
* Mon Oct 25 2010 jslaby@suse.de
- add missing " in the default file; add "fi" to grub2-linux.patch
* Mon Oct 11 2010 jslaby@suse.de
- repack gz to bz2 (0.5M saving)
* Sat Oct  9 2010 aj@suse.de
- Do not output vmlinux if vmlinuz of same version exists.
- Update default grub file.
* Sat Oct  9 2010 aj@suse.de
- Add patch grub-1.98-follow-dev-mapper-symlinks.patch from Fedora
  for grub2-probe to detect lvm devices correctly
* Sat Sep 11 2010 jslaby@suse.de
- add gettext "requires"
* Sun Mar 14 2010 aj@suse.de
- Fix build on x86-64.
* Fri Mar 12 2010 aj@suse.de
- Don't build parallel.
- Update to grub 1.98 including:
  * Multiboot on EFI support.
  * Saved default menu entry support, with new utilities `grub-reboot' and
    `grub-set-default'.
  * Encrypted password support, with a new utility `grub-mkpasswd-pbkdf2'.
  * `grub-mkfloppy' removed; use `grub-mkrescue' to create floppy images.
* Fri Feb 12 2010 aj@suse.de
- Update to grub 1.97.2:
  * Fix a few 4 GiB limits.
  * Fix license problems with a few BSD headers.
  * Lots of misc bugfixes.
* Wed Dec  9 2009 aj@suse.de
- Fix requires.
* Wed Dec  9 2009 aj@suse.de
- Mark /etc/default/grub as config file.
* Wed Dec  9 2009 aj@suse.de
- Mark root partition rw
* Wed Dec  9 2009 aj@suse.de
- New package grub2.
