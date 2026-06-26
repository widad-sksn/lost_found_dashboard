from odoo import models, api

class Users(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        if not password:
            return super(Users, cls)._login(db, login, password, user_agent_env)

        with cls.pool.cursor() as cr:
            cr.execute("""
                SELECT u.login 
                FROM res_users u 
                JOIN res_partner p ON u.partner_id = p.id 
                WHERE (u.login=%s OR p.email=%s) AND u.active=TRUE 
                LIMIT 1
            """, (login, login))
            res = cr.fetchone()
            if res:
                # Use the actual login field for authentication
                login = res[0]

        return super(Users, cls)._login(db, login, password, user_agent_env)
