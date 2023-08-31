
import os
import sys
import adsk.core
import traceback
import math

app_path = os.path.dirname(__file__)

sys.path.insert(0, app_path)
sys.path.insert(0, os.path.join(app_path, 'apper'))

try:
    import config
    import apper

    from .commands.HingeCommand import HingeCommand
    from .commands.SlideCommand import SlideCommand
    from .commands.RotateCommand import RotateCommand
    from .commands.SpringCommand import SpringCommand   
    from .commands.PlanarCommand import PlanarCommand
    from .commands.CylindricalCommand import CylindricalCommand
    from .commands.FabricateCommand import FabricateCommand
# Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)

    # Creates a basic Hello World message box on execute
    my_addin.add_command(
        'Hinge',
        HingeCommand,
        {
            'cmd_description': 'Create a hinge mechanism',
            'cmd_id': 'hingeCommand',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Hinge mechanism',
            'cmd_resources': 'command_icons_hinge',
            'command_visible': True,
            'command_promoted': True,
        }
    )
    my_addin.add_command(
        'Slide',
        SlideCommand,
        {
            'cmd_description': 'Create a slide mechanism',
            'cmd_id': 'slideCommand',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Slide mechanism',
            'cmd_resources': 'command_icons_slide',
            'command_visible': True,
            'command_promoted': True,
        }
    )
        
# General command showing inputs and user interaction
    my_addin.add_command(
    'Rotate',
    RotateCommand,
        {
        'cmd_description': 'Create a rotating mechanism',
        'cmd_id': 'rotateCommand',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Rotate mechanism',
        'cmd_resources': 'command_icons_rotate',
        'command_visible': True,
        'command_promoted': True,
        }
    )
    my_addin.add_command(
    'Planar',
    SpringCommand,
        {
        'cmd_description': 'Create a Planar mechanism',
        'cmd_id': 'planarCommand',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Planar mechanism',
        'cmd_resources': 'command_icons_planar',
        'command_visible': False,
        'command_promoted': False,
        }
    )   
    
    my_addin.add_command(
    'Cylindrical',
    SpringCommand,
        {
        'cmd_description': 'Create a Cylindrical mechanism',
        'cmd_id': 'cylindricalCommand',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Cylindrical mechanism',
        'cmd_resources': 'command_icons_cylindrical',
        'command_visible': False,
        'command_promoted': False,
        }
    )
    
    my_addin.add_command(
    'Spring',
    SpringCommand,
        {
        'cmd_description': 'Create a spring mechanism',
        'cmd_id': 'springCommand',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Spring mechanism',
        'cmd_resources': 'command_icons_spring',
        'command_visible': False,
        'command_promoted': False,
        }
    )
    
    my_addin.add_command(
    'Fabricate',
    FabricateCommand,
        {
        'cmd_description': 'Fabricate',
        'cmd_id': 'fabricateCommand',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Fabricate LamiFold',
        'cmd_resources': 'command_icons',
        'command_visible': True,
        'command_promoted': True,
        }
    )
    app = adsk.core.Application.cast(adsk.core.Application.get())
    ui = app.userInterface


except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    if ui:
        ui.messageBox('Initialization: {}'.format(traceback.format_exc()))

# Set to True to display various useful messages when debugging your app
debug = True


def run(context):
    my_addin.run_app()


def stop(context):
    my_addin.stop_app()
    sys.path.pop(0)
    sys.path.pop(0)
