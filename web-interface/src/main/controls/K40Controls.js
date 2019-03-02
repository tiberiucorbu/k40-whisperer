import {css, html, LitElement} from 'lit-element';

export class K40Controls extends LitElement {

    static get properties() {
        return {
            mood: {type: String}
        }
    }

    static get styles() {
        return css`
        :host { 
            min-width : 10rem; height: 100%; display : flex; flex-flow: column nowrap;
        }
        
        div {
            flex-grow : 1;
        }
        `;
    }

    render() {
        return html`
        <div>
            Hello
            <k40-connect></k40-connect>
        </div>
`;
    }
}

