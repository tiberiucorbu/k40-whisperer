import {css, html, LitElement} from 'lit-element';

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
            slot[name='aside']::slotted(*) {
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

