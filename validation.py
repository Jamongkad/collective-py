import web
import formencode
from formencode import htmlfill

from view import render

def validate(schema, html=None):
    def class_meth(meth):
        def new(self, *args, **kwa):   
            try:
                schema.to_python(dict(web.input()))
            except formencode.Invalid, error:
                return htmlfill.render(
                    render(html),
                    defaults=error.value,
                    errors=error.error_dict
                )
            else:
                return meth(self, *args, **kwa)
        return new
    return class_meth

