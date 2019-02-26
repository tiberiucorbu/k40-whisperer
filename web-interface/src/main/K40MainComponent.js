import {LitElement, html, css} from 'https://unpkg.com/lit-element/lit-element.js?module';

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
        return html`
        <k40-layout>
            <k40-controlls slot="aside"></k40-controlls>
            <k40-plot></k40-plot>
            <k40-status slot="status"></k40-status>
        </k40-layout>
`;
    }
}

