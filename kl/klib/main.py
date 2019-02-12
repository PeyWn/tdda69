import os

import klib.vm
import klib.io
import klib.interpreter
from klib.parser import parse_error, print_listener
from klib.io import stdout
from klib.native.python import abort_exception

def print_trace(stack_trace):
  for trace in stack_trace:
    stdout.writeln("  File \"{}\", line {}, column {}, in {}", trace.filename, trace.line, trace.column, trace.blockname)

def execute_script(input_file, propagate_exception, developer_verbose, test_type, include_dirs):
  module = klib.interpreter.module()
  extra_listeners = None
  if developer_verbose:
    extra_listeners = [print_listener(stdout)]
  try:
    module.load_file(input_file, extra_listeners = extra_listeners, developer_verbose = developer_verbose, include_dirs = include_dirs)
  except klib.parser.parse_error as em:
    stdout.writeln("  File \"{}\", line {}, column {}", em.filename, em.line, em.column)
    stdout.writeln("  Parse error: {}", em.message)
    if(propagate_exception):
      raise em
    return -1
  except klib.exception as em:
    if test_type == "run_success":
      stdout.writeln("Test failed: {}", em.message)
      return -1
    elif test_type == "run_fail":
      return 0
    else:
      stdout.writeln("Error: {}", em.message)
      if(propagate_exception):
        raise em
      return -1
  except abort_exception as ae:
    if test_type == "run_success":
      print_trace(ae.stack_trace)
      stdout.writeln("Test failed: {}", ae.args[0])
      return -1
    elif test_type == "run_fail":
      return 0
    else:
      print_trace(ae.stack_trace)
      stdout.writeln("Aborted: {}", ae.args[0])
      return -1
  if test_type == "run_fail":
    stdout.writeln("No failure detected!")
    return -1
  return 0

def main(argv):
  
  show_help     = False
  show_version  = False
  input_file    = None
  propagate_exception = False
  developer_verbose   = False
  test_type     = None
  test_suite    = None
  include_dirs  = []

  arg_i = 0
  while arg_i < len(argv):
    if(argv[arg_i] == "--help"):
      show_help = True
    elif(argv[arg_i] == "--version"):
      show_version = True
    elif(argv[arg_i] == "--propagate-exception"):
      propagate_exception = True
    elif(argv[arg_i] == "--developer-verbose"):
      developer_verbose = True
    elif(argv[arg_i] == "--test"):
      test_type = argv[arg_i + 1]
      arg_i += 1
    elif(argv[arg_i] == "--test-suite"):
      test_suite = argv[arg_i]
    elif argv[arg_i] == "--include-dir":
      include_dirs.append(argv[arg_i + 1])
      arg_i += 1
    else:
      input_file = argv[arg_i]
    arg_i += 1

  if(show_version):
    stdout.writeln("Kernel Language v0.9.0")
    return 0
  
  if test_suite and test_type:
    stdout.writeln("Cannot specify a test suite and test type")
    return -1
  
  if(show_help or input_file == None):
    stdout.writeln("kl [--help] [--version] [input_filename]")
    stdout.writeln("--help: show this help message")
    stdout.writeln("--version: show the version")
    stdout.writeln("--propagate-exception: ")
    stdout.writeln("--developer-verbose: ")
    stdout.writeln("--test [type]: run a test where type is:\n"
                   "   * 'run_success' if the test is expected to succeed\n"
                   "   * 'run_fail' if the test is expected to fail\n")
    stdout.writeln("--test-suite: run all the tests listed in the file")
    stdout.writeln("input_filename: name of the file to execute")
    return 0
  
  if test_suite != None:
    test_suite_file = klib.io.input_file_stream(input_file)
    failures = 0
    while not test_suite_file.at_end_of_stream:
      t = test_suite_file.read_line()
      if t != "":
        test_file_name = os.path.join(os.path.dirname(input_file), t)
        test_file = klib.io.input_file_stream(test_file_name)
        shebang_line = test_file.read_line()
        if shebang_line[0:2] == "#!":
          shebang = shebang_line.split(" ")
          test_type = None
          shebang_i = 0
          while shebang_i < len(shebang):
            if shebang[shebang_i] == "--test":
              test_type = shebang[shebang_i+1]
              break
            shebang_i += 1
          if test_type:
            if(execute_script(test_file_name, False, False, test_type, include_dirs) == 0):
              stdout.writeln("{}: success", t)
            else:
              stdout.writeln("{}: failed", t)
              failures += 1
          else:
            stdout.writeln("{}: invalid test, missing '--test'!", t)
            failures += 1
        else:
          stdout.writeln("{}: invalid test, missing shebang!", t)
          failures += 1
          
    if failures > 0:
      stdout.writeln("There was {} failures".format(failures))
      return -1
    else:
      stdout.writeln("Test suite was successful")
      return 0
  else:
    ret = execute_script(input_file, propagate_exception, developer_verbose, test_type, include_dirs)
    if ret == 0 and test_type != None:
      stdout.writeln("Test pass.")
    return ret
