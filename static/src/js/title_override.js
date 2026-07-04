/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";

patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        this.title.setParts({ zopenerp: "Smart Lost & Found" });
    }
});
