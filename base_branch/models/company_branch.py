from odoo import fields, models


class CompanyBranch(models.Model):
    _name = "res.company.branch"
    _description = "Company Branch"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    user_id = fields.Many2one("res.users", string="Manager")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=1,
    )
    zone_id = fields.Many2one("res.country.zone", string="Zone")
    logo = fields.Binary(string="Branch Logo")
