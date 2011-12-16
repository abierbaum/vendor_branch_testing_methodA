# -*- coding: utf-8 -*-
from webob import Request
import webtest

def input_app(environ, start_response):
    req = Request(environ)
    status = "200 OK"
    body =\
"""
<html>
    <head><title>form page</title></head>
    <body>
        <form method="POST" id="text_input_form">
            <input name="foo" type="text" value="bar">
            <input name="button" type="submit" value="text">
        </form>
        <form method="POST" id="radio_input_form">
            <input name="foo" type="radio" value="bar">
            <input name="foo" type="radio" value="baz" checked>
            <input name="button" type="submit" value="radio">
        </form>
        <form method="POST" id="checkbox_input_form">
            <input name="foo" type="checkbox" value="bar" checked>
            <input name="button" type="submit" value="text">
        </form>
    </body>
</html>
"""
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(body)))]
    start_response(status, headers)
    return [body]

def input_app_without_default(environ, start_response):
    req = Request(environ)
    status = "200 OK"
    body =\
"""
<html>
    <head><title>form page</title></head>
    <body>
        <form method="POST" id="text_input_form">
            <input name="foo" type="text">
            <input name="button" type="submit" value="text">
        </form>
        <form method="POST" id="radio_input_form">
            <input name="foo" type="radio" value="bar">
            <input name="foo" type="radio" value="baz">
            <input name="button" type="submit" value="radio">
        </form>
        <form method="POST" id="checkbox_input_form">
            <input name="foo" type="checkbox" value="bar">
            <input name="button" type="submit" value="text">
        </form>
    </body>
</html>
"""
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(body)))]
    start_response(status, headers)
    return [body]


def input_unicode_app(environ, start_response):
    req = Request(environ)
    status = "200 OK"
    body =\
u"""
<html>
    <head><title>form page</title></head>
    <body>
        <form method="POST" id="text_input_form">
            <input name="foo" type="text" value="Хармс">
            <input name="button" type="submit" value="Сохранить">
        </form>
        <form method="POST" id="radio_input_form">
            <input name="foo" type="radio" value="Хармс">
            <input name="foo" type="radio" value="Блок" checked>
            <input name="button" type="submit" value="Сохранить">
        </form>
        <form method="POST" id="checkbox_input_form">
            <input name="foo" type="checkbox" value="Хармс" checked>
            <input name="button" type="submit" value="Ура">
        </form>
    </body>
</html>
""".encode('utf8')
    headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(body)))]
    start_response(status, headers)
    return [body]


def test_input():
    app = webtest.TestApp(input_app)
    res = app.get('/')
    assert res.status_int == 200
    assert res.headers['content-type'] == 'text/html'
    assert res.content_type == 'text/html'

    form = res.forms['text_input_form']
    assert form['foo'].value == 'bar'
    assert form.submit_fields() == [('foo', 'bar')]

    form = res.forms['radio_input_form']
    assert form['foo'].value == 'baz'
    assert form.submit_fields() == [('foo', 'baz')]

    form = res.forms['checkbox_input_form']
    assert form['foo'].value == 'bar'
    assert form.submit_fields() == [('foo', 'bar')]


def test_input_unicode():
    app = webtest.TestApp(input_unicode_app)
    res = app.get('/')
    assert res.status_int == 200
    assert res.content_type == 'text/html'
    assert res.charset == 'utf-8'

    form = res.forms['text_input_form']
    assert form['foo'].value == u'Хармс'
    assert form.submit_fields() == [('foo', u'Хармс')]

    form = res.forms['radio_input_form']
    assert form['foo'].value == u'Блок'
    assert form.submit_fields() == [('foo', u'Блок')]

    form = res.forms['checkbox_input_form']
    assert form['foo'].value == u'Хармс'
    assert form.submit_fields() == [('foo', u'Хармс')]


def test_input_no_default():
    app = webtest.TestApp(input_app_without_default)
    res = app.get('/')
    assert res.status_int == 200
    assert res.headers['content-type'] == 'text/html'
    assert res.content_type == 'text/html'

    form = res.forms['text_input_form']
    assert form['foo'].value == ''
    assert form.submit_fields() == [('foo', '')]

    form = res.forms['radio_input_form']
    assert form['foo'].value is None
    assert form.submit_fields() == []

    form = res.forms['checkbox_input_form']
    assert form['foo'].value is None
    assert form.submit_fields() == []


