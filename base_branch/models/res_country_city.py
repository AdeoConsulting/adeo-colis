from odoo import fields, models


class ResCountryCity(models.Model):
    _name = "res.country.city"
    _description = "City"
    _order = "code"

    state_id = fields.Many2one("res.country.state", string="State", required=True)
    name = fields.Char(string="Libelle", required=True)
    code = fields.Char(string="City Code", help="The city code.", required=True)

    _sql_constraints = [
        (
            "name_city_code_uniq",
            "unique(state_id, code)",
            "The code of the city must be unique by state !",
        )
    ]


class CountryState(models.Model):
    _inherit = "res.country.state"

    name = fields.Char(string="Libelle")
