
class multi_listeners:
  def __init__(self, listners):
    self.listners = listners
  def import_statement(self, *args):
    for l in self.listners:
      l.import_statement(*args)

  def named_block(self, *args):
    for l in self.listners:
      l.named_block(*args)
    
  def start_block_expression(self, *args):
    for l in self.listners:
      l.start_block_expression(*args)
  
  def end_block_expression(self, *args):
    for l in self.listners:
      l.end_block_expression(*args)
  
  def start_group_expression(self, *args):
    for l in self.listners:
      l.start_group_expression(*args)
  
  def end_group_expression(self, *args):
    for l in self.listners:
      l.end_group_expression(*args)
  
  def start_expression(self, *args):
    for l in self.listners:
      l.start_expression(*args)
  
  def end_expression(self, *args):
    for l in self.listners:
      l.end_expression(*args)
    
  def clear_expression(self, *args):
    for l in self.listners:
      l.clear_expression(*args)
    
  def return_expression(self, *args):
    for l in self.listners:
      l.return_expression(*args)
    
  def value_expression(self, *args):
    for l in self.listners:
      l.value_expression(*args)
    
  def identifier_expression(self, *args):
    for l in self.listners:
      l.identifier_expression(*args)

  def binary_expression(self, *args):
    for l in self.listners:
      l.binary_expression(*args)
    
  def unary_expression(self, *args):
    for l in self.listners:
      l.unary_expression(*args)

  def cond_expression(self, *args):
    for l in self.listners:
      l.cond_expression(*args)

  def native_call_expression(self, *args):
    for l in self.listners:
      l.native_call_expression(*args)
    
  def function_call_expression(self, *args):
    for l in self.listners:
      l.function_call_expression(*args)

  def lambda_declaration_expression(self, *args):
    for l in self.listners:
      l.lambda_declaration_expression(*args)

  def env_expression(self, *args):
    for l in self.listners:
      l.env_expression(*args)

  def raise_expression(self, *args):
    for l in self.listners:
      l.raise_expression(*args)

  def catch_expression(self, *args):
    for l in self.listners:
      l.catch_expression(*args)

  def call_trace_expression(self, *args):
    for l in self.listners:
      l.call_trace_expression(*args)
