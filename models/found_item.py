from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FoundItem(models.Model):
    _name = "found.item"
    _description = "Found Item list"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Item Name", required=True, tracking=True)
    description = fields.Text(string="Item Description")
    ref_id = fields.Char(string="Tracking ID", readonly=True, copy=False, default="New")
    user_id = fields.Many2one('res.users', string="Reporter", default=lambda self: self.env.user, readonly=True)
    
    tag_ids = fields.Many2many('item.tag', string="Tags")

    # Some Common areas where they could loose things @>XO<@
    location = fields.Selection([
        ('a1_lab_utara', 'Gedung A - A.1. Lab Utara'),
        ('a1_gymnasium', 'Gedung A - A.1. Depan R. Gymnasium'),
        ('a2_r_prodi', 'Gedung A - A.2. R. Prodi'),
        ('a3_301', 'Gedung A - A.3. 301'),
        ('a3_meeting', 'Gedung A - A.3. MEETING FIKES'),
        ('a4_aula_selatan', 'Gedung A - A.4. Aula Selatan'),
        ('a4_aula_utara', 'Gedung A - A.4. Aula Utara'),
        ('a4_r_dosen', 'Gedung A - A.4. R. Dosen'),
        ('a_sw_lt4', 'Gedung A - SW Lt.4.R.Kls.FK1'),
        ('b1_lab_histologi', 'Gedung B - B.1. LAB Histologi'),
        ('b1_r_dosen', 'Gedung B - B.1. R. Dosen Profesi'),
        ('b1_mr1', 'Gedung B - B.1. MR 1 (Barat Admin FK)'),
        ('b1_mr2', 'Gedung B - B.1. MR 2 (Depan Panggung)'),
        ('b1_anatomi_basah', 'Gedung B - B.1. ANATOMI BASAH'),
        ('b1_r_transit', 'Gedung B - B.1. R. Transit'),
        ('b1_anatomi_kering', 'Gedung B - B.1. ANATOMI KERING'),
        ('b2_02', 'Gedung B - B.2. 02'),
        ('b2_05', 'Gedung B - B.2. 05'),
        ('b2_12', 'Gedung B - B.2. 12'),
        ('b2_lab_komunikasi', 'Gedung B - B.2. Lab Komunikasi'),
        ('b3_02', 'Gedung B - B.3. 02'),
        ('b3_depan_lab', 'Gedung B - B.3. Depan Lab'),
        ('b3_lorong', 'Gedung B - B.3. Lorong'),
        ('b4_01', 'Gedung B - B.4. 01'),
        ('b4_03', 'Gedung B - B.4. 03'),
        ('b4_07_biotek', 'Gedung B - B.4. 07 / Biotek'),
        ('b4_lab_lt4', 'Gedung B - B.4. Lab Lantai 4'),
        ('b4_lab_skill', 'Gedung B - B.4. Lab Skill'),
        ('b4_lab_toksikologi', 'Gedung B - B.4. Lab Toksikologi'),
        ('b5_02_01', 'Gedung B - B.5. 02/01'),
        ('b5_06_07', 'Gedung B - B.5. 06/07'),
        ('b5_depan_lab', 'Gedung B - B.5. Depan Lab'),
        ('b6_01', 'Gedung B - B.6. 01'),
        ('b6_lab_skill', 'Gedung B - B.6. Lab Skill'),
        ('c_r202', 'Gedung C - C.R. 2.02 (Meeting-Barat)'),
        ('c_r3_timur', 'Gedung C - C.R. 3 (Timur)'),
        ('c_r404', 'Gedung C - C.R. 4.04'),
        ('c_r502', 'Gedung C - C.R. 5.02'),
        ('c_r503', 'Gedung C - C.R. 5.03'),
        ('c_r504', 'Gedung C - C.R. 5.04'),
        ('c_r505', 'Gedung C - C.R. 5.05'),
        ('c_r507', 'Gedung C - C.R. 5.07'),
        ('c_r508', 'Gedung C - C.R. 5.08'),
        ('c_r509', 'Gedung C - C.R. 5.09'),
        ('kp1_206', 'KP1 - R. 206'),
        ('kp1_210', 'KP1 - R. 210'),
        ('kp1_211', 'KP1 - R. 211'),
        ('kp1_212', 'KP1 - R. 212'),
        ('kp1_213', 'KP1 - R. 213'),
        ('kp1_304', 'KP1 - R. 304'),
        ('kp1_akademik', 'KP1 - R. Akademik'),
        ('kp1_perpus', 'KP1 - R. Perpustakaan'),
        ('kp1_218', 'KP1 - R. 218'),
        ('sm1_lab_adm', 'Gedung SM - SM 1 Lab Adm Publik'),
        ('sm1_public_selatan', 'Gedung SM - SM 1 Public (Barat-Selatan)'),
        ('sm2_sidang_barat', 'Gedung SM - SM 2 R. Sidang Barat'),
        ('sm9_tengah', 'Gedung SM - SM Lt.9 Tengah'),
        ('sm_pojok_perpus', 'Gedung SM - POJOK PERPUS'),
        ('sm1_public_utara', 'Gedung SM - SM 1 Public (Barat-Utara)'),
        ('asrama_lt1', 'Asrama - AP ASRAMA LT 1'),
        ('asrama_lt2', 'Asrama - AP ASRAMA LT 2'),
        ('asrama_lt3', 'Asrama - AP ASRAMA LT 3'),
        ('asrama_lt4', 'Asrama - AP ASRAMA LT 4'),
        ('taman', 'Taman Kampus'),
        ('parkir_c', 'Parkiran Gedung C'),
        ('parkir_b', 'Parkiran Gedung B'),
        ('parkir_dosen', 'Parkiran Dosen'),
        ('parkir_masjid', 'Parkiran Masjid'),
        ('masjid', 'Masjid Kampus'),
        ('kantin', 'Kantin Kampus'),
        ('auditorium', 'Auditorium (Lainnya)'),
        ('1st_floor', '1st Floor (Lainnya)'),
        ('2nd_floor', '2nd Floor (Lainnya)'),
        ('3rd_floor','3rd Floor (Lainnya)'),
        ('hallway', 'Hallway (Lainnya)'),
        ('main_lobby', 'Main Lobby (Lainnya)'),
        ('cash_register', 'Cash Register (Lainnya)'),
        ('cafeteria', 'Cafeteria (Lainnya)'),
        ('library', 'Library (Lainnya)'),
        ('campus_grounds', 'Outdoor Campus Grounds (Lainnya)')
    ], string="Location", required=True)
    

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    photo = fields.Image(string="Photo", max_width=1024, max_height=1024)
    
    status = fields.Selection([
        ('draft', 'Menunggu'),
        ('approved', 'Dipublikasikan'),
        ('rejected', 'Ditolak'),
        ('done', 'Diklaim (Claimed)')
    ], string="Status", default='draft', tracking=True)
    

    def action_approve(self):
        for record in self:
            record.status = 'approved'
            template = self.env.ref('lost_found_dashboard.email_template_found_item_approved', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(record.id, force_send=True)
        return True

    def action_reject(self):
        for record in self:
            record.status = 'rejected'
            template = self.env.ref('lost_found_dashboard.email_template_found_item_rejected', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(record.id, force_send=True)
        return True

    def action_done(self):
        for record in self:
            record.status = 'done'
            template = self.env.ref('lost_found_dashboard.email_template_report_done_found', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(record.id, force_send=True)
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref_id', 'New') == 'New':
                total_items = self.search_count([])
                next_number = total_items + 1
                vals['ref_id'] = f"FND/{next_number:03d}"
        return super().create(vals_list)
