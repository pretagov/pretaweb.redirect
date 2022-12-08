"""Redirector, a folder-like Zope product that redirects the HTTP client
to a different URL.

Copyright (c) 1999-2001 by Dylan Jay <software@pretaweb.com>

See README.txt for more information.
"""

__version__ = "1.2.1"

from App.special_dtml import HTMLFile, DTMLFile
from AccessControl.rolemanager import RoleManager
import re
from six.moves.urllib.parse import urlparse
from AccessControl.SecurityInfo import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.ObjectManager import ObjectManager


"""
Object looks at the subpath and host header and does 301 redirects based on it's rules.
Rules are of the form

  DOMAIN_REGEX/PATH_REGEX NEW_URL

"""

manage_addRedirectorForm = HTMLFile('templates/redirectorAdd', globals())

def manage_addRedirector(self, id, REQUEST=None):
    '''Add a Redirector into the system'''

    Obj = Redirector()
    Obj.id = id
    Obj.title = id
    self._setObject(id, Obj)
    if REQUEST:
        return self.manage_main(self, REQUEST)


class Redirector(ObjectManager):
    '''Redirector base class'''

    meta_type = 'Redirector'
    icon = 'misc_/Redirector/icon'

    manage_options = (
            {'icon': '', 'label': 'Edit', 'action': 'manage_main',
             'target': 'manage_main'},
            {'icon': '', 'label': 'Security', 'action': 'manage_access',
             'target': 'manage_main'},
        )+ObjectManager.manage_options

    security = ClassSecurityInfo()

    security.declareObjectProtected('View')
    security.declareProtected('View', '__call__', 'index_html')

    Redirector_editForm = DTMLFile('templates/redirectorEdit', globals())
    manage = manage_main = Redirector_editForm
    Redirector_editForm._setName('Redirector_editForm')


    security.declareProtected('View management screens',
                              'manage_main', 'Redirector_editForm')

    errors = warnings = ()

    def __init__(self):
        '''Initialize'''

        self.rules_raw = ""
        self.rules = [] # [(compiled_regex,replacement)]

    def manage_makeChanges(self, rules_raw, REQUEST=None):
        '''Perform changes'''
        request = REQUEST

        self.rules_raw = request.rules_raw
        self.rules = []
        self.errors = []
        tests = []
        i = 0
        for line in self.rules_raw.split('\n'):
            i+=1
            line = line.strip()
            if not line or line[0]=='#':
                continue
            if line[0] == '=':
                line = line[1:].strip()
                parts = re.split(r"(?<!\\)\s+",line) #split on non escaped whitespace
                if len(parts) == 2:
                    tests.append( parts )

            parts = re.split(r"(?<!\\)\s+",line) #split on non escaped whitespace
            if len(parts) == 2:
                match, url = parts
                try:
                    self.rules.append((re.compile(match), url))
                except Exception as detail:
                    self.errors.append('%d: %s "%s"'%(i,str(detail),line))
            else:
                self.errors.append("Line should be DOMAIN_REGEX/PATH_REGEX NEW_URL: %s"%line)
        for oldurl,newurl in tests:
            scheme, netloc, path, params, query, fragment = urlparse.urlparse(oldurl)
            res = self.redirect(netloc,path,query)
            if res != newurl:
                self.errors.append("TEST: %s %s != %s"%(oldurl,res,newurl))

        message = "Saved changes."
        return self.Redirector_editForm(self, REQUEST,
                                               manage_tabs_message=message)



    def __before_publishing_traverse__(self, self2, request):
        path = request['TraversalRequestNameStack']
        if path and hasattr(self.aq_base, path[-1]):
             return
        # get rid of virtual_hosting out of traverse path
        if '/' in path:
            subpath = path[:path.index('/')]
        else:
            subpath = path[:]
        path[:] = []
        subpath.reverse()
        request.set('traverse_subpath', subpath)

    def redirect(self, domain, path, query_string=None):
        if path:
            oldurl = "%s/%s" % (domain, path.lstrip('/'))
        else:
            oldurl = domain

        for rule, url in self.rules:
            m = rule.match(oldurl)
            if m:
                url = m.expand(url)
                if query_string:
                    url+= "?" + query_string
                return url

    def index_html(self):
        """ do redirect
        """
        request = self.REQUEST
        domain = request['HTTP_HOST']
        path = '/'.join(request['traverse_subpath'])
        url = self.redirect(domain, path, request['QUERY_STRING'])
        if url:
            request.response.redirect(url, status="301")
        else:
            request.response.setStatus(404, "Not Found")






            #  def __bobo_traverse__(self, REQUEST, Name = ''):
            #    if Name[:6] != 'manage':
            #      class Traversal(ExtensionClass.Base):
            #        def __init__(self, base, path, mappings, target, hardMap):
            #          self.base = base
            #          self.path = path
            #          self.mappings = mappings
            #          self.target = target
            #          self.hardMap = hardMap
            #
            #        def __bobo_traverse__(self, REQUEST, Name = ''):
            #          self.path = self.path + '/' + Name
            #          return self.__class__(self.base, self.path, self.mappings,
            #            self.target, self.hardMap)
            #
            #        def __call__(self, REQUEST):
            #          path = self.path
            #          if REQUEST['QUERY_STRING']:
            #            path = path + "?" + REQUEST['QUERY_STRING']
            #          for k in self.mappings.keys():
            #            if re.match(k, path):
            #              path = re.sub(k, self.mappings[k], path)
            #              break
            #          else:
            #            if self.hardMap:
            #              path = self.target
            #          path = urlparse.urljoin(self.base, path)
            #          raise 'Redirect', path
            #
            #      return Traversal(REQUEST.URL2 + "/", Name, self.Mappings, self.Target,
            #        self.HardMap)
            #
            #    if hasattr(self, 'aq_base'):
            #      b = self.aq_base
            #      if hasattr(b, Name):
            #        return getattr(self, Name)
            #    try:
            #      return self[Name]
            #    except:
            #      return getattr(self, Name)


