
import redirect


__roles__ = None
__allow_access_to_unprotected_subobjects__ = 1


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    context.registerClass(
        redirect.Redirector,
        permission='Add pretaweb.redirector',
        constructors=(redirect.manage_addRedirectorForm,
                      redirect.manage_addRedirector),
        icon='RedirectorIcon.gif'
        )

#    context.registerHelp()
#    context.registerHelpTitle('Script (Python)')
#    global _m
#    _m['recompile'] = recompile
#    _m['recompile__roles__'] = ('Manager',)
