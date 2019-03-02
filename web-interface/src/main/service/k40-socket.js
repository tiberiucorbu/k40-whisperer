export class K40Socket {

    constructor(options) {
        this.options = options;
    }

    connect() {
       this.socket = new WebSocket(this.options.url);
    }

}