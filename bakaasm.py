import random
import string

from rich import print as print_a
from rich.syntax import Syntax

def rngh(ln=random.randint(16,27)):
  return "".join(random.choices(
    string.ascii_letters + string.ascii_uppercase + string.digits + ("@$#" * 3),
    k=ln
  ))

class BakaASM:pass
class BakaASM:
  def __init__(self, mode="pre", autoimport=False, dottags=False):
    self.mode = mode
    self.autoimport = autoimport
    self.dottags = dottags
    self.header = []
    self.footer = []
    self.instr = []
    self.sections = {
      "data": [],
      "footer": []
    }
    self.transformer = BakaASMTransformer()
    
    self._pre_blocks = ["macro", "if"]
  
  def use(self, what, _from="$"):
    if type(what) == list:
      for _what in what:
        self.header.append(f"~tab:1~_using {_from}:{_what}")
    else:
      self.header.append(f"~tab:1~_using {_from}:{what}")
    return self

  def use_namespace(self, path):
    self.header.append(f"~tab:1~_using :{path}")
    return self

  def let(self, name, value, _type=None):
    if isinstance(value, str | bytes):
      _bit = "u8" if value.isascii() else "u16"
      self.sections["data"].append(f"{name} := db <{_bit}>{value!r}, {len(value)}")
    else:
      if _type is not None:
        self.sections["data"].append(f"{name}#{_type} := {value!r}")
      else:
        self.sections["data"].append(f"{name} := {value!r}")
    return self
    
  def printf(self, tpl, *args, **kwargs):
    try: tpl = tpl.unwrap(tpl) 
    except: pass
    if (_bit := kwargs.get("_bit", None)) is None:
      _bit = "u8" if tpl.isascii() else "u16"
    if self.autoimport:
      self.use("_printf")
    _Xargs = []
    for _arg in args:
      _Xargn = _arg.name if isinstance(_arg,Var) else _arg.expr if isinstance(_arg, Expr) else f"{_arg!r}"
      _Xargbit = "u8" if _Xargn.isascii() else "u16"
      if type(_arg)==str:
        _Xargs.append(f"<{_Xargbit}>{_Xargn}")
      else:
        _Xargs.append(f"{_Xargn}")
    _Xfmtstr=f":fmt!({', '.join(_Xargs)})"
    self.instr.append(f"_printf <{_bit}>{tpl!r}{_Xfmtstr if len(_Xargs)>0 else ''}")
    return self

  def call(self, func):
    self.instr.append(func.unwrap(func))
    return self 

  def pre(self, *instr):
    _Xindent=0
    for _instr in instr:
      if (_Xtok:=_instr.split()[0]) in self._pre_blocks:
        _Xindent+=2
        self.instr.append("%" + " "*(_Xindent-2) + _instr)
      elif _Xtok=="else":
        self.instr.append("%" + " "*(_Xindent-2) + _instr)
      elif _Xtok.startswith("end"):
        _Xindent-=2
        self.instr.append("%" + " "*_Xindent + _instr)
      else: 
        self.instr.append("%" + " "*_Xindent + _instr)
    return self

  def defun(self, name, args=(), body=None):
    rh, rho, rhe = rngh(), rngh(), rngh()
    self.instr.append(f"defun {name}, _{name}${rh}")
    self.instr.append(f"nop!")
    self.instr.append(f":_{name}${rh}")
    if len(args)>0:
      _Xargs=[]
      _Xargsdfv=[]
      for _Xarg in args:
        _X0arg = f"{_Xarg[0]}#{_Xarg[1]}"
        _Xargs.append(f"{_X0arg}")
        _Xargsdfv.append(f"{_Xarg[2] or 'nop!'!r}")
      _Xargsdfv=", ".join(_Xargsdfv)
      _Xargs=", ".join(_Xargs)
      self.instr.append(f"({_Xargs}) = (%*...) ?? ({_Xargsdfv})")
    if body is not None:
      for _instr in body.raw():
        self.instr.append(_instr)
    else:
      self.instr.append("nop!")
    self.instr.append(f"jmp _{name}${rho}")
    self.instr.append(f":_{name}${rho}")
    return self

  def _do(self, *blocks):
    for i, block in enumerate(blocks):
      if len(block[0]) == 6:
        rh, rho, rhe = rngh(), rngh(), rngh()
        for _va,_vv in zip(block[0][0], block[0][1]):
          self.instr.append(f"{_va.name} := {_vv.expr if isinstance(_vv,Expr) else _vv}")
        self.instr.append(f"jmp _{rh}")
        self.instr.append(f":_{rh}")
        if block[0][4] == BakaOp.Cmpx:
          cond = f"{block[0][3]}({block[0][4]})"
        else:
          cond = f"{block[0][3]}({block[0][4]!r}, {block[0][5]!r})"
        self.instr.append(f"jmp:{cond} _{rhe}")
        self.instr.append(f"jmp _{rho}")
        self.instr.append(f":_{rhe}")
        for _instr in block[1].raw():
          self.instr.append(_instr)
        for _va,_vc in zip(block[0][0], block[0][2]):
          _Xvc = _vc.__repr__().split()
          _Xvf = _Xvc[0]
          _Xvv = _Xvc[1]
          self.instr.append(f"{_Xvf} {_va}, {_Xvv}")
        self.instr.append(f"jmp _{rh}")
        self.instr.append(f":_{rho}")
        self.instr.append(f"del {_va}")
      elif len(block[0]) == 2:
        for _va,_vv in zip(block[0][0], block[0][1]):
          rh, rho, rhe, rhi, rhm = rngh(), rngh(), rngh(), rngh(), rngh()
          self.instr.append(f"{rhm} := {_vv}")
          self.instr.append(f"i{rhi}#i8 = 0")
          self.instr.append(f"jmp _{rh}")
          self.instr.append(f":_{rh}")
          cond = f"neq!(_i{rhi}, {rhm}:size())"
          self.instr.append(f"jmp:{cond} _{rhe}")
          self.instr.append(f"jmp _{rho}")
          self.instr.append(f":_{rhe}")
          self.instr.append(f"{_va} := {rhm}[i{rhi}]")
          for _instr in block[1].raw():
            self.instr.append(_instr)
          self.instr.append(f"add! i{rhi}, 1")
          self.instr.append(f"jmp _{rh}")
          self.instr.append(f":_{rho}")
          self.instr.append(f"del {_va}")
    return self

  def _if(self, *blocks):
    for i, block in enumerate(blocks):
      rh, rho = rngh(), rngh()
      if isinstance(block, BakaASM) and len(blocks) > 1 and block == blocks[-1]:
        self.instr.append(f"jmp _{rh}")
        self.instr.append(f":_{rh}")
        for _instr in block.raw():
          self.instr.append(_instr)
        self.instr.append(f"jmp _{rho}")
        self.instr.append(f":_{rho}")
      else:
        if not type(block[0][0]) == tuple:
          if block[0][0] == BakaOp.Cmpx:
            cond = f"{block[0][0]}({block[0][1]})"
          else:
            cond = f"{block[0][0]}({block[0][1]!r}, {block[0][2]!r})"
        else:
          _cond = ""
          for cond in block[0]:
            _condend = ""
            if cond[0] == BakaOp.Cmpx:
              try: _condend = cond[2] + " "
              except: pass
              _cond += f"{cond[0]}({cond[1]}) {_condend}"
            else:
              try: _condend = cond[3]
              except: pass
              _condend = f" {_condend} " if not cond == block[0][-1] else ""
              _cond += f"{cond[0]}({cond[1]}, {cond[2]}){_condend}"
          cond = f"({_cond})"
        self.instr.append(f"jmp:{cond} _{rh}")
        self.instr.append(f"jmp _{rho}")
        self.instr.append(f":_{rh}")
        for _instr in block[1].raw():
          self.instr.append(_instr)
        self.instr.append(f"jmp _{rho}")
        self.instr.append(f":_{rho}")
    return self
  
  def if_(self, *blocks):
    for i, block in enumerate(blocks):
      if isinstance(block, BakaASM) and len(blocks) > 1 and block == blocks[-1]:
        self.instr.append(f"%else")
        for _instr in block.raw():
          self.instr.append(_instr)
      else:
        self.instr.append(f"%{'if' if i < 1 else 'elif'} {block[0][0] % block[0][1:-1]}")
        for _instr in block[1].raw():
          self.instr.append(_instr)
    self.instr.append(f"%endif")
    return self
    
  def define_(self, name, value):
    self.instr.append(f"%define {name} {value!r}")
    return self

  def build(self):
    _instr = []
    _instr.append(".data")
    for instr in self.sections["data"]:
      if instr.startswith("~tab"):
        _sz = instr.split("~tab:")[1].index("~")
        _tab = "\t" * int(instr[5:5+_sz])
        _instr.append(f"{_tab}{instr[6+_sz:]}")
      elif instr.startswith("~space:"):
        _sz = instr.split("~space:")[1].index("~")
        _space = " " * int(instr[7:7+_sz])
        _instr.append(f"{_space}{instr[8+_sz:]}")
      elif not (instr.startswith(":") or instr.startswith(".") or instr.startswith("@")):
        _instr.append(f"\t\t{instr}")
      else:
        _instr.append(instr)
    _instr.append(".text")

    for instr in self.header + self.instr + self.footer:
      if instr.startswith("~tab:"):
        _sz = instr.split("~tab:")[1].index("~")
        _tab = "\t" * int(instr[5:5+_sz])
        _instr.append(f"{_tab}{instr[6+_sz:]}")
      elif instr.startswith("~space:"):
        _sz = instr.split("~space:")[1].index("~")
        _space = " " * int(instr[7:7+_sz])
        _instr.append(f"{_space}{instr[8+_sz:]}")
      elif not (instr.startswith(":") or instr.startswith(".") or instr.startswith("@") or instr.startswith("%")):
        _instr.append(f"\t\t{instr}")
      else:
        _instr.append(instr)
    for instr in self.sections["footer"]:
      if instr.startswith("~tab"):
        _sz = instr.split("~tab:")[1].index("~")
        _tab = "\t" * int(instr[5:5+_sz])
        _instr.append(f"{_tab}{instr[6+_sz:]}")
      elif instr.startswith("~space:"):
        _sz = instr.split("~space:")[1].index("~")
        _space = " " * int(instr[7:7+_sz])
        _instr.append(f"{_space}{instr[8+_sz:]}")
      elif not (instr.startswith(":") or instr.startswith(".") or instr.startswith("@")):
        _instr.append(f"\t\t{instr}")
      else:
        _instr.append(instr)
    return self.transformer.transform(_instr)
  
  def raw(self):
    return self.header + self.instr + self.footer

class BakaASMTransformer:
  @staticmethod
  def transform_operators(instr):
    return (instr
              .replace("<", "l")
              .replace("<=", "le")
              .replace("==", "eq")
              .replace("!=", "neq")
              .replace("<>", "neq")
              .replace(">=", "ge")
              .replace(">", "g")
              .replace("||", "or")
              .replace("|", "or")
              .replace("&&", "and")
              .replace("&", "and"))
   
  def transform(self, source):
    _0 = self.dottags_to_header(source)
    _1 = self.usings_to_header(_0)
    _2 = self.remove_duplicate_dottags(_1)
    _3 = self.remove_duplicate_usings(_2)
    _4 = self.sort_usings(_3)
    _5 = self.sort_dottags(_4)
    _6 = self.pre_to_header(_5)
    
    _last = _6
    _source = "\n".join(_last)
    
    return _source
  
  def pre_to_header(self, source):
    _instr = []
    _pre = []
    
    for instr in source:
      if instr.startswith("%"):
        _pre.append(instr)
      else:
        _instr.append(instr)
    
    return _pre + _instr
  
  def usings_to_header(self, source):
    _instr = []
    _usings = []
    
    for instr in source:
      if "_using" in instr:
        _usings.append(instr)
      else:
        _instr.append(instr)
    
    return _usings + _instr
  
  def remove_duplicate_usings(self, source):
    _instr = []
    _usings = []
    
    for instr in source:
      if "_using" in instr:
        _usings.append(instr)
      else:
        _instr.append(instr)
    
    return list(set(_usings)) + _instr
  
  def remove_duplicate_dottags(self, source):
    _instr = []
    _usings = []
    
    for instr in source:
      if instr.strip().startswith("._"):
        _usings.append(instr)
      else:
        _instr.append(instr)
    
    return list(set(_usings)) + _instr
  
  def sort_usings(self, source):
    _instr = []
    _usings = []
    
    for instr in source:
      if "_using" in instr:
        _usings.append(instr)
      else:
        _instr.append(instr)
    
    return sorted(_usings) + _instr
    
  def dottags_to_header(self, source):
    _instr = []
    _dottags = []
    
    for instr in source:
      if instr.strip().startswith("._"):
        _dottags.append(instr)
      else:
        _instr.append(instr)
    
    return _dottags + _instr
  
  def sort_dottags(self, source):
    _instr = []
    _dottags = []
    
    for instr in source:
      if instr.strip().startswith("._"):
        _dottags.append(instr)
      else:
        _instr.append(instr)
    
    return sorted(_dottags) + _instr

class Var:
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name
  
  @staticmethod
  def unwrap(var):
    return var.__repr__()

class Expr:
  def __init__(self, expr):
    self.expr = expr

  def __repr__(self):
    return self.expr
  
  @staticmethod
  def unwrap(expr):
    return expr.__repr__()

class EExpr:
  def __init__(self, *a):
    self.al=len(a)
    if self.al==2:
      self.arg1=a[1]
      self.op=a[0]
    elif self.al==3:
      self.op=a[0]
      self.arg1=a[1]
      self.arg2=a[2]

  def __repr__(self):
    if self.al==2:
      return f"{self.op} {self.arg1}"
    elif self.al==3:
      return f"({self.op} {self.arg1}, {self.arg2})"
  
  @staticmethod
  def unwrap(eexpr):
    return eexpr.__repr__()

class Func:
  def __init__(self, name, generic=(), args=(), kwargs=()):
    self.name = name
    self.generic = generic
    self.args = args
    self.kwargs = kwargs

  def __repr__(self):
    _Xfunc, _Xgeneric, _Xargs, _Xkwargs = [], [], [], []
    if not (_Cgeneric := self.generic) == ():
      for _0Xgeneric in _Cgeneric:
        _Xgeneric.append(_0Xgeneric.unwrap(_0Xgeneric))
    else:
      _Xgeneric = _Cgeneric
    for _X0arg in self.args:
      _Xargs.append(f"{_X0arg!r}")
    for _X0kwarg in self.kwargs:
      _Xkwargs.append(f"{_X0kwarg[0]}={_X0kwarg[1]}")
    _Xfunc.append(self.name)
    if len(_Xgeneric) > 0:
      _Xfunc.append("<"+", ".join(_Xgeneric)+">")
    else:
      _Xfunc.append("")
    _Xfunc.append(", ".join(_Xargs))
    _Xfunc.append(", ".join(_Xkwargs))
    _Xfunc="{0[0]}{0[1]}({0[2]}{0[3]})".format(_Xfunc)
    return _Xfunc
  
  @staticmethod
  def unwrap(func):
    return func.__repr__()

class Ternary:
  def __init__(self, condition, a, b):
    self.condition = condition
    self.a = a
    self.b = b

  def __repr__(self):
    return f"{self.condition} ? {self.a!r} : {self.b!r}"
    
  @staticmethod
  def unwrap(ternary):
    return ternary.__repr__()

class BakaReg:
  __slots__ = (a := [f"{A}X" for A in "ABCD"]) + [f"E{A}" for A in a] + [f"R{A}" for A in a]

class BakaOp:
  Add = "add!"
  Sub = "sub!"
  Mul = "mul!"
  Div = "div!"
  Fdiv = "fdiv!"
  Exp = "exp!"
  Mod = "mod!"
  Eq = "eq!"
  Leq = "leq!"
  Geq = "geq!"
  Neq = "neq!"
  Cmpx = "complex!"
  And = "and!"
  Or = "or!"
  L = "l!"
  G = "g!"
  N = "n!"

@type.__call__
class Type:
  (_a := [8, 16, 32, 64, 128, 512])
  __slots__ = (_b := [*[f"U{b}" for b in _a],
                      *[f"UI{b}" for b in _a],
                      *[f"I{b}" for b in _a]])
  __dict__ = {_X0:_X0.lower() for _X0 in _b}
  Int = "I8"
  Bytes = "U8"
  def __getattr__(self,a):
    if a in self.__slots__:
      return self.__dict__.get(a).lower()