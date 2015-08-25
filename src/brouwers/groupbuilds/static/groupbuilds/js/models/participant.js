import Api from 'scripts/api';
import Model from 'scripts/model';


class Participant extends Model {
    static Meta() {
        return {
            app_label: 'groupbuilds',
            endpoints: {
                list: 'groupbuilds/participant/',
                detail: 'groupbuilds/participant/:id/'
            }
        }
    }
}
