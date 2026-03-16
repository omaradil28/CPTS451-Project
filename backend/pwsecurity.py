import bcrypt as bc


def HashPassword(plainPassword):
    """
    Function: HashPassword()
    Description: Hashes the password.
    Arguments:
        - plainPassword : String of arbitrary length that respresents a user's password
    Returns: Hashed password string using bcrypt algorithm
    """

    salt = bc.gensalt()
    plainPasswordBytes = plainPassword.encode('utf-8')
    hashedPassword = bc.hashpw(plainPasswordBytes, salt)

    return hashedPassword

def CheckHash(plainPassword, hashPassword):
    """
    Function: CheckHash()
    Description: Hashes plainPassword and then checks it against hashPassword.
    Arguments:
        - plainPassword : String of arbitrary length to hash and check
        - hashPassword : Hashed password to compare to
    Returns: True if the plainPassword matches hashPassword once hashed, False otherwise
    """

    plainPasswordBytes = plainPassword.encode('utf-8')
    return bc.checkpw(plainPasswordBytes, hashPassword)