class AccountError(Exception):
  def __init__(self, value):
    self.value = value
  def str(self):
    return repr(self.value)
 
def make_account(balance):
  def withdraw(amount):
    nonlocal balance
    if balance >= amount:
      balance = balance - amount
    else:
      raise AccountError("Account balance too low")
      
  def deposit(amount):
    #nonlocal balance
    balance = balance + amount
  
  def get_value():
    return balance
  
  public_methods = {'withdraw' : withdraw, 'deposit' : deposit, 'get_value' : get_value}
  return public_methods