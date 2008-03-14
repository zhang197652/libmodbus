#! /usr/bin/env python
# encoding: utf-8

VERSION='1.9.0'
APPNAME='libmodbus'

# these variables are mandatory ('/' are converted automatically)
srcdir = '.'
blddir = 'build'

def init():
     print "A groovy libmodbus for Linux!"

def set_options(opt):
     # options provided by the modules
     opt.tool_options('compiler_cc')

def configure(conf):
     conf.check_tool('compiler_cc')
     conf.check_tool('misc')

     headers = 'arpa/inet.h fcntl.h netinet/in.h stdlib.h \
                string.h sys/ioctl.h sys/socket.h sys/time.h \
                termio.h termios.h unistd.h'

     # check for headers and append found headers to headers_found for later use
     headers_found = []
     for header in headers.split():
          if conf.check_header(header):
               headers_found.append(header)

     functions_defines = (
          ('inet_ntoa', 'HAVE_INET_NTOA'),
          ('memset', 'HAVE_MEMSET'),
          ('select', 'HAVE_SELECT'),
          ('socket', 'HAVE_SOCKET'))

     for (function, define) in functions_defines:
          e = conf.create_function_enumerator()
          e.mandatory = True
          e.function = function
          e.headers = headers_found
          e.define = define
          e.run()
 
     conf.define('VERSION', VERSION)
     conf.define('PACKAGE', 'libmodbus')

     conf.write_config_header()

def build(bld):
     import misc

     bld.add_subdirs('src')  

     obj = bld.create_obj('subst')
     obj.source = 'modbus.pc.in'
     obj.target = 'modbus.pc'
    
     obj.dict = {'VERSION' : VERSION, 
                 'prefix': bld.env()['PREFIX'], 
                 'exec_prefix': bld.env()['PREFIX'],
                 'libdir': bld.env()['PREFIX'] + '/lib', 
                 'includedir': bld.env()['PREFIX'] + '/include'}

def shutdown():
     import UnitTest
     unittest = UnitTest.unit_test()
     unittest.run()
     unittest.print_results()
