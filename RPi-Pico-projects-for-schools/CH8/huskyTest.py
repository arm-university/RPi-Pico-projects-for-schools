from huskylensPythonLibrary import HuskyLensLibrary

husky = HuskyLensLibrary("I2C")  # Use the same I2C setup
print(husky.command_request_knock())  # Should return "Knock knock"