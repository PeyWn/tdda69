function a(arg1, arg2) pure // specify this function is pure (pure/unpured is optional keyword, which
{
  
}

thread name {
}

thread name a(1, 2);

function b(arg1, arg2) unpure // unpure function can only be used by one thread
{
  r = thread a(1, 2);
  r.wait();
  print(r)
}

value a 10;
value a {
 b: 5
 c: { a: 4, d: func(1) }
}

stream reader_s writer_s;

port writer_s port_name; // writer_s ownership is given to the port

thread printer {
  reader_s.wait()
  print(reader_s.next()) // only one thread can use the print function
}

thread {
  writer_s.send("Hello")
}

thread {
  writer_s.send("World")
}

% implemented as macro

typedfunction b -> int (arg1 -> int, arg2 -> string)
{
}

class B
{
  B()
  {
  }
  function do()
  {
  }
}

function a()
{
  while()
  {
  }
} // transformed into recursion

macro factorial($x) -> $x*factorial(${x-1}) // $x indicates any value ${x-1} indicate subsitute by the result of the expression 
macro factorial(0) -> 1

macro abs($x) -> $x
macro abs($x{x<0}) -> ${-x} // $x{x<0} indicates a rule on the value of x
