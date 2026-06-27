/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";
import { View } from "@web/views/view";

export class ItemMatchingDashboard extends Component {
    static components = { View };
    
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.user = useService("user");
        
        this.state = useState({
            activeMenu: 'matching', // 'matching', 'lost', 'found', 'claims'
            currentResModel: '',
            currentViewType: 'list',
            matches: [],
            currentIndex: 0,
            loading: false,
            userName: "",
            modalImage: false,
            selectedMatch: null
        });

        onWillStart(async () => {
            this.state.userName = this.user.name || "Admin User";
            await this.fetchMatches();
        });
    }

    setModalImage(base64Image) {
        this.state.modalImage = base64Image;
    }

    openMatchDetail(match) {
        this.state.selectedMatch = match;
    }

    closeMatchDetail() {
        this.state.selectedMatch = null;
    }

    get viewProps() {
        const props = {
            type: this.state.currentViewType,
            resModel: this.state.currentResModel,
            display: { controlPanel: true },
            selectRecord: (resId) => this.openFormView(resId),
            createRecord: () => this.openFormView(false),
        };
        
        if (this.state.activeMenu === 'found' || this.state.activeMenu === 'lost') {
            props.domain = [['status', '!=', 'done']];
        } else if (this.state.activeMenu === 'history_found' || this.state.activeMenu === 'history_lost') {
            props.domain = [['status', '=', 'done']];
        }
        
        if (this.state.currentViewType === 'kanban') {
            props.forceGlobalClick = true;
        }
        return props;
    }

    openFormView(resId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: this.state.currentResModel,
            res_id: resId || false,
            views: [[false, "form"]],
            target: "new",
        });
    }

    async fetchMatches() {
        this.state.loading = true;
        try {
            this.state.matches = await this.orm.call(
                "item.claim.request",
                "get_pending_claims_for_dashboard",
                []
            );
            this.state.currentIndex = 0;
        } catch (error) {
            console.error("Error fetching matches:", error);
        } finally {
            this.state.loading = false;
        }
    }

    navigateToAction(actionTag) {
        if (actionTag === 'dashboard') {
            window.location.href = '/';
            return;
        }
        
        if (actionTag === 'lost_found_dashboard.found_item_action') {
            this.state.activeMenu = 'found';
            this.state.currentResModel = 'found.item';
            this.state.currentViewType = 'list';
        } else if (actionTag === 'history_found') {
            this.state.activeMenu = 'history_found';
            this.state.currentResModel = 'found.item';
            this.state.currentViewType = 'list';
        } else if (actionTag === 'lost_found_dashboard.lost_claim_action') {
            this.state.activeMenu = 'lost';
            this.state.currentResModel = 'lost.claim';
            this.state.currentViewType = 'list';
        } else if (actionTag === 'history_lost') {
            this.state.activeMenu = 'history_lost';
            this.state.currentResModel = 'lost.claim';
            this.state.currentViewType = 'list';
        } else if (actionTag === 'lost_found_dashboard.action_item_matching') {
            this.state.activeMenu = 'matching';
        } else if (actionTag === 'lost_found_dashboard.item_claim_request_action') {
            this.state.activeMenu = 'claims';
            this.state.currentResModel = 'item.claim.request';
            this.state.currentViewType = 'list';
        } else {
            this.action.doAction(actionTag);
        }
    }

    async onMatchClick() {
        if (this.state.loading || !this.state.selectedMatch) return;
        
        const currentMatch = this.state.selectedMatch;
        this.state.loading = true;
        
        try {
            await this.orm.call(
                "item.claim.request",
                "action_approve",
                [[currentMatch.claim_id]]
            );
            
            this.notification.add("Klaim berhasil disetujui. Notifikasi telah dikirim!", {
                type: "success",
            });
            
            this.state.selectedMatch = null;
            this.fetchMatches();
        } catch (error) {
            this.notification.add("Gagal menyetujui klaim.", {
                type: "danger",
            });
            console.error(error);
        } finally {
            this.state.loading = false;
        }
    }

    async onSkipClick() {
        if (this.state.loading || !this.state.selectedMatch) return;
        
        const currentMatch = this.state.selectedMatch;
        this.state.loading = true;
        
        try {
            await this.orm.call(
                "item.claim.request",
                "action_reject",
                [[currentMatch.claim_id]]
            );
            
            this.notification.add("Klaim ditolak.", {
                type: "success",
            });
            
            this.state.selectedMatch = null;
            this.fetchMatches();
        } catch (error) {
            this.notification.add("Gagal menolak klaim.", {
                type: "danger",
            });
            console.error(error);
        } finally {
            this.state.loading = false;
        }
    }
}

ItemMatchingDashboard.template = "lost_found_dashboard.ItemMatchingDashboard";

registry.category("actions").add("lost_found_dashboard.action_item_matching", ItemMatchingDashboard);
