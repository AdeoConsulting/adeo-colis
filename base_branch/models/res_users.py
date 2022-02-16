from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"

    company_branch_ids = fields.Many2many(
        "res.company.branch", string="Allowed Branches", copy=False
    )
    branch_ids = fields.Many2many(
        "res.company.branch",
        "res_users_branch_rel",
        "user_id",
        "branch_id",
        string="Current Branches",
        copy=False,
    )
    company_branch_id = fields.Many2one(
        "res.company.branch", string="Current Branch", copy=False
    )

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        admin_user = self.env.user
        public_user = self.env.ref("base.public_user")
        if (
            admin_user
            and not admin_user.has_group("base.group_erp_manager")
            and admin_user != public_user
        ):
            args = [
                "|",
                ("company_branch_id", "=", False),
                ("company_branch_id", "=", self.env.user.company_branch_id.id),
            ] + list(args)
        return super(Users, self)._search(
            args, offset, limit, order, count, access_rights_uid
        )

    def write(self, vals):
        if vals.get("company_branch_id"):
            return super(Users, self.sudo()).write(vals)
        return super(Users, self).write(vals)

    def read(self, fields=None, load="_classic_read"):
        read_partner = super(Users, self).read(fields, load=load)
        admin_user = self.env.user.has_group("base.group_erp_manager")
        if admin_user:
            return read_partner
        for partner in read_partner:
            if (
                partner.get("company_branch_id")
                and self.env.user.company_branch_id.id != partner["company_branch_id"]
            ):
                if (
                    isinstance(partner["company_branch_id"], tuple)
                    and self.env.user.company_branch_id.id
                    != partner["company_branch_id"][0]
                ):
                    raise ValidationError(_("You are not allowed to access"))
        return read_partner

    @api.onchange("company_branch_ids")
    def _onchange_company_branch_ids(self):
        new_branch_ids = [
            branch_id
            for branch_id in self.branch_ids.ids
            if branch_id in self.company_branch_ids.ids
        ]
        self.branch_ids = [(6, 0, new_branch_ids)]

    @api.onchange("company_branch_id")
    def _onchange_company_branch_id(self):
        if self.company_branch_id:
            if self.company_branch_id.id not in self.branch_ids.ids:
                self.branch_ids = [(4, self.company_branch_id.id)]

    @api.model
    def update_branch_ids(self, user_id, branch_id=None, branch_ids=None):
        """Called when user switch between branches."""
        user = self.env["res.users"].sudo().browse(user_id)
        if branch_id:
            user.company_branch_id = branch_id
            if branch_id not in self.branch_ids.ids:
                user.branch_ids = [(4, branch_id)]
        if branch_ids:
            user.branch_ids = [(6, 0, branch_ids)]
        if user.company_branch_id not in user.branch_ids:
            user.branch_ids = [(4, user.company_branch_id.id)]
        self.clear_caches()
