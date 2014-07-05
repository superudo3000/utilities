#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Instruct an AVM FRITZ!Box via UPnP_ to reconnect.

This is usually realized with tools like Netcat_ or cURL_.  However, when
developing in Python_ anyway, it is more convenient to integrate a native
implementation.  This one requires Python_ 2.5 or higher.

UPnP_ (Universal Plug and Play) control messages are based on SOAP_, which is
itself based on XML_, and transmitted over HTTP_.

Make sure UPnP_ is enabled on the FRITZ!Box.

A reconnect only takes a few second while restarting the box takes about up to
a minute; not counting the time needed to navigate through the web interface.

.. _Netcat: http://netcat.sourceforge.net/
.. _cURL:   http://curl.haxx.se/
.. _Python: http://www.python.org/
.. _UPnP:   http://www.upnp.org/
.. _SOAP:   http://www.w3.org/TR/soap/
.. _XML:    http://www.w3.org/XML/
.. _HTTP:   http://tools.ietf.org/html/rfc2616

:Copyright: 2008-2014 Jochen Kupperschmidt
:Date: 05-Jul-2014 (original release: 04-Apr-2008)
:License: MIT
"""

from __future__ import print_function
from contextlib import closing
import socket


def reconnect(host='fritz.box', port=49000, debug=False):
    """Connect to the box and submit SOAP data via HTTP."""
    request_data = create_http_request(host, port)

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((host, port))
        s.send(request_data)
        if debug:
            data = s.recv(1024)
            print('Received:', data)


def create_http_request(host, port):
    body = create_http_body()

    return '\r\n'.join([
        'POST /upnp/control/WANIPConn1 HTTP/1.1',
        'Host: {0}:{1:d}'.format(host, port),
        'SoapAction: urn:schemas-upnp-org:service:WANIPConnection:1#ForceTermination',
        'Content-Type: text/xml; charset="utf-8"',
        'Content-Length: {0:d}'.format(len(body)),
        '',
        body,
    ])


def create_http_body():
    return '\r\n'.join([
        '<?xml version="1.0" encoding="utf-8"?>',
        '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">',
        '  <s:Body>',
        '    <u:ForceTermination xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1"/>',
        '  </s:Body>',
        '</s:Envelope>',
    ])


if __name__ == '__main__':
    reconnect()
