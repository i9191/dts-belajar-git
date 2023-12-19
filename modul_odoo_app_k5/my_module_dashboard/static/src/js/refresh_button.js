/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class clasButtonRefersh extends ListController {
    setup() {
        super.setup();
    }

    async OnRefreshClick() {
        var rpc = require('web.rpc')
        console.log("infoooooooooo");
        const wizardModel = 'wizard.dashboard.refresh';
        return rpc.query({
            model: wizardModel,
            method: 'refresh_data',  // Gantilah dengan method create yang sesuai
            args: [""]
        }).then(function (res){
            console.log("marii");
            location.reload();
    
            // this.trigger('reload');  // Untuk merefresh tampilan setelah pembaruan data

        });
    }
 
}
registry.category("views").add("refresh_button", {
    ...listView,
    Controller: clasButtonRefersh,
    buttonTemplate: "refreshButton.ListView.Buttons",
});