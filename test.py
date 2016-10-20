def fix_none(field):
    if field == None:
        return ''
    return field

print(fix_none('abc'))
print(fix_none(None) + 'def')
