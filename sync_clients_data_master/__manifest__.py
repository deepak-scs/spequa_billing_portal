# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sync Client Data - Master ",
    "version": "14.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
    "website": "www.serpentcs.com",
    "category": "Tools",
    "depends": ["hr", "mail", 'base_vat'],
    "data": [
        "security/ir.model.access.csv",
        "data/fetch_client_data.xml",
        "data/invoice_product_data.xml",
        "views/client_data_view.xml",
        "views/res_partner_view.xml",
    ],
    "application": True,
    "installable": True,
}
