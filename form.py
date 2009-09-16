import formencode

class LoginForm(formencode.Schema):

    allow_extra_fields = True

    username = formencode.validators.String(not_empty=True)
