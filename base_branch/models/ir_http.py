from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super(Http, self).session_info()
        user = request.env.user
        result.update(
            {
                "user_branches": {
                    "allowed_branches": [
                        (branch.id, branch.name) for branch in user.company_branch_ids
                    ],
                    "branch_ids": [branch.id for branch in user.branch_ids],
                    "current_branch_id": user.company_branch_id.id,
                    "current_branch_name": user.company_branch_id.name,
                },
                "display_switch_branch_menu": user.has_group(
                    "base_branch.group_multi_branches"
                )
                and len(user.company_branch_ids) > 1,
            }
        )
        return result
