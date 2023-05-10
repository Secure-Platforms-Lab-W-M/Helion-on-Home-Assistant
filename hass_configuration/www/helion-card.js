import "https://unpkg.com/wired-card@0.8.1/wired-card.js?module";
import "https://unpkg.com/wired-toggle@0.8.0/wired-toggle.js?module";
import {
  LitElement,
  html,
  css
} from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";

function loadCSS(url) {
  const link = document.createElement("link");
  link.type = "text/css";
  link.rel = "stylesheet";
  link.href = url;
  document.head.appendChild(link);
}

class Helion extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: {}
    };
  }

  render() {
    return html`
    <p id = "entitiy" style="color:#8db3e2;font-size:22px;"> <b> Helion </b> </p>
        
    <p style="font-size:18px;"> <b> Simulated Events </b> </p>

    <fieldset class="multiswitch">
      <legend>Configuration</legend>

      <div class="slide-container">
        <input type="radio" name="method" id="method1" checked>
        <label for="method1">Backoff</label>
        <input type="radio" name="method" id="method2">
        <label for="method2">Interpolation</label>
        <!-- leave this "slide" -->
        <a class="slide" aria-hidden="true"></a>
      </div>

      <div class="slide-container">
        <input type="radio" name="model" id="model1" checked>
        <label for="model1">3 grams</label>
        <input type="radio" name="model" id="model2">
        <label for="model2">4 grams</label>
        <!-- leave this "slide" -->
        <a class="slide" aria-hidden="true"></a>
      </div>

      <div class="slide-container">
        <input type="radio" name="flavor" id="flavor1" checked>
        <label for="flavor1">Up</label>
        <input type="radio" name="flavor" id="flavor2">
        <label for="flavor2">Down</label>
        <input type="radio" name="flavor" id="flavor3">
        <label for="flavor3">Strange</label>
        <!-- leave this "slide" -->
        <a class="slide" aria-hidden="true"></a>
      </div>
    </fieldset>

    <p> Tokens </p>

    <select size="10">  <!-- Note: I've removed the 'multiple' attribute -->
      <option>Turn the lights on</option>
      <option>Switch off the light</option>
      <option>Turn the humidifier on</option>
      <option>Robot Vacuum off</option>
      <option>Turn the lights on</option>
      <option>Switch off the light</option>
      <option>Turn the humidifier on</option>
      <option>Robot Vacuum off</option>
      <option>Turn the lights on</option>
      <option>Switch off the light</option>
      <option>Turn the humidifier on</option>
      <option>Robot Vacuum off</option>
      <option>Turn the lights on</option>
      <option>Switch off the light on</option>
      <option>Turn the humidifier on</option>
      <option>Robot Vacuum off</option>
    </select>
    `;
  }

  setConfig(config) {
    this.config = config;
  }

  // The height of your card. Home Assistant uses this to automatically
  // distribute all cards over the available columns.
  getCardSize() {
    return 10;
  }

  static get styles() {
    return css`
    :host {
      padding: 16px;
      display: block;
    }

    select {
      margin-left: 4px;
      padding-left: 4px;
    }

    option {
      padding: 4px;
      margin-left: 4px;
    }

    .multiswitch input {
      position: absolute;
      left: -200vw;
    }

    .multiswitch .slide-container {
      position: relative;
      margin-bottom: 10px;
      display: flex;
      max-width: 15em;
      line-height: 2em;
      /* don't allow highlighting the text inside the toggle */
      user-select: none;
    }

    .multiswitch .slide-container label {
      /* Even though we're using "flex" to display, we have to assign widths so that we know exactly where to position the slide */
      width: 50%;
      text-align: center;
      padding-left: 1em;
      padding-right: 1em;
      z-index: 2;
    }

    .multiswitch .slide-container a {
      position: absolute;
      left: 50%;
      z-index: 1;
      height: 100%;
      width: 50%;
      transition: left 0.1s ease-out;
      box-shadow: 1px 0 0 rgba(0, 0, 0, 0.2),
                  inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }

    /*
      Auto adjusting widths
    */
    .multiswitch label:nth-last-child(6),
    .multiswitch label:nth-last-child(6) ~ label,
    .multiswitch label:nth-last-child(6) ~ a {
      width: 33.3334%;
    }

    .multiswitch label:nth-last-child(8),
    .multiswitch label:nth-last-child(8) ~ label,
    .multiswitch label:nth-last-child(8) ~ a {
      width: 25%;
    }

    .multiswitch label:nth-last-child(10),
    .multiswitch label:nth-last-child(10) ~ label,
    .multiswitch label:nth-last-child(10) ~ a {
      width: 20%;
    }

    .multiswitch label:nth-last-child(12),
    .multiswitch label:nth-last-child(12) ~ label,
    .multiswitch label:nth-last-child(12) ~ a {
      width: 16.6667%;
    }

    /*
     Slider
    */

    /* all options, first selected */
    .multiswitch input:checked ~ a {
      left: 0;
      box-shadow: 1px 0 0 rgba(0, 0, 0, 0.2),
                  inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    /* 2 options, 2nd selected */
    .multiswitch label:nth-last-child(4) ~ input:nth-child(3):checked ~ a {
      left: 50%;
    }
    /* 3 options, 2nd selected */
    .multiswitch label:nth-last-child(6) ~ input:nth-child(3):checked ~ a {
      left: 33.3334%;
    }
    /* 3 options, 3rd selected */
    .multiswitch label:nth-last-child(6) ~ input:nth-child(5):checked ~ a {
      left: 66.6667%;
    }

    /*
      Slider shadows
    */
    /* middle spots */
    .multiswitch input:not(:first-child):checked ~ a {
      box-shadow: 1px 0 0 rgba(0, 0, 0, 0.2),
                  -1px 0 0 rgba(0, 0, 0, 0.2),
                  inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    /* last spots */
    .multiswitch label:nth-last-child(4) ~ input:nth-child(3):checked ~ a,
    .multiswitch label:nth-last-child(6) ~ input:nth-child(5):checked ~ a,
    .multiswitch label:nth-last-child(8) ~ input:nth-child(7):checked ~ a,
    .multiswitch label:nth-last-child(10) ~ input:nth-child(9):checked ~ a,
    .multiswitch label:nth-last-child(12) ~ input:nth-child(11):checked ~ a {
      box-shadow: -1px 0 0 rgba(0, 0, 0, 0.2),
                  inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }

    /*
     RH Brand Styling
    */
    body {
      padding: 30px;
    }

    fieldset {
      border: 0;
      padding: 0;
      margin-bottom: 1em;
    }

    fieldset legend {
      display: block;
      margin-bottom: 5px;
      font-weight: 600;
    }

    .multiswitch .slide-container {
      background: #333;
      color: #fff;
      transition: background 0.1s ease-out;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.3);
    }

    .multiswitch .slide-container label {
      cursor: pointer;
      text-shadow: 0 1px 1px rgba(0, 0, 0, .4);
    }

    .multiswitch .slide-container a {
      background: #0088ce;
      border: 1px solid #005f90;
    }

    /*
     Horizontal layout
    */
    .switch {
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
    }

    .multiswitch input:focus ~ a {
      outline: 2px solid #0088ce;
    }

    p {
      color: #ffffff;
      padding-left: 4px;
    }

    button {
      margin-left: 4px;
      padding-left: 4px;
    }

    input {
      margin-left: 4px;
      padding-left: 4px;
    }
    `;
  }
}
customElements.define("helion-card", Helion);
