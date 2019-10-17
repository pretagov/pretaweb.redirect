Introduction
============
Redirector, a folder-like Zope product that redirects the HTTP client
to a different URL.


How to use
==========

In the ZMI create a redirector object

Object looks at the subpath and host header and does 301 redirects based on it's rules.

This is designed to be used in conjunction with virtual host monster (VHM). Setup VHM to point a domain to your global redir object in your zope root as would a Plone site. Then add redirector rules to determine where to redirect the user. For example, all urls in an old domain name, to the same subpath on a new domain.

Rules are of the form::

  DOMAIN_REGEX/PATH_REGEX NEW_URL


