import "@vaadin/vaadin-dialog";
import "@vaadin/vaadin-button";
import '@vaadin/vaadin-checkbox';
import '@vaadin/vaadin-form-layout';
import '@vaadin/vaadin-text-field/vaadin-text-field.js';
import '@vaadin/vaadin-text-field/vaadin-text-area.js';

import {K40Main} from './main/K40MainComponent.js';
import {K40Connect} from "./main/controls/K40Connect.js";
import {K40Controls} from "./main/controls/K40Controls.js";
import {K40Layout} from "./main/layout/layout.js";
import {K40ConnectionConfiguration} from "./main/configuration/K40ConfigurationComponent";
import {K40WssTextField} from "./main/configuration/K40WssTextField";


customElements.define('k40-layout', K40Layout);
customElements.define('k40-main', K40Main);

customElements.define(K40WssTextField.is, K40WssTextField);
customElements.define('k40-controls', K40Controls);
customElements.define('k40-connect', K40Connect);
customElements.define('k40-connection-configuration', K40ConnectionConfiguration);