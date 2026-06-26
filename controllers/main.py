from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import base64

class LostFoundPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'lost_claim_count' in counters:
            values['lost_claim_count'] = request.env['lost.claim'].search_count([('user_id', '=', request.env.user.id)])
        if 'found_item_count' in counters:
            values['found_item_count'] = request.env['found.item'].search_count([('user_id', '=', request.env.user.id)])
        if 'item_claim_count' in counters:
            values['item_claim_count'] = request.env['item.claim.request'].search_count([('user_id', '=', request.env.user.id)])
        return values

    @http.route(['/'], type='http', auth="public", website=True)
    def portal_my_home_custom(self, **kw):
        lost_items = request.env['lost.claim'].sudo().search([('status', '=', 'approved')], limit=4, order='create_date desc')
        found_items = request.env['found.item'].sudo().search([('status', '=', 'approved')], limit=4, order='create_date desc')
        
        found_count = request.env['found.item'].sudo().search_count([('status', '=', 'approved')])
        lost_count = request.env['lost.claim'].sudo().search_count([('status', '=', 'approved')])
        user_count = request.env['res.users'].sudo().search_count([]) # Count all users including students
        
        values = {
            'lost_items': lost_items,
            'found_items': found_items,
            'found_count': found_count,
            'lost_count': lost_count,
            'user_count': user_count,
        }
        return request.render("lost_found_dashboard.custom_portal_home", values)

    @http.route(['/my/lost_items', '/my/lost_items/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_lost_items(self, page=1, **kw):
        if not request.env.user.phone:
            return request.redirect('/my/profil')
        values = self._prepare_portal_layout_values()
        LostClaim = request.env['lost.claim']
        domain = [('user_id', '=', request.env.user.id)]
        
        pager = portal_pager(
            url="/my/lost_items",
            total=LostClaim.search_count(domain),
            page=page,
            step=10
        )
        claims = LostClaim.search(domain, limit=10, offset=pager['offset'])
        values.update({
            'lost_claims': claims,
            'page_name': 'lost_items',
            'pager': pager,
            'default_url': '/my/lost_items',
        })
        return request.render("lost_found_dashboard.portal_my_lost_items", values)

    @http.route(['/my/found_items', '/my/found_items/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_found_items(self, page=1, **kw):
        if not request.env.user.phone:
            return request.redirect('/my/profil')
        values = self._prepare_portal_layout_values()
        FoundItem = request.env['found.item']
        domain = [('user_id', '=', request.env.user.id)]
        
        pager = portal_pager(
            url="/my/found_items",
            total=FoundItem.search_count(domain),
            page=page,
            step=10
        )
        items = FoundItem.search(domain, limit=10, offset=pager['offset'])
        values.update({
            'found_items': items,
            'page_name': 'found_items',
            'pager': pager,
            'default_url': '/my/found_items',
        })
        return request.render("lost_found_dashboard.portal_my_found_items", values)

    @http.route(['/my/lost_items/new'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_new_lost_item(self, **post):
        if not request.env.user.phone:
            return request.redirect('/my/profil')
            
        error = None
        if request.httprequest.method == 'POST':
            vals = {
                'name': post.get('name'),
                'description': post.get('description'),
                'location': post.get('location'),
                'date_lost': post.get('date_lost'),
                'person_name': request.env.user.name,
                'contact_email': request.env.user.email,
            }
            if post.get('image'):
                vals['photo'] = base64.b64encode(post.get('image').read())
            new_claim = request.env['lost.claim'].sudo().create(vals)
            
            # Send Email Template
            template = request.env.ref('lost_found_dashboard.email_template_lost_claim_created', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(new_claim.id, force_send=True)

            return request.redirect('/my/lost_items')
            
        locations = request.env['lost.claim'].sudo().fields_get(allfields=['location'])['location']['selection']
        return request.render("lost_found_dashboard.portal_new_lost_item", {'locations': locations, 'error': error})
        
    @http.route(['/my/lost_items/<int:item_id>'], type='http', auth="user", website=True)
    def portal_lost_item_detail(self, item_id, **kw):
        item = request.env['lost.claim'].search([('id', '=', item_id), ('user_id', '=', request.env.user.id)])
        if not item:
            return request.redirect('/my/lost_items')
        return request.render("lost_found_dashboard.portal_lost_item_detail", {'item': item})

    @http.route(['/my/lost_items/<int:item_id>/edit'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_lost_item_edit(self, item_id, **post):
        item = request.env['lost.claim'].search([('id', '=', item_id), ('user_id', '=', request.env.user.id), ('status', '=', 'draft')])
        if not item:
            return request.redirect('/my/lost_items')
            
        if request.httprequest.method == 'POST':
            vals = {
                'name': post.get('name'),
                'description': post.get('description'),
            }
            item.sudo().write(vals)
            return request.redirect(f'/my/lost_items/{item.id}')
            
        return request.render("lost_found_dashboard.portal_lost_item_edit", {'item': item})

    @http.route(['/my/found_items/new'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_new_found_item(self, **post):
        error = None
        if request.httprequest.method == 'POST':
            vals = {
                'name': post.get('name'),
                'description': post.get('description'),
                'location': post.get('location'),
                'date': post.get('date'),
            }
            if post.get('image'):
                vals['photo'] = base64.b64encode(post.get('image').read())
            new_item = request.env['found.item'].sudo().create(vals)
            
            # Send Email Template
            template = request.env.ref('lost_found_dashboard.email_template_found_item_created', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(new_item.id, force_send=True)

            return request.redirect('/my/found_items')
            
        locations = request.env['found.item'].sudo().fields_get(allfields=['location'])['location']['selection']
        return request.render("lost_found_dashboard.portal_new_found_item", {'locations': locations, 'error': error})

    @http.route(['/public/found_items'], type='http', auth="public", website=True)
    def public_found_items(self, **kw):
        search_kw = kw.get('search', '')
        item_type = kw.get('type', 'all')
        
        domain = [('status', '=', 'approved')]
        if search_kw:
            domain.append(('name', 'ilike', search_kw))
            
        lost_items = request.env['lost.claim'].sudo().search(domain, order='create_date desc')
        found_items = request.env['found.item'].sudo().search(domain, order='create_date desc')
            
        return request.render("lost_found_dashboard.public_found_items", {
            'lost_items': lost_items,
            'found_items': found_items,
            'item_type': item_type,
            'search_kw': search_kw
        })

    @http.route(['/public/lost_item/<int:item_id>'], type='http', auth="public", website=True)
    def public_lost_item(self, item_id, **kw):
        item = request.env['lost.claim'].sudo().browse(item_id)
        if not item.exists():
            return request.redirect('/public/found_items?type=lost')
        return request.render("lost_found_dashboard.public_lost_item_detail", {'item': item})

    @http.route(['/claim/found_item/<int:item_id>'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def claim_found_item(self, item_id, **post):
        item = request.env['found.item'].sudo().browse(item_id)
        if request.httprequest.method == 'POST':
            vals = {
                'found_item_id': item.id,
                'proof_description': post.get('proof_description'),
                'user_id': request.env.user.id,
            }
            if post.get('photo_proof'):
                vals['photo_proof'] = base64.b64encode(post.get('photo_proof').read())
                
            request.env['item.claim.request'].sudo().create(vals)
            return request.redirect('/my/claims')
            
        return request.render("lost_found_dashboard.portal_claim_found_item", {'item': item})

    @http.route(['/claim/lost_item/<int:item_id>'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def claim_lost_item(self, item_id, **post):
        item = request.env['lost.claim'].sudo().browse(item_id)
        if request.httprequest.method == 'POST':
            vals = {
                'lost_claim_id': item.id,
                'proof_description': post.get('proof_description'),
                'user_id': request.env.user.id,
            }
            if post.get('photo_proof'):
                vals['photo_proof'] = base64.b64encode(post.get('photo_proof').read())
                
            request.env['item.claim.request'].sudo().create(vals)
            return request.redirect('/my/claims')
            
        return request.render("lost_found_dashboard.portal_claim_lost_item", {'item': item})

    @http.route(['/my/claims'], type='http', auth="user", website=True)
    def portal_my_claims(self, **kw):
        claims = request.env['item.claim.request'].search([('user_id', '=', request.env.user.id)])
        return request.render("lost_found_dashboard.portal_my_claims", {'claims': claims})

    @http.route(['/my/profil'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_my_profil(self, **post):
        user = request.env.user
        partner = user.partner_id
        
        if request.httprequest.method == 'POST':
            # Update user info
            update_vals = {}
            if post.get('name'):
                update_vals['name'] = post.get('name')
            if post.get('email'):
                update_vals['email'] = post.get('email')
            if post.get('phone'):
                update_vals['phone'] = post.get('phone')
                
            if update_vals:
                partner.sudo().write(update_vals)
                    
            return request.redirect('/my/profil?success=1')
            
        values = {
            'user': user,
            'partner': partner,
            'success': request.params.get('success') == '1'
        }
        return request.render("lost_found_dashboard.portal_my_profil", values)

from odoo.addons.web.controllers.home import Home

class CustomHome(Home):
    def _login_redirect(self, uid, redirect=None):
        url = super()._login_redirect(uid, redirect=redirect)
        user = request.env['res.users'].browse(uid)
        
        # Admin / Staff goes directly to Dashboard (Pencocokan Barang)
        if user.has_group('lost_found_dashboard.group_lostnfound_staff') or user.has_group('base.group_system'):
            action = request.env.ref('lost_found_dashboard.action_item_matching_dashboard', raise_if_not_found=False)
            if action:
                return f'/web#action={action.id}'
            return '/web'
            
        # Regular Internal user
        if user.has_group('base.group_user'):
            return '/web'
            
        # Public / Portal users
        if url == '/my':
            return '/'
        return url
