from distutils.core import setup, Extension
setup(name="emb", version='1.0', ext_modules=[Extension('emb',['c-2-py-2.c'])])
setup(name="hworld", version='1.0', ext_modules=[Extension('hworld',['c-2-py-3.c'])])

