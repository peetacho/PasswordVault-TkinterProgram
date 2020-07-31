class Entries():

    def __init__(self, account, username, email, password, description):
        self.account = account
        self.username = username
        self.email = email
        self.password = password
        self.description = description

    def __str__(self):
        return self.account


#"{}\n{}\n{}\n{}\n{}\n".format(self.account, self.username, self.email, self.password, self.description)
