#!/usr/bin/env python3

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))

import unittest

import klib.bytecode
import klib.environment
import klib.vm
import klib.parser

class TestExecutor(unittest.TestCase):

  def run_test_executor(self, instructions, expected_stack, initial_environment, expected_environment):
    code     = klib.bytecode.program()
    
    for i in range(0, len(instructions)):
      (opcode, arguments) = instructions[i]
      code.add_instruction(klib.bytecode.instruction(opcode, klib.parser.metadata(i, 0, None, None, None), **arguments))
    env      = klib.environment.environment()

    for key, value in initial_environment.items():
      env.define_cell(key, value)
    
    executor = klib.vm.executor()
    actual_stack = executor.execute(code, env, verbose = True)

    if expected_stack:
      self.assertEqual(len(expected_stack), len(actual_stack))
      
      for i in range(0, len(expected_stack)):
        f_elt = expected_stack[i]
        a_elt = actual_stack[i]
        #if(isinstance(f_elt, Object) or isinstance(f_elt, Function)):
          #self.assertEqual(f_elt.__class__, a_elt.__class__)
        #else:
        self.assertEqual(f_elt, a_elt)
    
    if expected_environment:
      self.assertEqual(len(expected_environment.items()), len(env))
      for key, value in expected_environment.items():
        self.assertEqual(env.get(key).get_value(), value)
      
    return (actual_stack, env)
    
  def test_001_push(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, {"value": 1.0}), (klib.bytecode.opcodes.PUSH, {"value": -1.0})],
      [1.0, -1.0],
      {}, {})
  
  def test_002_pop(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, {"value": 1.0}), (klib.bytecode.opcodes.PUSH, {"value": -1.0}), (klib.bytecode.opcodes.PUSH, {"value": 0.0}), (klib.bytecode.opcodes.POP, {"count": 2})],
      [1.0],
      {}, {})
  
  def test_003_dup(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, {"value": 1.0}), (klib.bytecode.opcodes.DUP, {})],
      [1.0, 1.0],
      {}, {})
  
  def test_004_swap(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, {"value": 1.0}), (klib.bytecode.opcodes.PUSH, {"value": -1.0}), (klib.bytecode.opcodes.SWAP, {})],
      [-1.0, 1.0],
      {}, {})
  
  def test_010_push_env(self):
    (stack, env) = self.run_test_executor([(klib.bytecode.opcodes.PUSH_ENV, {})], None, {}, None)
    self.assertEqual(len(stack), 1)
    self.assertEqual(stack[0], env)
  
  def test_011_new_env(self):
    (stack, env) = self.run_test_executor(
      [(klib.bytecode.opcodes.NEW_ENV, {}),
       (klib.bytecode.opcodes.PUSH_ENV, {})],
      None, {}, None)
    self.assertEqual(len(stack), 1)
    self.assertNotEqual(stack[0], env)
    self.assertTrue(isinstance(stack[0], klib.environment.environment))
    self.assertEqual(stack[0].parent, env)
  
  def test_012_drop_env(self):
    (stack, env) = self.run_test_executor(
      [(klib.bytecode.opcodes.NEW_ENV, {}),
       (klib.bytecode.opcodes.DROP_ENV, {}),
       (klib.bytecode.opcodes.PUSH_ENV, {})],
      None, {}, None)
    self.assertEqual(len(stack), 1)
    self.assertEqual(stack[0], env)
  
  def test_013_make_ref(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.MAKE_REF, { "name": 'a'}),
       (klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.PUSH, {"value": 'b'}),
       (klib.bytecode.opcodes.MAKE_REF, {})],
      [],
      { }, { })
  
  def test_014_store(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.PUSH, {"value": -1.0}),
       (klib.bytecode.opcodes.STORE, { "name": 'a'}),
       (klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.MAKE_REF, { "name": 'b'}),
       (klib.bytecode.opcodes.PUSH, {"value": -1.5}),
       (klib.bytecode.opcodes.STORE, { }),
       (klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.MAKE_REF, { "name": 'c'}),
       (klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.MAKE_REF, { "name": 'a'}),
       (klib.bytecode.opcodes.STORE, { })],
      [-1.0, -1.5, -1.0],
      { 'a': 1.0, 'b': None, 'c': None }, { 'a': -1.0, 'b': -1.5, 'c': -1.0 })
      
  def test_015_dcl_cell(self):
    (stack, env) = self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.DUP, {}),
       (klib.bytecode.opcodes.DCL_CELL, { "name": 'a' }),
       (klib.bytecode.opcodes.PUSH, {"value": -1.0}),
       (klib.bytecode.opcodes.STORE, { "name": 'a'})],
      [-1.0],
      { },
      { 'a': -1.0 })
    self.assertTrue(env.get("a").is_writable())
      
  def test_016_def_value(self):
    (stack, env) = self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.PUSH, {"value": -1.0}),
       (klib.bytecode.opcodes.DEF_VALUE, { "name": 'a' })],
      [],
      { },
      { 'a': -1.0 })
    self.assertFalse(env.get("a").is_writable())
      
  def test_017_clear(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.CLEAR, { "name": 'a' }),
       (klib.bytecode.opcodes.PUSH_ENV, {}),
       (klib.bytecode.opcodes.MAKE_REF, { "name": 'b'}),
       (klib.bytecode.opcodes.CLEAR, { })],
      [None, None],
      { 'a': -1.0, 'b': 3.0, 'c': 5.0 },
      { 'c': 5.0 })
  
  def test_018_push_call_trace(self):
    (stack, env) = self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH_CALL_TRACE, {}), (klib.bytecode.opcodes.PUSH_CALL_TRACE, {})],
      None, {}, None)
    self.assertEqual(len(stack), 2)
    ct = stack[0]
    self.assertEqual(len(ct), 1)
    self.assertEqual(ct[0].line, 0)
    self.assertEqual(ct[0].column, 0)
    self.assertEqual(ct[0].filename, None)
    self.assertEqual(ct[0].blockname, None)
    self.assertEqual(ct[0].parent, None)
    ct = stack[1]
    self.assertEqual(len(ct), 1)
    self.assertEqual(ct[0].line, 1)
    self.assertEqual(ct[0].column, 0)
    self.assertEqual(ct[0].filename, None)
    self.assertEqual(ct[0].blockname, None)
    self.assertEqual(ct[0].parent, None)  

  def test_020_jmp(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.JMP, { "index": 2}), (klib.bytecode.opcodes.PUSH, { "value": 1.0 }), (klib.bytecode.opcodes.PUSH, { "value": -1.0}) ],
      [-1.0],
      { }, { })

  def test_021_ifjmp(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, { "value": True}), (klib.bytecode.opcodes.IFJMP, { "index": 3}), (klib.bytecode.opcodes.PUSH, { "value": 1.0 }), (klib.bytecode.opcodes.PUSH, { "value": -1.0 }) ],
      [-1.0],
      { }, { })
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, { "value": False}), (klib.bytecode.opcodes.IFJMP, { "index": 3}), (klib.bytecode.opcodes.PUSH, { "value": 1.0 }), (klib.bytecode.opcodes.PUSH, { "value": -1.0 }) ],
      [1.0, -1.0],
      { }, { })

  def test_022_unlessjmp(self):
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, { "value": False}), (klib.bytecode.opcodes.IFJMP, { "index": 3}), (klib.bytecode.opcodes.PUSH, { "value": 1.0 }), (klib.bytecode.opcodes.PUSH, { "value": -1.0 }) ],
      [1.0, -1.0],
      { }, { })
    self.run_test_executor( 
      [(klib.bytecode.opcodes.PUSH, { "value": True}), (klib.bytecode.opcodes.IFJMP, { "index": 3}), (klib.bytecode.opcodes.PUSH, { "value": 1.0 }), (klib.bytecode.opcodes.PUSH, { "value": -1.0 }) ],
      [-1.0],
      { }, { })

  def test_023_ret(self):
    # Simple
    code     = klib.bytecode.program()
    
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.PUSH, klib.parser.metadata(0, 0, None, None, None), value = "test"))
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.RET, klib.parser.metadata(1, 0, None, None, None)))
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.PUSH, klib.parser.metadata(2, 0, None, None, None), value = "test2"))
    env      = klib.environment.environment()

    executor = klib.vm.executor()
    result = executor.execute(code, env, return_stack = False)

    self.assertEqual(result, "test")
  
    # Return the value of a reference
    code     = klib.bytecode.program()
    
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.PUSH_ENV, klib.parser.metadata(0, 0, None, None, None)))
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.MAKE_REF, klib.parser.metadata(0, 0, None, None, None), name = "test"))
    code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.RET, klib.parser.metadata(1, 0, None, None, None)))
    env      = klib.environment.environment()
    env.define_value("test", init_value = "somevalue")

    executor = klib.vm.executor()
    result = executor.execute(code, env, return_stack = False)

    self.assertEqual(result, "somevalue")
  
  
  def test_024_native_call(self):
    self.run_test_executor(
      [(klib.bytecode.opcodes.PUSH, { "value": "test"}),
       (klib.bytecode.opcodes.NATIVE_CALL, {"native_function": klib.native.modules["py"].get("identity"), "count": 1})],
      ["test"], {}, {})
  
  def test_025_call(self):
    func_code = klib.bytecode.program()
    
    func_code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.PUSH_ENV, klib.parser.metadata(0, 0, None, None, None)))
    func_code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.MAKE_REF, klib.parser.metadata(0, 0, None, None, None), name = "arg"))
    func_code.add_instruction(klib.bytecode.instruction(klib.bytecode.opcodes.RET, klib.parser.metadata(1, 0, None, None, None)))

    function = klib.environment.function(["arg"], None, None, program = func_code)
    
    self.run_test_executor( 
      [ (klib.bytecode.opcodes.PUSH, { "value": "test"}),
        (klib.bytecode.opcodes.PUSH, { "value": function}),
        (klib.bytecode.opcodes.CALL, { "count": 1}) ],
      ["test"],
      { }, { })

  def test_03x_exception(self):
    self.run_test_executor(
      [ (klib.bytecode.opcodes.TRY_PUSH, {"index": 5}),
        (klib.bytecode.opcodes.PUSH, {"value": 1.0}),
        (klib.bytecode.opcodes.THROW, {}),
        (klib.bytecode.opcodes.PUSH, {"value": 3.0}),
        (klib.bytecode.opcodes.TRY_POP, {})], [1.0], {}, {})
  
    self.assertRaises(klib.interpreter.kl_exception, self.run_test_executor, [(klib.bytecode.opcodes.PUSH, {"value": 1.0}), (klib.bytecode.opcodes.THROW, {}) ], [], {}, {})
    self.assertRaises(klib.interpreter.kl_exception, self.run_test_executor,
                      [(klib.bytecode.opcodes.TRY_PUSH, {"index": 5}),
                       (klib.bytecode.opcodes.PUSH, {"value": 1.0}),
                       (klib.bytecode.opcodes.PUSH, {"value": 3.0}),
                       (klib.bytecode.opcodes.TRY_POP, {}),
                       (klib.bytecode.opcodes.THROW, {})],
                      [], {}, {})
    
  def test_040_make_function(self):
    args = ['a', 'b']
    body = "nobody"
    modifiers = {}
    (stack, env) = self.run_test_executor([(klib.bytecode.opcodes.MAKE_FUNC, {"body": body, "argument_names": args, "modifiers": modifiers})], None, {}, {})
    self.assertEqual(len(stack), 1)
    self.assertEqual(stack[0].argument_names, args)
    self.assertEqual(stack[0].body, body)
  
  def run_test_binary(self, opcode, arg1, arg2, result):
    self.run_test_executor([(klib.bytecode.opcodes.PUSH, {"value": arg1}), (klib.bytecode.opcodes.PUSH, {"value": arg2}), (opcode, {})], [result], {}, {})
  
  def test_050_add(self):
    self.run_test_binary(klib.bytecode.opcodes.ADD, 1.0, 2.0, 3.0)

  def test_051_sub(self):
    self.run_test_binary(klib.bytecode.opcodes.SUB, 1.0, 2.0,-1.0)
  
  def test_052_div(self):
    self.run_test_binary(klib.bytecode.opcodes.DIV, 1.0, 2.0, 0.5)
  
  def test_053_mul(self):
    self.run_test_binary(klib.bytecode.opcodes.MUL, 3.0, 2.0, 6.0)
  
  def test_054_mod(self):
    self.run_test_binary(klib.bytecode.opcodes.MOD, 7.0, 2.0, 1.0)
  
  def test_055_left_shift(self):
    self.run_test_binary(klib.bytecode.opcodes.LEFT_SHIFT, 10.0, 2.0, 40.0)
    
  def test_056_right_shift(self):
    self.run_test_binary(klib.bytecode.opcodes.RIGHT_SHIFT, 10.0, 2.0, 2.0)
    
  def test_057_unsigned_right_shift(self):
    self.run_test_binary(klib.bytecode.opcodes.UNSIGNED_RIGHT_SHIFT, -8.0, 2.0, 1073741822.0)
    
  def test_060_supperior(self):
    self.run_test_binary(klib.bytecode.opcodes.GREATER, -8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.GREATER,  8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.GREATER,  2.0, 2.0, False)
  
  def test_061_supperior_equal(self):
    self.run_test_binary(klib.bytecode.opcodes.GREATER_EQUAL, -8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.GREATER_EQUAL,  8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.GREATER_EQUAL,  2.0, 2.0, True)
  
  def test_062_inferior(self):
    self.run_test_binary(klib.bytecode.opcodes.LESS, -8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.LESS,  8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.LESS,  2.0, 2.0, False)
  
  def test_063_inferior_equal(self):
    self.run_test_binary(klib.bytecode.opcodes.LESS_EQUAL, -8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.LESS_EQUAL,  8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.LESS_EQUAL,  2.0, 2.0, True)
  
  def test_064_equal(self):
    self.run_test_binary(klib.bytecode.opcodes.EQUAL, -8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.EQUAL,  8.0, 2.0, False)
    self.run_test_binary(klib.bytecode.opcodes.EQUAL,  2.0, 2.0, True)
  
  def test_065_different(self):
    self.run_test_binary(klib.bytecode.opcodes.DIFFERENT, -8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.DIFFERENT,  8.0, 2.0, True)
    self.run_test_binary(klib.bytecode.opcodes.DIFFERENT,  2.0, 2.0, False)
  
  def test_066_and(self):
    self.run_test_binary(klib.bytecode.opcodes.AND, True, True, True)
    self.run_test_binary(klib.bytecode.opcodes.AND, True, False, False)
    self.run_test_binary(klib.bytecode.opcodes.AND, False, True, False)
    self.run_test_binary(klib.bytecode.opcodes.AND, False, False, False)
  
  def test_067_and(self):
    self.run_test_binary(klib.bytecode.opcodes.OR, True, True, True)
    self.run_test_binary(klib.bytecode.opcodes.OR, True, False, True)
    self.run_test_binary(klib.bytecode.opcodes.OR, False, True, True)
    self.run_test_binary(klib.bytecode.opcodes.OR, False, False, False)
  
  def run_test_unary(self, opcode, arg, result):
    self.run_test_executor([(klib.bytecode.opcodes.PUSH, { "value": arg}), (opcode, {})], [result], {}, {})
  
  def test_070_neg(self):
    self.run_test_unary(klib.bytecode.opcodes.NEG, 1.0, -1.0)
  
  def test_071_tilde(self):
    self.run_test_unary(klib.bytecode.opcodes.TILDE, 10.0,-11.0)
  
  def test_072_not(self):
    self.run_test_unary(klib.bytecode.opcodes.NOT, True, False)
    self.run_test_unary(klib.bytecode.opcodes.NOT, False, True)

if __name__ == '__main__':
  unittest.main(failfast=True)  # Only test until first failure
