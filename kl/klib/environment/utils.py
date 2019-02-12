
import klib.exception

def function_modifiers(node):
  modifiers_args = {}
  for mod in node.modifiers:
    if mod == "__pure__":
      modifiers_args['pure'] = True
    else:
      raise klib.exception("Unknown function modifier: {} for function {}".format(mod, node.name))
  return modifiers_args
