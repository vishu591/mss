import re

class Validation:

    # to check if the entered password is valid or not
    def isValidPassword(self, passwd):
        return_val = True
        while(True):
            if len(passwd) < 8:
                print('the length of password should be at least 8 char long')
                return_val = False
                break
            if not re.search("[a-z]", passwd):
                print('the password should have at least one numeral')
                return_val = False
                break
            if not re.search("[A-Z]", passwd):
                print('the password should have at least one uppercase letter')
                return_val = False
                break
            if not re.search("[0-9]", passwd):
                print('the password should have at least one lowercase letter')
                return_val = False
                break
            if not re.search("[_@$#]", passwd):
                print('the password should have at least one of the symbols _$@#')
                return_val = False
                break
        return return_val