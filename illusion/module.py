# The parent class for a module in the illusion python model.
# The in_dict dictionary contains the inputs.
# The out_dict dictionary contains the combinational outputs.

class Module():

    def __init__(self):
        self.in_dict = {}
        self.out_dict = {}

    # calculates the output dictionary based on the input dictionary.
    def calculate_combinational(self):
        self.out_dict = self.out_dict

    # updates the internal state of the module.
    # should only be called once a clock cycle.
    def update_state(self):
        pass


