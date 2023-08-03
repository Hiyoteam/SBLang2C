class SBExp:
    def __init__(self,exp) -> None:
        self.exp=exp
        if not exp.startswith("sbexp::"):
            raise NameError("Invaild SBExp")
    