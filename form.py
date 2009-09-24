import formencode

class LoginForm(formencode.Schema):

    allow_extra_fields = True
    username = formencode.validators.String(not_empty=True)

class DashboardForm(formencode.Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    search = formencode.validators.String(not_empty=True)
