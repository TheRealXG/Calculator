#
# Hello world Waf script
#
from __future__ import print_function

rtems_version = "5"

try:
    import rtems_waf.rtems as rtems
except:
    print('error: no rtems_waf git submodule')
    import sys
    sys.exit(1)

def init(ctx):
    rtems.init(ctx, version = rtems_version, long_commands = True)

def bsp_configure(conf, arch_bsp):
    # Add BSP specific configuration checks
    pass

def options(opt):
    rtems.options(opt)

def configure(conf):
    rtems.configure(conf, bsp_configure = bsp_configure)

def build(bld):
    rtems.build(bld)

    bld(features = 'c cprogram',
        target = 'rtems/calc.exe',
        cflags = '-g -O2',
	includes = 'gen man',
        source = ['man/main.c',
		'man/init.c',
		'man/memcpy.c',
		'man/printUtils.c',
		'gen/kcg_types.c',
		'gen/root_Calc.c',
		'gen/kcg_consts.c',
		'gen/key2Char_Calc.c',
		'gen/valueEntry_Calc.c',
		'gen/performFunction_Calc.c',
                'gen/updateDisplay_Calc_Utils.c'])
