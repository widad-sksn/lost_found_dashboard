from odoo import http
from odoo.http import request
import json

class LostFoundAPI(http.Controller):

    @http.route('/api/lost_found/metrics', type='http', auth='public', methods=['GET'], csrf=False)
    def get_metrics(self, **kwargs):
        # Allow CORS if needed
        headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')]
        
        try:
            lost_claims = request.env['lost.claim'].sudo().search_read([], ['status', 'date_lost', 'location'])
            found_items = request.env['found.item'].sudo().search_read([], ['status', 'date', 'location'])
            
            # Simple aggregations
            data = {
                'total_lost': len(lost_claims),
                'total_found': len(found_items),
                'lost_by_status': {},
                'found_by_status': {}
            }
            
            for claim in lost_claims:
                status = claim['status']
                data['lost_by_status'][status] = data['lost_by_status'].get(status, 0) + 1
                
            for item in found_items:
                status = item['status']
                data['found_by_status'][status] = data['found_by_status'].get(status, 0) + 1
                
            return request.make_response(json.dumps(data), headers=headers)
        except Exception as e:
            error_data = {'error': str(e)}
            return request.make_response(json.dumps(error_data), headers=headers, status=500)
