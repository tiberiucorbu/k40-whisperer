import {BehaviorSubject} from "rxjs";
import {map} from 'rxjs/operators';

class K40Configuration {

    constructor(key) {
        this.key = key;
        this.configurationSubject = new BehaviorSubject({});
        this.syncConfigurationFormStorage(window.localStorage);
    }

    syncConfigurationFormStorage(storage) {
        let configuration = this._configuration || {};
        try {
            let item = storage.getItem(this.key);
            configuration = JSON.parse(item);
        } finally {
            this._configuration = configuration;
        }
    }

    get configuration() {
        return this._configuration || {};
    }

    set configuration(configuration) {
        this._configuration = configuration || {};
        window.localStorage.setItem(this.key, JSON.stringify(this._configuration));
        this.syncConfigurationFormStorage(window.localStorage);
        this.configurationSubject.next(configuration)
    }


    get exists() {
        return !!window.localStorage.getItem(this.key)
    }


    configurationChanges() {
        return this.configurationSubject.pipe(map((item) => item));
    }
}

export const ConnectionConfig = new K40Configuration('k40-configuration-connection');
