import os

class input_stream:
  '''
  Represent an input stream.
  fd is a file descriptor, for instance returned by sys.open
  '''
  def __init__(self, fd):
    self.fd = fd
    self.char_queue = []
    self.at_end_of_stream = False
  
  def read_line(self):
    buffer = ""
    while True:
      c = self.next_char()
      if self.at_end_of_stream or c == '\n':
        break
      buffer += c
    return buffer
  
  def next_char(self):
    if(len(self.char_queue) == 0):
      c = os.read(self.fd, 1)
      if(len(c) == 0):
        self.at_end_of_stream = True
        return None
      else:
        if(c[0] & 0xC0 == 0xC0):
          oc = os.read(self.fd, 1)
          c = c + oc
        elif(c[0] & 0xE0 == 0xE0):
          oc = os.read(self.fd, 2)
          c = c + oc
        elif(c[0] & 0xF0 == 0xF0):
          oc = os.read(self.fd, 3)
          c = c + oc
        return c.decode("utf-8") 
    else:
      return self.char_queue.pop()
  def unget_char(self, c):
    self.char_queue.append(c)
    
  def end_of_stream(self):
    return self.at_end_of_stream

class input_file_stream(input_stream):
  def __init__(self, filename):
    self.input_file_fd = os.open(filename, os.O_RDONLY)
    super().__init__(self.input_file_fd)
  def __del__(self):
    os.close(self.input_file_fd)

class output_stream:
  '''
  Represent an output stream.
  fd is a file descriptor, for instance returned by sys.open
  '''
  def __init__(self, fd):
    self.fd = fd
  
  def write(self, txt, *args):
    os.write(self.fd, txt.format(*args).encode('utf-8'))
      
  def writeln(self, txt, *args):
    self.write(txt, *args)
    os.write(self.fd, b"\n")


stdin   = input_stream(0)
stdout  = output_stream(1)
stderr  = output_stream(2)

