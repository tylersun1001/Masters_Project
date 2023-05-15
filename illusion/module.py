# The parent class for a module in the illusion python model.
# The in_dict dictionary contains the inputs.
# The out_dict dictionary contains the combinational outputs.

class Module():

    def __init__(self):
        self.in_dict = {}
        self.out_dict = {}

    # calculates the output dictionary based on the input dictionary.
    # also runs internal logic within the module
    # should only be called once a clock cycle.
    def calculate_combinational():
        self.out_dict = self.out_dict

