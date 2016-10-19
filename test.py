def fix_none(field):
    if field == None:
        return ''
    return field

print(fix_none('abc'))
print(fix_none(None) + 'def')

/Users/wahhab/Sites/rts/env/lib/python3.5/site-packages/django/db/models/fields/__init__.py:1430:
RuntimeWarning: DateTimeField Issue.added_date received a naive datetime (2016-10-17 18:33:25.369050) while time zone support is active.
  RuntimeWarning)
