#
# fysom.py - pYthOn Finite State Machine - this is a port of Jake
#                        Gordon's javascript-state-machine to python
#                        https://github.com/jakesgordon/javascript-state-machine
#
# Copyright (C) 2011 Mansour Behabadi <mansour@oxplot.com>, Jake Gordon
#                                        and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import unittest

from fysom import Fysom, FysomError


class FysomStateTests(unittest.TestCase):

    def setUp(self):
        self.fsm = Fysom({
            'initial': 'green',
            'events': [
                {'name': 'warn',  'src': 'green',  'dst': 'yellow'},
                {'name': 'panic', 'src': 'yellow', 'dst': 'red'},
                {'name': 'calm',  'src': 'red',    'dst': 'yellow'},
                {'name': 'clear', 'src': 'yellow', 'dst': 'green'}
            ]
        })

    def test_is_state_should_succeed_for_initial_state(self):
        self.assertTrue(self.fsm.isstate('green'))

    def test_identity_transition_should_not_be_allowed_by_default(self):
        self.assertFalse(self.fsm.can('clear'))
        self.assertTrue(self.fsm.cannot('clear'))

    def test_configured_transition_should_work(self):
        self.assertTrue(self.fsm.can('warn'))

    def test_transition_should_change_state(self):
        self.fsm.warn()
        self.assertTrue(self.fsm.isstate('yellow'))

    def test_should_raise_exception_when_state_transition_is_not_allowed(self):
        self.assertRaises(FysomError, self.fsm.panic)
        self.assertRaises(FysomError, self.fsm.calm)
        self.assertRaises(FysomError, self.fsm.clear)


class FysomManyToManyTransitionTests(unittest.TestCase):

    def test_rest_should_always_transition_to_hungry_state(self):
        fsm = Fysom({
            'initial': 'hungry',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.rest()
        self.assertEquals(fsm.current, 'hungry')

        fsm = Fysom({
            'initial': 'satisfied',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.rest()
        self.assertEquals(fsm.current, 'hungry')

        fsm = Fysom({
            'initial': 'full',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.rest()
        self.assertEquals(fsm.current, 'hungry')

        fsm = Fysom({
            'initial': 'sick',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.rest()
        self.assertEquals(fsm.current, 'hungry')

    def test_eat_should_transition_to_satisfied_when_hungry(self):
        fsm = Fysom({
            'initial': 'hungry',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.eat()
        self.assertEqual(fsm.current, 'satisfied')

    def test_eat_should_transition_to_full_when_satisfied(self):
        fsm = Fysom({
            'initial': 'satisfied',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.eat()
        self.assertEqual(fsm.current, 'full')


    def test_eat_should_transition_to_sick_when_full(self):
        fsm = Fysom({
            'initial': 'full',
            'events': [
                {'name': 'eat',  'src': 'hungry',    'dst': 'satisfied'},
                {'name': 'eat',  'src': 'satisfied', 'dst': 'full'},
                {'name': 'eat',  'src': 'full',      'dst': 'sick'},
                {'name': 'rest', 'src': ['hungry', 'satisfied', 'full', 'sick'],
                 'dst': 'hungry'}
            ]
        })
        fsm.eat()
        self.assertEqual(fsm.current, 'sick')


class FysomInitializationTests(unittest.TestCase):

    def test_should_have_no_state_when_no_initial_state_is_given(self):
        fsm = Fysom({
            'events': [
                {'name': 'warn',  'src': 'green',  'dst': 'yellow'},
                {'name': 'panic', 'src': 'yellow', 'dst': 'red'},
                {'name': 'calm',  'src': 'red',    'dst': 'yellow'},
                {'name': 'clear', 'src': 'yellow', 'dst': 'green'}
            ]
        })
        self.assertEqual(fsm.current, 'none')

    def test_initial_state_should_be_green_when_configured(self):
        fsm = Fysom({
            'initial': 'green',
            'events': [
                {'name': 'warn',  'src': 'green',  'dst': 'yellow'},
                {'name': 'panic', 'src': 'yellow', 'dst': 'red'},
                {'name': 'calm',  'src': 'red',    'dst': 'yellow'},
                {'name': 'clear', 'src': 'yellow', 'dst': 'green'}
            ]
        })
        self.assertEqual(fsm.current, 'green')

    def test_initial_state_should_work_with_different_event_name(self):
        fsm = Fysom({
            'initial': {'state': 'green', 'event': 'init'},
            'events': [
                {'name': 'panic', 'src': 'green', 'dst': 'red'},
                {'name': 'calm',  'src': 'red',   'dst': 'green'},
                ]
        })
        self.assertEquals(fsm.current, 'green')

    def test_deferred_initial_state_should_be_none_then_state(self):
        fsm = Fysom({
            'initial': {'state': 'green', 'event': 'init', 'defer': True},
            'events': [
                {'name': 'panic', 'src': 'green', 'dst': 'red'},
                {'name': 'calm',  'src': 'red',   'dst': 'green'},
                ]
        })
        self.assertEqual(fsm.current, 'none')
        fsm.init()
        self.assertEqual(fsm.current, 'green')


class FysomCallbackTests(unittest.TestCase):

    def before_foo(self, e):
        self.before_foo_event = e
        self.fired_callbacks.append('before_foo')

    def before_bar(self, e):
        self.before_bar_event = e
        self.fired_callbacks.append('before_bar')

    def on_foo(self, e):
        self.foo_event = e
        self.fired_callbacks.append('after_foo')

    def on_bar(self, e):
        self.bar_event = e
        self.fired_callbacks.append('after_bar')

    def on_baz(self, e):
        raise ValueError('Baz-inga!')

    def on_enter_fooed(self, e):
        self.enter_fooed_event = e

    def on_enter_bared(self, e):
        self.enter_bared_event = e

    def setUp(self):
        self.fired_callbacks = []

        self.fsm = Fysom({
            'initial': 'sleeping',
            'events': [
                {'name': 'foo',  'src': 'sleeping',  'dst': 'fooed'},
                {'name': 'bar', 'src': 'fooed', 'dst': 'bared'},
                {'name': 'baz', 'src': 'bared', 'dst': 'bazed'},
            ],
            'callbacks': {
                'onfoo': self.on_foo,
                'onbar': self.on_bar,
                'onbaz': self.on_baz,
                'onbeforefoo': self.before_foo,
                'onbeforebar': self.before_bar,
                'onenterfooed': self.on_enter_fooed,
                'onenterbared': self.on_enter_bared
            }
        })

    def test_onafter_event_callbacks_should_fire_with_keyword_arguments_when_events_occur(self):
        self.fsm.foo(attribute='test')
        self.assertTrue(hasattr(self, 'foo_event'), 'Callback on_foo did not fire.')
        self.assertTrue(self.foo_event is not None)
        self.assertEqual(self.foo_event.attribute, 'test')

        self.fsm.bar(id=123)
        self.assertTrue(hasattr(self, 'bar_event'), 'Callback on_bar did not fire.')
        self.assertTrue(self.bar_event is not None)
        self.assertEqual(self.bar_event.id, 123)

    def test_onafter_event_callbacks_raising_exceptions_should_not_be_eaten(self):
        self.fsm.foo()
        self.fsm.bar()
        self.assertRaises(ValueError, self.fsm.baz)

    def test_onbefore_event_callbacks_should_fire_before_onafter_callbacks_with_keyword_arguments_when_events_occur(self):
        self.fsm.foo(attribute='test')
        self.assertTrue(hasattr(self, 'before_foo_event'), 'Callback onbeforefoo did not fire.')
        self.assertTrue(self.before_foo_event is not None)
        self.assertEqual(self.before_foo_event.attribute, 'test')
        self.fsm.bar(id=123)
        self.assertTrue(hasattr(self, 'before_bar_event'), 'Callback onbeforebar did not fire.')
        self.assertTrue(self.before_bar_event is not None)
        self.assertEqual(self.before_bar_event.id, 123)
        self.assertEqual(['before_foo', 'after_foo', 'before_bar', 'after_bar'], self.fired_callbacks)

    def test_onenter_state_callbacks_should_fire_with_keyword_arguments_when_state_transitions_occur(self):
        self.fsm.foo(attribute='test')
        self.assertTrue(hasattr(self, 'enter_fooed_event'), 'Callback onenterfooed did not fire.')
        self.assertTrue(self.enter_fooed_event is not None)
        self.assertEqual(self.enter_fooed_event.attribute, 'test')

        self.fsm.bar(id=123)
        self.assertTrue(hasattr(self, 'enter_bared_event'), 'Callback onenterbared did not fire.')
        self.assertTrue(self.enter_bared_event is not None)
        self.assertEqual(self.enter_bared_event.id, 123)