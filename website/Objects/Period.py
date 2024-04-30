class Period:
    def __init__(self, subject, start_time, end_time, type, code, lstext=None, subst_text=None) -> None:
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time
        self.type = type
        self.code = code
        self.lstext = lstext
        self.subst_text = subst_text