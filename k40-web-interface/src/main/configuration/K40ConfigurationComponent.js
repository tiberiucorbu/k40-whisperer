import {css, html, LitElement} from "lit-element";

export class K40ConnectionConfiguration extends LitElement {

    static get properties() {
        return {
            wssUrl: {type: String},
            username: {type: String},
            token: {type: String}
        }
    }

    static get styles() {
        return css`
        :host { 
            min-width : 10rem; height: 100%; display : flex; flex-flow: column nowrap;
        }
        `;
    }

    render() {
        return html`
        <h2>Connection Settings</h2>
        <vaadin-form-layout>
          <k40-wss-text-field id="wss-url" label="WebSocket url" placeholder="wss://rpilocal:480" required value="${this.wssUrl || ''}"></k40-wss-text-field>
          <vaadin-text-field id="username" label="Name" placeholder="John" required value="${this.username || ''}"></vaadin-text-field>
          <vaadin-text-area  id="token" label="Authorization Token"  required placeholder="" value="${this.token || ''}"></vaadin-text-area>
        </vaadin-form-layout>
            `;
    }

    firstUpdated(_changedProperties) {
        super.firstUpdated(_changedProperties);
        this.findElements();
        this.attachEventListeners();
    }

    attachEventListeners() {
        this.wssUrlTextField.oninput = (e) => {
            this.wssUrl = this.wssUrlTextField.value;
        };
        this.userNameTextField.oninput = (e) => {
            this.username = this.userNameTextField.value;
        };
        this.tokenTextField.oninput = (e) => {
            this.token = this.tokenTextField.value;
        };
    }

    findElements() {
        this.wssUrlTextField = this.shadowRoot.getElementById('wss-url');
        this.userNameTextField = this.shadowRoot.getElementById('username');
        this.tokenTextField = this.shadowRoot.getElementById('token');
    }
}

