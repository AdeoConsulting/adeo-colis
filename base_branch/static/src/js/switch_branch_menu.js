odoo.define("base_branch.SwitchBranchMenu", function(require) {
    "use strict";

    var config = require("web.config");
    var session = require("web.session");
    var SystrayMenu = require("web.SystrayMenu");
    var Widget = require("web.Widget");

    var SwitchBranchMenu = Widget.extend({
        template: "SwitchBranchMenu",
        events: {
            "click .dropdown-item[data-menu] div.log_into": "_onSwitchBranchClick",
            "click .dropdown-item[data-menu] div.toggle_company":
                "_onToggleBranchClick",
        },
        // @override
        init: function() {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
            this._onSwitchCompanyClick = _.debounce(
                this._onSwitchCompanyClick,
                1500,
                true
            );
        },

        // @override
        willStart: function() {
            this.allowed_branch_ids = session.user_branches.branch_ids;
            this.user_branches = session.user_branches.allowed_branches;
            this.current_branch = session.user_branches.current_branch_id;
            this.current_branch_name = session.user_branches.current_branch_name;
            return this._super.apply(this, arguments);
        },

        setBranches: function(main_branch_id, branch_ids) {
            this._rpc({
                model: "res.users",
                method: "update_branch_ids",
                args: [session.uid, main_branch_id, branch_ids],
            }).then(function() {
                location.reload();
            });
        },
        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onSwitchBranchClick: function(ev) {
            ev.stopPropagation();
            var dropdownItem = $(ev.currentTarget).parent();
            var dropdownMenu = dropdownItem.parent();
            var branchID = dropdownItem.data("branch-id");
            var allowed_branch_ids = this.allowed_branch_ids;
            if (dropdownItem.find(".fa-square-o").length) {
                // 1 enabled branch: Stay in single branch mode
                if (this.allowed_branch_ids.length === 1) {
                    dropdownMenu
                        .find(".fa-check-square")
                        .removeClass("fa-check-square")
                        .addClass("fa-square-o");
                    dropdownItem
                        .find(".fa-square-o")
                        .removeClass("fa-square-o")
                        .addClass("fa-check-square");
                    allowed_branch_ids = [branchID];
                } else {
                    // Multi branch mode
                    allowed_branch_ids.push(branchID);
                    dropdownItem
                        .find(".fa-square-o")
                        .removeClass("fa-square-o")
                        .addClass("fa-check-square");
                }
            }
            this.setBranches(branchID, null);
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onToggleBranchClick: function(ev) {
            ev.stopPropagation();
            var dropdownItem = $(ev.currentTarget).parent();
            var branchID = dropdownItem.data("branch-id");
            var allowed_branch_ids = this.allowed_branch_ids;
            if (dropdownItem.find(".fa-square-o").length) {
                allowed_branch_ids.push(branchID);
                dropdownItem
                    .find(".fa-square-o")
                    .removeClass("fa-square-o")
                    .addClass("fa-check-square");
            } else {
                allowed_branch_ids.splice(allowed_branch_ids.indexOf(branchID), 1);
                dropdownItem
                    .find(".fa-check-square")
                    .addClass("fa-square-o")
                    .removeClass("fa-check-square");
            }
            this.setBranches(null, allowed_branch_ids);
        },
    });

    if (session.display_switch_branch_menu) {
        SystrayMenu.Items.push(SwitchBranchMenu);
    }

    return SwitchBranchMenu;
});
