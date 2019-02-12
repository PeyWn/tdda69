import klib.interpreter.module
import os

class modules_manager:
  '''
  Handle importing of modules
  '''  
  def __init__(self):
    self.loaded_modules = dict()
    self.search_path = [os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "modules"))]

  def import_module(self, module, major_version, minor_version):
    key = ".".join(module)
    if(key in self.loaded_modules):
      mv = self.loaded_modules[module]
      if(major_version in mv):
        best_miver = float("inf")
        best_mod   = None
        for miver, mod in mv.iteritems():
          if miver >= minor_version and miver < best_miver:
            best_miver  = miver
            best_mod    = mod
        if best_mod:
          return best_mod
    best_miver = float("inf")
    best_path  = None
    for path in self.search_path:
      mpath = os.path.join(path, *module)
      if(os.path.exists(mpath)):
        
        for f in os.listdir(mpath):
          major_v, minor_v = f.split(".")
          if(int(major_v) == major_version and int(minor_v) >= minor_version and int(minor_v) < best_miver):
            best_miver = int(minor_v)
            best_path  = os.path.join(mpath, f, "__init__.kl")
    if(best_path):
      mod = klib.interpreter.module(self)
      mod.load_file(best_path)
      self.loaded_modules[key] = [mod]
      return mod
    else:
      raise Exception("Module {} {}.{} not found.".format(module, major_version, minor_version))
