
from .redirect import Redirector, manage_addRedirectorForm, manage_addRedirector


__roles__ = None
__allow_access_to_unprotected_subobjects__ = 1


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    context.registerClass(
        Redirector,
        permission='Add pretaweb.redirector',
        constructors=(manage_addRedirectorForm,
                      manage_addRedirector),
        icon='RedirectorIcon.gif'
        )

#    context.registerHelp()
#    context.registerHelpTitle('Script (Python)')
#    global _m
#    _m['recompile'] = recompile
#    _m['recompile__roles__'] = ('Manager',)
