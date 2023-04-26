from . import models
from odoo import api, SUPERUSER_ID

def _setup_access_rights():
    # Allow admin and members of the Employees group to access all records
    # of the odoosense.odoosense model
    # Members of other groups will not have access to any records by default.
    env = api.Environment(SUPERUSER_ID, 'odoosense')
    employees_group = env.ref('base.group_user')
    employees_group.write({'implied_ids': [(4, env.ref('odoosense.group_odoosense_user').id)]})

def uninstall_hook(cr, registry):
    # Remove the implied group relationship when the module is uninstalled
    env = api.Environment(cr, SUPERUSER_ID, {})
    employees_group = env.ref('base.group_user')
    employees_group.write({'implied_ids': [(3, env.ref('odoosense.group_odoosense_user').id)]})