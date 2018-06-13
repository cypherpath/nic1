class Flagger:
    """
    Class Name: Flagger
    Responsibility: Provide a means to make multiple checks without large/nested if statements
    Usage:            Set the desired state (true or false) each call to test records information
                    about the provided value counting total number of true and false states
                    passed to test.
    """

    def __init__(self, pass_state: bool = True) -> None:
        """
        Method Name: __init__
        Purpose: pass_state is the desired state for all tests to equal
        """
        self.__pass_state = pass_state
        self.__run_state = pass_state
        self.__num_true_tests = 0
        self.__num_false_tests = 0
        self.__num_tests = 0

    def all_false(self) -> bool:
        """
        Method Name: all_false
        Purpose: Output whether or not all tests have returned false
        """
        return self.__num_tests != 0 and self.__num_false_tests == self.__num_tests

    def all_true(self) -> bool:
        """
        Method Name: all_true
        Purpose: Output whether or not all tests have returned true
        """
        return self.__num_tests != 0 and self.__num_true_tests == self.__num_tests

    def test(self, new_state: bool) -> None:
        """
        Method Name: test
        Purpose: Update run_state with new_state, track number of tests and outcomes
        """
        self.__num_tests += 1

        if new_state:
            self.__num_true_tests += 1
        else:
            self.__num_false_tests += 1

        # Update run_state
        if self.__run_state == self.__pass_state and self.__run_state != new_state:
            self.__run_state = False
