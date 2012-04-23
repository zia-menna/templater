#!/usr/bin/env python
# coding: utf-8

from os import unlink
from templater import Templater


def test_new_learn_text_trying_to_delete_some_variable():
    template = Templater()
    template.learn('<b> a and b </b>')
    template.learn('<b> c and d </b>')
    template.learn('<b> e and  </b>')
    result = template._template
    expected = [None, '<b> ', None, ' and ', None, ' </b>', None]
    assert result == expected
    #TODO: should never have less variables when learning?

def test_parse():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    result = template.parse('a b c d')
    expected = ['', 'b c', '']
    assert result == expected

def test_Templater_parse_file_should_open_and_parse_a_file_from_filename():
    template = Templater('+<u>+</u>+', marker='+')
    fp = open('test.html', 'w')
    fp.write('testing <u> parsing </u> files\n')
    fp.close()
    result_1 = template.parse_file('test.html')
    expected = ['testing ', ' parsing ', ' files']
    unlink('test.html')
    assert expected == result_1

    fp = open('test.html', 'w')
    fp.write('testing <u> parsing </u> files\r\n')
    fp.close()
    result_2 = template.parse_file('test.html')
    unlink('test.html')
    assert expected == result_2

def test_join():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    parsed = template.parse('a b c d')
    result = template.join(parsed)
    expected = 'a b c d'
    assert result == expected

def test_join_with_less_parameters_than_variables_should_raise_ValueError():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    try:
        result = template.join([''])
    except ValueError:
        pass
    else:
        assert 'ValueError not raised!' == False

def test_Templater_should_import_pre_processed_template_if_user_want():
    pre_processed = [None, '<u>', None, '</u>', None]
    template = Templater(template=pre_processed)
    assert template._template == pre_processed
    assert template.join(['', 'python', '']) == '<u>python</u>'

def test_Templater_should_import_template_string_with_marks():
    template = Templater(template='<b>|||</b>', marker='|||')
    result_template = template._template
    assert result_template == [None, '<b>', None, '</b>', None]
    assert template.join(['', 'spam eggs', '']) == '<b>spam eggs</b>'

def test_Templater_dump_and_load_should_pickle_and_unpickle():
    processed_template = [None, '<b>', None, '</b><u>', None, '</u>', None]
    template = Templater(template=processed_template, tolerance=5)
    template.dump('my-template.tpl')
    t2 = Templater.load('my-template.tpl')
    unlink('my-template.tpl')
    result_1 = t2._template
    expected_1 = processed_template
    result_2 = t2._tolerance
    expected_2 = 5
    assert expected_1 == result_1
    assert expected_2 == result_2

def test_Templater_should_be_able_to_adjust_tolerance():
    t = Templater(tolerance=1)
    t.learn('git and pyth')
    t.learn('eggs and spam')
    expected = [None, ' and ', None]
    result = t._template
    assert expected == result

def test_Templater_save_should_save_template_as_a_raw_file_with_markers():
    processed_template = [None, '<b>', None, '</b><u>', None, '</u>', None]
    t = Templater(template=processed_template)
    t.save('test.html', marker='|||')
    fp = open('test.html')
    result = fp.read()
    fp.close()
    unlink('test.html')
    expected = '|||<b>|||</b><u>|||</u>|||\n'
    assert expected == result

def test_Templater_open_should_create_a_template_from_a_raw_file_with_markers():
    fp = open('test.html', 'w')
    fp.write('|||<b>|||</b><u>|||</u>|||')
    fp.close()
    t = Templater.open('test.html', marker='|||')
    unlink('test.html')
    result = t._template
    expected = [None, '<b>', None, '</b><u>', None, '</u>', None]
    assert expected == result

def test_Templater_open_should_remove_leading_linefeed_if_there_is_some():
    fp = open('test.html', 'w')
    fp.write('|||<b>|||</b><u>|||</u>|||\n')
    fp.close()
    t = Templater.open('test.html', marker='|||')
    unlink('test.html')
    result_1 = t._template
    expected = [None, '<b>', None, '</b><u>', None, '</u>', None]
    assert expected == result_1

    fp = open('test.html', 'w')
    fp.write('|||<b>|||</b><u>|||</u>|||\r\n')
    fp.close()
    t = Templater.open('test.html', marker='|||')
    unlink('test.html')
    result_2 = t._template
    assert expected == result_2
