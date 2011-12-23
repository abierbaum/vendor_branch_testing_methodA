

def doSomething(value, other = None):
  print "Did something with: ", value
  if other is not None:
     commonMethod(other)
  

def doSomething2(value):
  print "Did something2: ", value


def commonMethod(value):
  print "common support: ", value

def refactor2Method(value):
  print "value: ", value
