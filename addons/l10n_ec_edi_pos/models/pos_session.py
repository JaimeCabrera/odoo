from odoo import models


class PosSession(models.Model):

    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.company_id.country_code == 'EC':
            result.append('l10n_latam.identification.type')
        return result

    def _loader_params_l10n_latam_identification_type(self):
        return {
            'search_params': {
                'domain': [('active', '=', True)],
                'fields': ['name'],
            },
        }

    def _get_pos_ui_l10n_latam_identification_type(self, params):
        return self.env['l10n_latam.identification.type'].search_read(**params['search_params'])

    def _loader_params_res_partner(self):
        vals = super()._loader_params_res_partner()
        if self.company_id.country_code == 'EC':
            vals['search_params']['fields'] += ['l10n_latam_identification_type_id']
        return vals

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        if self.company_id.country_code == 'EC':
            final_consumer = self.env.ref('l10n_ec.ec_final_consumer', raise_if_not_found=False)
            if final_consumer:
                loaded_data['final_consumer_id'] = final_consumer.id

    def _create_account_move(self, balancing_account, amount_to_balance, bank_payment_method_diffs):
        """Override to add user information to the closing entry reference."""
        move = super()._create_account_move(balancing_account, amount_to_balance, bank_payment_method_diffs)
        if move:
            # Add user information to the reference
            user_name = self.user_id.name or self.env.user.name
            current_ref = move.ref or ''
            move.ref = f"{current_ref} - Usuario: {user_name}"
        return move
