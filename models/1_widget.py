# ON/OFF Button widget
def BuildRadioButtonWidget(field, value):
    fieldName = str(field).split('.')[1]

    div = DIV(INPUT( _type='checkbox', _name='%s' % fieldName, _checked=value), _class='make-bootstrap-switch', 
              data={'on':"primary", 'off':"default", 'on-label':T('Yes'), 'off-label':T('No') })
    script = SCRIPT("""
        $(".make-bootstrap-switch input[name='%s']").parent().bootstrapSwitch();
    """ % fieldName)
    return DIV(div, script)

