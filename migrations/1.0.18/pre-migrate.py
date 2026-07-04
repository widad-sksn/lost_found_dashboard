def migrate(cr, version):
    cr.execute("UPDATE ir_model_data SET noupdate = False WHERE module = 'lost_found_dashboard' AND model = 'mail.template';")
