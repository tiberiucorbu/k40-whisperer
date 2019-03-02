import {TextFieldElement} from "@vaadin/vaadin-text-field/src/vaadin-text-field";

class NotAnUrlError extends Error {
}

class NotAWebSocketError extends Error {
}

class UnableToConnectToServerError extends Error {
    constructor(e) {
        super();
        this.cause = e;
    }

}

export class K40WssTextField extends TextFieldElement {
    static get is() {
        return 'k40-wss-text-field';
    }

    async testConnection() {
        let ws;
        return new Promise((res, rej) => {
            ws = new WebSocket(this.value);
            ws.onopen = res;
            ws.onerror = (e) => {
                rej(
                    new UnableToConnectToServerError(e)
                )
            };
        }).finally(() => {
            if (!!ws) {
                ws.close();
            }
        })

    }

    testUrlFormat() {
        let url;
        try {
            url = new URL(this.value);
        } catch (e) {
            throw new NotAnUrlError();
        }
        if (!this.isWebSocket(url)) {
            throw new NotAWebSocketError();
        }
    }

    isWebSocket(url) {
        return url.protocol === 'ws:' || url.protocol === 'wss:';
    }

    async validate() {
        const valid = await this.checkValidity();
        this.invalid = !valid;
        return valid;
    }


    async checkValidity() {
        let invalid = false;
        try {
            this.testUrlFormat();
            await this.testConnection();
            this.errorMessage = '';
        } catch (e) {
            invalid = true;
            if (e instanceof NotAnUrlError) {
                this.errorMessage = 'Not a valid url'
            }
            if (e instanceof NotAWebSocketError) {
                this.errorMessage = 'Url is not a web socket';
            }
            if (e instanceof UnableToConnectToServerError) {
                this.errorMessage = 'Cannot connect';
            }
        }
        return !invalid;
    }
}