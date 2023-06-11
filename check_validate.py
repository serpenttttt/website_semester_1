def validate_login(login):
    if 6 <= len(login) <= 30:

        if login[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            for i in login:
                if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_':
                    return False
            return True
    else:
        return False


def validate_password(password):
    upper = False
    lower = False
    digits = False
    symbols = False
    if 8 <= len(password) <= 30:
        for i in password:
            if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                upper = True
            if i in 'abcdefghijklmnopqrstuvwxyz':
                lower = True
            if i in '0123456789':
                digits = True
            if i in '_-+*.!%$#@&*^|\/~[]{}':
                symbols = True
        if upper and lower and digits and symbols:
            return True
        else:
            return False
    else:
        return False