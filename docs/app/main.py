"""FrankenUI Tasks Example"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../99_main.ipynb.

# %% auto 0
__all__ = ['app', 'rt', 'reference_fns', 'is_htmx', 'with_layout', 'tasks', 'cards', 'dashboard', 'forms', 'music', 'auth',
           'playground', 'mail', 'fnname2title', 'api_route', 'tutorial_spacing', 'themeswitcher', 'llms',
           'getting_started', 'index', 'sidebar']

# %% ../99_main.ipynb
from fasthtml.common import *
import fasthtml.common as fh
from functools import partial
from fh_frankenui.core import *
import re
from fasthtml.components import Uk_theme_switcher
from utils import hjs

# %% ../99_main.ipynb
app,rt = fast_app(pico=False, hdrs=(*Theme.blue.headers(),*hjs))

# %% ../99_main.ipynb
def is_htmx(request=None): return request and 'hx-request' in request.headers

def _create_page(active, original_content, request, open_section):
    if is_htmx(request): return original_content
    else: return with_layout(active, open_section, original_content)

# %% ../99_main.ipynb
def with_layout(active, open_section, original_content):
    return Div(cls="flex flex-col md:flex-row w-full")(
            Button(UkIcon("menu",50,50,cls='mt-4'), cls="md:hidden mb-4", uk_toggle="target: #mobile-sidebar"),
            Div(sidebar(active,open_section), id='mobile-sidebar', hidden=True),
            Div(cls="md:flex w-full")(
                Div(sidebar(active,open_section), cls="hidden md:block w-1/5"),
                Div(original_content, cls='md:w-4/5 w-full mr-5', id="content", )))

# %% ../99_main.ipynb
from tasks import tasks_homepage
from cards import cards_homepage
from dashboard import dashboard_homepage
from forms import forms_homepage
from music import music_homepage
from auth import auth_homepage
from playground import playground_homepage
from mail import mail_homepage

# %% ../99_main.ipynb
_create_example_page = partial(_create_page, open_section='Examples')
@rt
def tasks(request=None):      return _create_example_page('task',      tasks_homepage,     request)
@rt
def cards(request=None):      return _create_example_page('card',      cards_homepage,     request)
@rt
def dashboard(request=None):  return _create_example_page('dashboard', dashboard_homepage, request)
@rt
def forms(request=None):      return _create_example_page('form',      forms_homepage,     request)
@rt 
def music(request=None):      return _create_example_page('music',     music_homepage,     request)
@rt
def auth(request=None):       return _create_example_page('auth',      auth_homepage,      request)
@rt
def playground(request=None): return _create_example_page('playground',playground_homepage,request)
@rt
def mail(request=None):       return _create_example_page('mail',      mail_homepage,      request) 

# %% ../99_main.ipynb
import api_reference

# %% ../99_main.ipynb
def fnname2title(ref_fn_name): return ref_fn_name[5:].replace('_',' | ').title() 

# %% ../99_main.ipynb
reference_fns = L([o for o in dir(api_reference) if o.startswith('docs_')])

@rt('/api_ref/{o}')
def api_route(request, o:str):
    if o not in reference_fns: raise HTTPException(404)
    content = getattr(api_reference, o)()
    title = fnname2title(o)
    return _create_page('api_reference', 
                        DivContainer(content), 
                        request=request, 
                        open_section='API Reference')

# %% ../99_main.ipynb
from tutorial_spacing import spacing_tutorial

# %% ../99_main.ipynb
_create_example_page = partial(_create_page, open_section='Tutorials')
@rt
def tutorial_spacing(request=None): return _create_example_page('spacing',      spacing_tutorial,     request)

# %% ../99_main.ipynb
@rt
def themeswitcher(request): 
    return _create_page('theme', Div(Uk_theme_switcher(),cls="p-12"), request, None)

# %% ../99_main.ipynb
@rt
def llms(request=None):
    return _create_page('llms', DivContainer(render_md(open('LLM Contexts.md').read())), request, 'LLMs')

# %% ../99_main.ipynb
@rt
def getting_started(request=None):
    content = DivContainer(render_md(open('GettingStarted.md').read()))
    return _create_page('getting_started', content, request, None)

# %% ../99_main.ipynb
@rt
def index():return getting_started()

# %% ../99_main.ipynb
def sidebar(active,open_section):
    def create_li(title, href):
        is_active = title.lower() == active.lower()
        return Li(A(title, cls="uk-active" if is_active else "",
                    hx_target="#content", hx_get=href, hx_trigger='mousedown', hx_push_url='true'))

    return NavContainer(
        create_li("Getting Started", getting_started),
        create_li("LLMs", llms),
        NavParentLi(
            A(DivFullySpaced("API Reference", NavBarParentIcon())),
            NavContainer(
                *[create_li(fnname2title(o), f"/api_ref/{o}") for o in reference_fns],
                parent=False,  
            ),
            cls='uk-open' if open_section=='API Reference' else ''
        ),
        NavParentLi(
            A(DivFullySpaced('Guides', NavBarParentIcon())),
            NavContainer(
                *[create_li(title, href) for title, href in [
                    ('Spacing', tutorial_spacing),
                ]],
                parent=False
            ),
            cls='uk-open' if open_section=='Guides' else ''
        ),
        
        NavParentLi(
            A(DivFullySpaced('Examples', NavBarParentIcon())),
            NavContainer(
                *[create_li(title, href) for title, href in [
                    ('Task', tasks),
                    ('Card', cards),
                    ('Dashboard', dashboard),
                    ('Form', forms),
                    ('Music', music),
                    ('Auth', auth),
                    ('Playground', playground),
                    ('Mail', mail),
                ]],
                parent=False
            ),
            cls='uk-open' if open_section=='Examples' else ''
        ),
        create_li("Theme", themeswitcher),
        uk_nav=True,
        cls=(NavT.primary, "space-y-4 p-4 w-full md:w-full")
    )

# %% ../99_main.ipynb
serve()
