/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class AkademikListController extends ListController {
    setup() {
        super.setup();
    }
    OnNilaiReadCSVClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'wizard.dataakademik.csv',
            name: 'Baca Data Akademik Mahasiswa dari CSV',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_id: false,
        });
    }
    OnMatkulReadCSVClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'wizard.readcsv.matkul',
            name: 'Baca Data Mata Kuliah Akademik dari CSV',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_id: false,
        });
    }
    OnMhsReadCSVClick() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'wizard.datamahasiswa',
            name: 'Baca Data Mahasiswa dari CSV',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_id: false,
        });
    }
}
registry.category("views").add("readnilai_button", {
    ...listView,
    Controller: AkademikListController,
    buttonTemplate: "button_akademik.ListView.Buttons",
});
registry.category("views").add("readmatkul_button", {
    ...listView,
    Controller: AkademikListController,
    buttonTemplate: "button_matkul.ListView.Buttons",
});
registry.category("views").add("readmhs_button", {
    ...listView,
    Controller: AkademikListController,
    buttonTemplate: "button_mhs.ListView.Buttons",
});