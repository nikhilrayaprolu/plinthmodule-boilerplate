from .forms import TtrssForm
from plinth.modules import ttrss
from django.contrib import messages
from plinth import actions
from plinth import package
@package.required(['module_name'])
def index(request):
    """Serve configuration page."""
    status = get_status()

    form = None

    if request.method == 'POST':
        form = module_nameForm(request.POST, prefix='ttrss')
        if form.is_valid():
            _apply_changes(request, status, form.cleaned_data)
            status = get_status()
            form = module_nameForm(initial=status, prefix='ttrss')
    else:
        form = module_nameForm(initial=status, prefix='ttrss')

    return TemplateResponse(request, 'module_name.html',
                            {'title': 'module_shortname',
                             'status': status,
                             'form': form})
def get_status():
    """Get the current status."""
    return {'enabled': module_name.is_enabled()}

def _apply_changes(request, old_status, new_status):
    """Apply the changes."""
    modified = False

    if old_status['enabled'] != new_status['enabled']:
        sub_command = 'enable' if new_status['enabled'] else 'disable'
        actions.superuser_run('ttrss', [sub_command])
        modified = True

    if modified:
        messages.success(request, 'Configuration updated')
    else:
        messages.info(request, 'Setting unchanged')