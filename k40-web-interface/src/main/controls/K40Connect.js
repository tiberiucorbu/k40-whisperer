import {css, html, LitElement} from 'lit-element';

export class K40Connect extends LitElement {

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
        `;
    }

    render() {
        return html`
        <div>
            <vaadin-button>Connect</vaadin-button>
            
        </div>
`;
    }
}

