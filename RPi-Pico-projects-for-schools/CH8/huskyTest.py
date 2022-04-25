from huskylensPythonLibrary import HuskyLensLibrary

husky = HuskyLensLibrary("I2C") #Create the HuskyLens object as I2C 

print(husky.command_request_knock())