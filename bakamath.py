from bakaasm import *

def openlib(s):
  # not
  s.pre("macro n#i32(x#expr) (!x)#i32")
  
  # equal
  s.pre(
    "macro eq#i32(x#expr,y#expr) @static",
      "if x==y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro eq#expr(x#expr,y#expr) x==y"
  )
  
  # not equal
  s.pre(
    "macro neq#i32(x#expr,y#expr) @static",
      "if x!=y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro neq#expr(x#expr,y#expr) x!=y"
  )
  
  # less
  s.pre(
    "macro l#i32(x#expr,y#expr) @static",
      "if x<y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro l#expr(x#expr,y#expr) x<y"
  )
  
  # less-or-equal
  s.pre(
    "macro leq#i32(x#expr,y#expr) @static",
      "if x=<y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro leq#expr(x#expr,y#expr) x=<y"
  )
  
  # greater
  s.pre(
    "macro g#i32(x#expr,y#expr) @static",
      "if x>y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro g#expr(x#expr,y#expr) x>y"
  )
  
  # greater-or-equal
  s.pre(
    "macro geq#i32(x#expr,y#expr) @static",
      "if x>=y",
        "return 1",
      "else",
        "return 0",
      "endif",
    "endmacro",
    "macro geq#expr(x#expr,y#expr) x>=y"
  )

ni32xexpr_static = lambda x: not x
ni32xexpr = lambda x: "(!x)"