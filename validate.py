import re
def validate_login():
    pass

def validate_signup(details):
    return True
    print(details)
    print(details['email'])
    if ( not re.search(r'^[a-zA-Z ]*$', details['name']) ):
        print("Invalid Name")
        return False
    if ( not re.search(r'[A-Za-z0-9\.\-\\s\,]', details['address']) ):
        print("Invalid address")
        return False
    #if ( not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', details['email']) ):
    #    print(details['email'], "Invalid email", re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', details['email']))
    #    return False
    if ( not re.search(r'^[0-9]{10}$', details['phno']) ):
        print("Invalid email")
        return False
    if ( not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', details['password']) ):
        print("Invalid password")
        return False
    if ( not details['password'] == details['c-password'] ):
        print("Invalid password")
        return False
    return True