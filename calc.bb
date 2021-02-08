DESCRIPTION = "This package contains the simple calc program."
LICENSE = "CLOSED"

SRC_URI = "file://*"

S = "${WORKDIR}"

FILES_{$PN} = "calc"
TARGET_CC_ARCH += "${LDFLAGS}"

do_install() {
  install -d ${D}${bindir}
  install -m 0755 calc ${D}${bindir}
}
