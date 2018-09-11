from distutils.core import setup
import py2exe,sys,os

sys.argv.append('py2exe')


setup(options = {'py2exe':{\
                           'packages':['Pmw']}},\
      windows =[{'script':'HomePage.py'}],\
      zipfile =None)
