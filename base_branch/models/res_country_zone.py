from odoo import fields, models


class ResCountryZone(models.Model):
    _description = "Zone"
    _name = "res.country.zone"
    _order = "code"

    city_id = fields.Many2one("res.country.city", string="City", required=True)
    name = fields.Char(string="Libelle", required=True)
    code = fields.Char(string="Zone Code", help="The zone code.", required=True)

    _sql_constraints = [
        (
            "name_zone_code_uniq",
            "unique(city_id, code)",
            "The code of the zone must be unique by city !",
        )
    ]
