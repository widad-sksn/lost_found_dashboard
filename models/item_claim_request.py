from odoo import models, fields, api

class ItemClaimRequest(models.Model):
    _name = "item.claim.request"
    _description = "Item Claim Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    found_item_id = fields.Many2one('found.item', string="Barang Ditemukan", tracking=True)
    lost_claim_id = fields.Many2one('lost.claim', string="Data Barang Hilang", tracking=True)
    user_id = fields.Many2one('res.users', string="Pengklaim", default=lambda self: self.env.user, readonly=True, required=True, tracking=True)
    proof_description = fields.Text(string="Keterangan / Detail Bukti", required=True)
    photo_proof = fields.Image(string="Foto Bukti", max_width=1024, max_height=1024)
    
    status = fields.Selection([
        ('draft', 'Menunggu Verifikasi'),
        ('approved', 'Diterima'),
        ('rejected', 'Ditolak')
    ], string="Status Klaim", default='draft', tracking=True)
    
    admin_notes = fields.Text(string="Catatan Admin")

    @api.constrains('found_item_id', 'lost_claim_id')
    def _check_target_item(self):
        for record in self:
            if not record.found_item_id and not record.lost_claim_id:
                raise models.ValidationError("Klaim harus tertuju pada Barang Ditemukan atau Data Barang Hilang.")

    def action_approve(self):
        for record in self:
            record.status = 'approved'
            
            # Send Notification to Claimer
            template_claimer = self.env.ref('lost_found_dashboard.email_template_claim_approved', raise_if_not_found=False)
            if template_claimer:
                template_claimer.sudo().send_mail(record.id, force_send=True)
                
            # Send Notification to original Reporter and update status to done
            if record.found_item_id:
                record.found_item_id.status = 'done'
                template_finder = self.env.ref('lost_found_dashboard.email_template_finder_matched', raise_if_not_found=False)
                if template_finder and record.found_item_id.user_id:
                    template_finder.sudo().send_mail(record.id, force_send=True)
            elif record.lost_claim_id:
                record.lost_claim_id.status = 'done'
                template_loser = self.env.ref('lost_found_dashboard.email_template_loser_matched', raise_if_not_found=False)
                if template_loser and record.lost_claim_id.user_id:
                    template_loser.sudo().send_mail(record.id, force_send=True)

        return True

    def action_reject(self):
        for record in self:
            record.status = 'rejected'
            
            # Send Email Notification
            template = self.env.ref('lost_found_dashboard.email_template_claim_rejected', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(record.id, force_send=True)
                
        return True

    @api.model
    def get_pending_claims_for_dashboard(self):
        claims = self.search([('status', '=', 'draft')])
        res = []
        for claim in claims:
            data = {
                'claim_id': claim.id,
                'claim_user': claim.user_id.name or "Unknown",
                'claim_date': claim.create_date.strftime("%Y-%m-%d %H:%M") if claim.create_date else "",
                'claim_proof_description': claim.proof_description or "",
                'claim_photo': claim.photo_proof.decode('utf-8') if claim.photo_proof else False,
            }
            if claim.found_item_id:
                data.update({
                    'item_type': 'Barang Ditemukan',
                    'original_name': claim.found_item_id.name,
                    'original_category': ", ".join(claim.found_item_id.tag_ids.mapped('name')) if claim.found_item_id.tag_ids else "-",
                    'original_location': dict(self.env['found.item']._fields['location'].selection).get(claim.found_item_id.location, claim.found_item_id.location) if claim.found_item_id.location else "",
                    'original_date': claim.found_item_id.date.strftime("%Y-%m-%d") if claim.found_item_id.date else "",
                    'original_reporter': claim.found_item_id.user_id.name or "Unknown",
                    'original_description': claim.found_item_id.description or "",
                    'original_photo': claim.found_item_id.photo.decode('utf-8') if claim.found_item_id.photo else False,
                })
            elif claim.lost_claim_id:
                data.update({
                    'item_type': 'Data Barang Hilang',
                    'original_name': claim.lost_claim_id.name,
                    'original_category': ", ".join(claim.lost_claim_id.tag_ids.mapped('name')) if claim.lost_claim_id.tag_ids else "-",
                    'original_location': dict(self.env['lost.claim']._fields['location'].selection).get(claim.lost_claim_id.location, claim.lost_claim_id.location) if claim.lost_claim_id.location else "",
                    'original_date': claim.lost_claim_id.date_lost.strftime("%Y-%m-%d") if claim.lost_claim_id.date_lost else "",
                    'original_reporter': claim.lost_claim_id.person_name or claim.lost_claim_id.user_id.name or "User",
                    'original_description': claim.lost_claim_id.description or "",
                    'original_photo': claim.lost_claim_id.photo.decode('utf-8') if claim.lost_claim_id.photo else False,
                })
            res.append(data)
        return res
