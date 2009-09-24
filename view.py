from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['./views'], output_encoding='utf-8', input_encoding='utf-8')

def render(template, **kwa):
    mytemplate = mylookup.get_template(template)
    return mytemplate.render(**kwa)
