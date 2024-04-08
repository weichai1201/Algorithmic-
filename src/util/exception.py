
class Exception:
    """
    Print terminal lines when exception is raised.
    Does NOT terminate the program.

    @author: Huanjie Zhang
    """
    @staticmethod
    def raise_illegal_arguments(msg=""):
        print("Illegal argument exception(s) with message: %s", msg)


    @staticmethod
    def raise_illegal_format(msg=""):
        print("Illegal format exception(s) with message: %s", msg)

