class TestResult:
    def __init__(self, success, hint=None):
        self.success = success
        self.hint_ = hint

    def __bool__(self):
        return self.success

    def hint(self):
        return self.hint_ if not self.success else ""


class Test:
    def __init__(self):
        self.tests = {}

    def add_test(self, function):
        self.tests[function.__name__] = function

    def run(self):
        print(f"Running {len(self.tests)} tests")
        for idx, element in enumerate(self.tests):
            result = self.tests[element].__call__()
            hint = result.hint()

            print(f"test {element} ...", ("FAILED" if not result else "ok") + (f": {hint}" if hint else ""))