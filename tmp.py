from jinja2 import Template

template = Template('Hello {{name}}!')
name = 'flask'

print(template.render(name=name))