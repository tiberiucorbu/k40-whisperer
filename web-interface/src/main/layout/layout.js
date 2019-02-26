import {css, html, LitElement} from 'https://unpkg.com/lit-element/lit-element.js?module';

export class K40Layout extends LitElement {

    static get styles() {
        return css`
            :host {
                width : 100%;
                height: 100%;
                display : flex;
                flex-flow : row nowrap;
            }
            #main {
                flex-grow : 1;
            }
            ::slotted([aside]) {
                height: 100%;
                display:block;
            }
        `;
    }

    render() {
        return html`
            <aside id="aside">
                <slot name="aside"></slot>
            </aside>
            <div id="main">
                <slot></slot>
                <footer>
                    <slot name="status"></slot>
                </footer>
            </div>
`;
    }
}

