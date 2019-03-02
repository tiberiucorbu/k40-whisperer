import {css, html, LitElement} from 'lit-element';
import {configuration, ConnectionConfig} from "./configuration/K40Configuration";

export class K40Main extends LitElement {

    static get properties() {
        return {
            mood: {type: String}
        }
    }

    static get styles() {
        return css`:host { width : 100%; height: 100%; display: block; }`;
    }

    render() {
        // if (!configuration.connection)
        return html`
                <k40-layout>
                     <vaadin-dialog id="dialog">
                        <k40-connection-configuration></k40-connection-configuration>
                    </vaadin-dialog>
                    <p> There is no configuration present into the local storage, unable to connect to the server without it </p>
                    <vaadin-button id="open-configuration-dialog-button">Configure</vaadin-button>
                </k40-layout>
            `;
    }

    async firstUpdated(_changedProperties) {
        super.firstUpdated(_changedProperties);
        await this.findElements();

        const connectionConfigurationComponent = document.createElement('k40-connection-configuration');
        let updateConnectionConfiguration = (value) => {
            connectionConfigurationComponent.wssUrl = value.wssUrl;
            connectionConfigurationComponent.username = value.username;
            connectionConfigurationComponent.token = value.token;
        };

        updateConnectionConfiguration(ConnectionConfig.configuration);
        ConnectionConfig.configurationChanges().subscribe(updateConnectionConfiguration);
        connectionConfigurationComponent.oninput = (e) => {
            ConnectionConfig.configuration = {
                wssUrl: connectionConfigurationComponent.wssUrl,
                token: connectionConfigurationComponent.token,
                username: connectionConfigurationComponent.username
            };
        }

        this.dialog.renderer = function (root, dialog) {
            root.appendChild(connectionConfigurationComponent);
        };
        this.button.onclick = async () => {
            this.dialog.opened = true;
        };

    }

    async findElements() {
        this.button = this.shadowRoot.getElementById('open-configuration-dialog-button');
        this.dialog = this.shadowRoot.getElementById('dialog');
        await customElements.whenDefined('vaadin-dialog');
        await customElements.whenDefined('k40-connection-configuration');
    }

    async updated(_changedProperties) {
        super.updated(_changedProperties);

    }


}

